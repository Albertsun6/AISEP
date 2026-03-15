# Walkthrough: Auction 线上拍卖系统 — 完整交付

## 项目总览

| 阶段 | Slice-1 拍品管理 | Slice-2 拍卖会编排 | Slice-3 竞价引擎 |
|------|-----------------|-------------------|-----------------|
| S4 设计 | ✅ | ✅ | ✅ |
| S5 代码 | ✅ 33 tests | ✅ 20 tests | ✅ 21 tests |
| S6 测试 | ✅ 7轮迭代 | ✅ 2轮迭代 | ✅ 一次通过 |
| S7 部署 | — | — | ✅ Docker Compose |

**总测试覆盖：74 tests / 0 failures / 0 errors**

---

## 模块统计

| 模块 | 文件 | 行数 | Model | 核心方法 |
|------|------|------|-------|---------|
| auction_lot | 15 | ~800 | 3 | approve/assign/sell + 图片约束 + 分类树 |
| auction_session | 11 | 766 | 2 | publish/start/close/cancel + 拍品唯一性 |
| auction_bidding | 10 | 852 | 2 | place_bid(FOR UPDATE) + 三路落槌 + immutable |
| **合计** | **36** | **~2418** | **7** | |

---

## 关键设计决策

1. **FOR UPDATE 行级锁** — `place_bid` 防止并发超卖
2. **Bus 实时推送** — 出价后 `bus._sendone` 通知前端
3. **三路落槌判定** — 成交 / 有条件 / 流拍，阈值从 session 读取
4. **bid 不可修改** — ORM write/unlink 覆写，允许计算字段更新
5. **菜单修复** — admin 自动加入 `group_auction_manager`

## 部署

```bash
cd deploy/
./prepare.sh          # 复制 3 模块到 addons/
cp .env.example .env  # 修改密码
docker compose up -d  # 启动 Odoo + PG + Nginx
```

## 集成验收截图

````carousel
![菜单自动可见](/Users/yongqian/Desktop/AISEP250311/projects/auction/history/menu_visible.png)
<!-- slide -->
![拍品表单](/Users/yongqian/Desktop/AISEP250311/projects/auction/history/lot_form.png)
<!-- slide -->
![拍卖会表单](/Users/yongqian/Desktop/AISEP250311/projects/auction/history/session_form.png)
````
