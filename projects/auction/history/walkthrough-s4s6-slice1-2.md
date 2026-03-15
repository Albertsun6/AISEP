# Walkthrough: 菜单修复 + Slice-3 S4 + 集成 UI 验收

## 完成总览

| # | 任务 | 结果 |
|---|------|------|
| 1 | 菜单修复 | admin 自动获得拍卖经理权限 ✅ |
| 2 | Slice-3 S4 设计 | design.yaml 310行 · Gate 通过 ✅ |
| 3 | 集成 UI 验收 | Slice-1+2 全菜单可用 ✅ |

---

## 1. 菜单修复

在 `auction_lot_security.xml` 的 `group_auction_manager` 中追加 `users` 字段，安装时自动将 admin 加入拍卖经理组：

```xml
<field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
```

## 2. Slice-3 S4 竞价引擎设计

| 维度 | 内容 |
|------|------|
| Model | `auction.bidding.round`(12字段+4方法) / `auction.bid`(6字段+immutable) |
| 核心方法 | `place_bid`(FOR UPDATE) / `_check_hammer`(三路判定) / `accept/reject_conditional` |
| ADR | ADR-001(Bus推送) + ADR-002(FOR UPDATE锁) |

## 3. 集成 UI 验收

````carousel
![菜单修复验证 — 安装后自动显示"拍卖管理"](/Users/yongqian/.gemini/antigravity/brain/08d65e3f-8789-402d-99a8-74c8fbb3c844/menu_visible.png)
<!-- slide -->
![拍品表单 — 顶部显示双菜单（拍品管理+拍卖会管理）](/Users/yongqian/.gemini/antigravity/brain/08d65e3f-8789-402d-99a8-74c8fbb3c844/lot_form.png)
<!-- slide -->
![拍卖会表单 — 状态栏+规则页签+编排页签](/Users/yongqian/.gemini/antigravity/brain/08d65e3f-8789-402d-99a8-74c8fbb3c844/session_form.png)
````

![集成验收全流程录屏](/Users/yongqian/.gemini/antigravity/brain/08d65e3f-8789-402d-99a8-74c8fbb3c844/integration_ui_verification_1773615974576.webp)

## 项目进度

```
Slice-1 拍品管理  ██████████████ S4✅ S5✅ S6✅
Slice-2 拍卖会编排 ██████████████ S4✅ S5✅ S6✅
Slice-3 竞价引擎  ███░░░░░░░░░░░ S4✅ S5⬜ S6⬜
```
