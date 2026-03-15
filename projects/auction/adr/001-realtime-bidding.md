# ADR-001: 实时竞价推送方案选择

## 背景（Context）

竞价引擎需要将最新出价信息实时推送给所有在线竞拍者。Odoo 17 原生不支持 WebSocket 协议，但内置了 `bus.bus` 长轮询机制。项目 `known_risks` 中 `risk-001` 已标记此风险。

## 备选方案

| 方案 | 延迟 | 复杂度 | 运维成本 | 扩展性 |
|------|------|--------|---------|--------|
| **A: 短轮询 (Polling)** | ~3-5s | 低 | 低 | 差（大量无效请求） |
| **B: Odoo Bus (Long Polling)** | ~1-2s | 中 | 低 | 中（Odoo 内建） |
| **C: 独立 WebSocket 服务** | <100ms | 高 | 高（额外进程/部署） | 优 |

## 决策（Decision）

选择 **方案 B: Odoo Bus (Long Polling)**。

## 理由（Rationale）

1. **技术栈统一**：不引入额外语言/框架（Node.js/FastAPI），降低团队认知成本
2. **零额外运维**：Odoo 自带 longpolling worker（端口 8072），无需独立部署
3. **够用原则**：线上拍卖的出价频率通常为每分钟数十次，1-2s 延迟可接受
4. **迁移预留**：`place_bid()` 方法内的推送逻辑封装为 `_notify_bid_update()`，未来迁移 WebSocket 只需替换此方法

## 后果（Consequences）

- ✅ 部署简单，开发快速
- ⚠️ 延迟略高，不适合超高频拍卖场景（如 1000+人同时竞价）
- ⚠️ 如果未来需亚秒级推送，需引入独立 WebSocket 服务（方案 C），但接口已预留

## 状态：accepted
