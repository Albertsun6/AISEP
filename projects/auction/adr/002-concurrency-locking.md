# ADR-002: 并发竞价一致性策略

## 背景（Context）

在线竞价场景中，多个竞拍者可能"同时"提交出价。如果不做并发控制，可能出现：
- 两个出价都基于同一个 `current_price` 验证通过
- 产生两笔"最高出价"，数据不一致
- 最终成交价低于应有价格

Odoo ORM 的 `write()` 不提供行级锁语义，无法解决这类 **Lost Update** 问题。
项目 `known_risks` 中 `risk-002` 已标记此风险。

## 备选方案

| 方案 | 一致性 | 性能影响 | 实现复杂度 |
|------|--------|---------|-----------|
| **A: ORM write() 直接写** | ❌ 无保障 | 无 | 低 |
| **B: 乐观锁（Version 字段）** | ⚠️ 需重试 | 低 | 中 |
| **C: PostgreSQL FOR UPDATE** | ✅ 强一致 | 中（短时锁） | 中 |
| **D: Redis 分布式锁** | ✅ 强一致 | 低 | 高（引入 Redis） |

## 决策（Decision）

选择 **方案 C: PostgreSQL `SELECT ... FOR UPDATE`** 行级锁。

## 理由（Rationale）

1. **强一致性**：在 `place_bid()` 方法中，先 `FOR UPDATE` 锁定 `auction.bidding.round` 行，再校验金额、写入出价、更新 `current_price`，整个事务串行化
2. **不引入新依赖**：基于 PostgreSQL 事务的行级锁，无需额外中间件
3. **锁粒度精确**：只锁单个 `BiddingRound` 行（按 lot 级别），不影响其他拍品的竞价
4. **锁持有时长短**：单次出价事务（校验 + 写入 + 推送）预期 <50ms，对性能影响可接受

## 实现要点

```python
def place_bid(self, bidder_id, amount):
    """出价方法 — 含行级锁保障并发一致性"""
    self.ensure_one()
    # 1. 行级锁 — 串行化同一拍品的并发出价
    self.env.cr.execute(
        "SELECT id FROM auction_bidding_round WHERE id = %s FOR UPDATE",
        [self.id]
    )
    # 2. 刷新内存记录（锁定后 ORM 缓存可能过期）
    self.invalidate_recordset()
    # 3. 校验
    min_bid = (self.current_price or self.starting_price) + self.bid_increment
    if amount < min_bid:
        raise UserError(f"出价必须 ≥ {min_bid}")
    # 4. 创建出价记录 + 更新当前价
    self.env['auction.bid'].create({...})
    self.current_price = amount
    # 5. 推送通知
    self._notify_bid_update()
```

## 后果（Consequences）

- ✅ 强一致性，杜绝并发"超卖"
- ⚠️ 使用了 `self.env.cr.execute()`（裸 SQL），偏离 pitfalls P3-03 的指导
- ⚠️ 极端高并发时（>100 人/秒对同一拍品），排队等锁可能导致延迟增加
- 📝 `constitution.md` 已记录此例外：竞价锁场景允许裸 SQL，需引用本 ADR

## 状态：accepted
