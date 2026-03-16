/**
 * 竞价直播页面 JavaScript
 *
 * 功能：
 * 1. 连接 Odoo Bus Long Polling 接收实时出价推送
 * 2. 提交出价（JSON-RPC → Controller → place_bid）
 * 3. 实时更新 DOM（价格脉冲、出价列表滑入、Toast 通知）
 */

(function () {
    'use strict';

    // ── 数据初始化 ──────────────────────────
    const dataEl = document.getElementById('auction-data');
    const DATA = JSON.parse(dataEl.textContent);

    let currentPrice = DATA.current_price || DATA.starting_price;
    let bidCount = DATA.bid_count;
    let minBid = DATA.min_bid;
    let state = DATA.state;

    // ── DOM 引用 ────────────────────────────
    const priceAmount = document.getElementById('price-amount');
    const bidCountEl = document.getElementById('bid-count');
    const bidAmountInput = document.getElementById('bid-amount');
    const bidButton = document.getElementById('bid-button');
    const bidForm = document.getElementById('bid-form');
    const minBidDisplay = document.getElementById('min-bid-display');
    const historyList = document.getElementById('history-list');
    const historyCount = document.getElementById('history-count');
    const statusBadge = document.getElementById('status-badge');
    const liveBadge = document.getElementById('live-badge');
    const toastContainer = document.getElementById('toast-container');

    // ── Bus Polling（Odoo 17 peek_notifications）──
    let lastId = 0;
    let pollActive = true;
    // Odoo 17 uses /websocket/peek_notifications (JSON-RPC)
    const POLL_URL = '/websocket/peek_notifications';
    const BUS_CHANNEL = DATA.db_name + '/auction.bidding.round/' + DATA.round_id;

    function startPolling() {
        if (!pollActive || state !== 'open') return;
        // 首次轮询标记
        doPoll(true);
    }

    function doPoll(isFirst) {
        if (!pollActive) return;

        fetch(POLL_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                id: Date.now(),
                params: {
                    channels: [BUS_CHANNEL],
                    last: lastId,
                    is_first_poll: isFirst || false,
                }
            }),
        })
        .then(function (resp) { return resp.json(); })
        .then(function (data) {
            if (data.result && data.result.notifications) {
                data.result.notifications.forEach(function (notif) {
                    if (notif.id) lastId = Math.max(lastId, notif.id);
                    var payload = notif.message || notif;
                    if (payload.type === 'new_bid' && payload.payload) {
                        handleNewBid(payload.payload);
                    }
                });
            }
            // 继续轮询（3s 间隔，避免过于频繁）
            if (pollActive && state === 'open') {
                setTimeout(function () { doPoll(false); }, 3000);
            }
        })
        .catch(function (err) {
            console.warn('Bus poll error:', err);
            // 断线重连（较长间隔）
            if (pollActive) {
                setTimeout(function () { doPoll(false); }, 5000);
            }
        });
    }

    // ── 处理新出价推送 ──────────────────────
    function handleNewBid(payload) {
        // 更新价格
        currentPrice = payload.amount;
        bidCount = payload.bid_count || (bidCount + 1);
        minBid = currentPrice + DATA.bid_increment;

        updatePriceDisplay();
        updateBidCount();
        updateMinBid();

        // 添加出价历史条目
        addBidHistoryItem({
            time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
            bidder: '竞拍者 #' + payload.bidder_id,
            amount: payload.amount,
            isWinning: true,
        });

        // Toast
        showToast('新的出价: ¥' + formatNumber(payload.amount), 'info');
    }

    // ── 更新 DOM ───────────────────────────
    function updatePriceDisplay() {
        priceAmount.textContent = formatNumber(currentPrice);
        // 脉冲动画
        var priceEl = document.getElementById('current-price');
        priceEl.classList.add('pulse');
        setTimeout(function () { priceEl.classList.remove('pulse'); }, 600);
    }

    function updateBidCount() {
        bidCountEl.textContent = bidCount;
    }

    function updateMinBid() {
        minBidDisplay.textContent = formatNumber(minBid);
        bidAmountInput.min = minBid;
        bidAmountInput.placeholder = formatNumber(minBid);
    }

    function addBidHistoryItem(bid) {
        // 移除空状态提示
        var emptyEl = historyList.querySelector('.history-empty');
        if (emptyEl) emptyEl.remove();

        // 更新旧的最高标记
        var oldWinning = historyList.querySelectorAll('.history-item.winning');
        oldWinning.forEach(function (el) {
            el.classList.remove('winning');
            var badge = el.querySelector('.bid-winning');
            if (badge) badge.remove();
        });

        // 创建新条目
        var item = document.createElement('div');
        item.className = 'history-item new-entry' + (bid.isWinning ? ' winning' : '');
        item.innerHTML =
            '<span class="bid-time">' + escapeHtml(bid.time) + '</span>' +
            '<span class="bid-bidder">' + escapeHtml(bid.bidder) + '</span>' +
            '<span class="bid-amount">¥ ' + formatNumber(bid.amount) + '</span>' +
            (bid.isWinning ? '<span class="bid-winning">👑 最高</span>' : '');

        historyList.insertBefore(item, historyList.firstChild);

        // 更新计数
        historyCount.textContent = '(' + historyList.querySelectorAll('.history-item').length + ')';
    }

    function updateStatus(newState) {
        state = newState;
        var statusMap = {
            'open': '🟢 竞价中',
            'hammer': '🏆 已成交',
            'unsold': '⚫ 流拍',
            'conditional_pending': '🟡 有条件成交-待确认',
            'conditional_accepted': '🏆 有条件成交-已接受',
            'conditional_rejected': '🔴 有条件成交-已拒绝',
        };
        statusBadge.textContent = statusMap[newState] || newState;

        if (newState !== 'open') {
            bidForm.style.display = 'none';
            liveBadge.classList.add('ended');
            liveBadge.innerHTML = '<span>ENDED</span>';
            pollActive = false;
        }
    }

    // ── 出价提交 ────────────────────────────
    function submitBid() {
        var amount = parseFloat(bidAmountInput.value);
        if (isNaN(amount) || amount < minBid) {
            showToast('出价金额必须 ≥ ¥' + formatNumber(minBid), 'error');
            bidAmountInput.focus();
            return;
        }

        bidButton.disabled = true;
        bidButton.classList.add('loading');

        fetch('/auction/bid', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'call',
                id: Date.now(),
                params: {
                    round_id: DATA.round_id,
                    amount: amount,
                }
            }),
        })
        .then(function (resp) { return resp.json(); })
        .then(function (data) {
            bidButton.disabled = false;
            bidButton.classList.remove('loading');

            if (data.result && data.result.success) {
                showToast('出价成功！¥' + formatNumber(amount), 'success');
                bidAmountInput.value = '';
                // 价格更新将由 Bus 推送触发
            } else {
                var err = (data.result && data.result.error) || '出价失败';
                showToast(err, 'error');
            }
        })
        .catch(function (err) {
            bidButton.disabled = false;
            bidButton.classList.remove('loading');
            showToast('网络错误，请重试', 'error');
        });
    }

    // ── Toast 通知 ──────────────────────────
    function showToast(message, type) {
        var toast = document.createElement('div');
        toast.className = 'toast ' + (type || 'info');
        toast.textContent = message;
        toastContainer.appendChild(toast);

        setTimeout(function () {
            toast.classList.add('fade-out');
            setTimeout(function () { toast.remove(); }, 300);
        }, 3000);
    }

    // ── 工具函数 ────────────────────────────
    function formatNumber(n) {
        return parseFloat(n).toLocaleString('zh-CN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        });
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ── 事件绑定 ────────────────────────────
    bidButton.addEventListener('click', submitBid);

    bidAmountInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            submitBid();
        }
    });

    // ── 初始化 ──────────────────────────────
    function init() {
        // 设置初始最低出价
        bidAmountInput.min = minBid;
        bidAmountInput.placeholder = formatNumber(minBid);

        // 如果当前非竞价中，隐藏出价表单
        if (state !== 'open') {
            updateStatus(state);
        } else {
            // 启动 Bus 轮询
            startPolling();
        }
    }

    init();
})();
