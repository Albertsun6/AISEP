import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BiddingLiveController(http.Controller):
    """竞价直播页面控制器"""

    @http.route(
        '/auction/live/<int:round_id>',
        type='http',
        auth='user',
        website=False,
    )
    def bidding_live_page(self, round_id, **kw):
        """渲染竞价直播页面"""
        bidding_round = request.env['auction.bidding.round'].sudo().browse(round_id)
        if not bidding_round.exists():
            return request.not_found()

        lot = bidding_round.lot_id
        session = bidding_round.session_id

        # 最近 50 条出价记录
        bids = bidding_round.bid_ids.sorted('bid_time', reverse=True)[:50]

        # 计算最低出价
        if bidding_round.current_price:
            min_bid = bidding_round.current_price + bidding_round.bid_increment
        else:
            min_bid = bidding_round.starting_price

        values = {
            'bidding_round': bidding_round,
            'lot': lot,
            'session': session,
            'bids': bids,
            'min_bid': min_bid,
            'db_name': request.env.cr.dbname,
            'user': request.env.user,
        }
        return request.render(
            'auction_bidding.bidding_live_page', values
        )

    @http.route(
        '/auction/bid',
        type='json',
        auth='user',
        methods=['POST'],
    )
    def place_bid_api(self, round_id, amount, **kw):
        """JSON-RPC 出价接口"""
        try:
            bidding_round = request.env['auction.bidding.round'].browse(round_id)
            if not bidding_round.exists():
                return {'error': '竞价轮次不存在'}

            bidder = request.env.user.partner_id
            bid = bidding_round.place_bid(bidder.id, amount)

            return {
                'success': True,
                'bid_id': bid.id,
                'current_price': bidding_round.current_price,
                'bid_count': bidding_round.bid_count,
            }
        except Exception as e:
            _logger.warning('Bid failed: %s', str(e))
            return {'error': str(e)}

    @http.route(
        '/auction/api/round/<int:round_id>',
        type='json',
        auth='user',
        methods=['POST'],
    )
    def get_round_status(self, round_id, **kw):
        """获取竞价轮次状态（用于页面初始化和断线重连）"""
        bidding_round = request.env['auction.bidding.round'].sudo().browse(round_id)
        if not bidding_round.exists():
            return {'error': '竞价轮次不存在'}

        bids = bidding_round.bid_ids.sorted('bid_time', reverse=True)[:50]

        return {
            'round_id': bidding_round.id,
            'state': bidding_round.state,
            'current_price': bidding_round.current_price or 0,
            'starting_price': bidding_round.starting_price,
            'bid_increment': bidding_round.bid_increment,
            'bid_count': bidding_round.bid_count,
            'lot_name': bidding_round.lot_id.name,
            'session_name': bidding_round.session_id.name,
            'bids': [{
                'id': b.id,
                'bidder': b.bidder_id.name,
                'amount': b.amount,
                'time': b.bid_time.strftime('%H:%M:%S') if b.bid_time else '',
                'is_winning': b.is_winning,
            } for b in bids],
        }
