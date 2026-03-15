# 拍卖模块 — 项目铁律

> 本文件继承[全局 constitution.md](../../constitution.md)，额外定义本项目的不可变约束。
> 项目级约束**可以更严格**，但**不可削弱**全局铁律的任何条款。

## 继承的全局铁律

参见根目录 `constitution.md`（12 条全局约束自动生效）。

## 项目特有约束

### 技术约束
- **TC-01**: 严禁裸 SQL，必须使用 ORM。**唯一例外**：竞价并发锁 `FOR UPDATE`（需 [ADR-002](../adr/002-concurrency-locking.md) 背书）
- **TC-02**: 必须通过 `_inherit` 扩展标准模块，禁止直接修改 Odoo 核心代码

### 业务约束
- **BC-01**: 所有金额字段必须使用 `Monetary` 类型 + `currency_id` 伴侣字段
- **BC-02**: 拍品和拍卖会不做物理删除，使用软删除（`active` 字段）
- **BC-03**: 出价记录 (`auction.bid`) **不可修改、不可删除**（ACL 级别强制）

### 安全约束
- **SC-01**: 每个 Model 必须定义 `ir.model.access.csv`，至少涵盖 Manager/User/Base 三级权限
- **SC-02**: 底价字段 (`reserve_price`) 通过 `groups="auction_lot.group_auction_manager"` 限制可见性，确保仅拍卖经理可见
