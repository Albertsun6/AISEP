# 制造业 ERP — 部署指南

> 适用于：proj-001 制造业 ERP 系统（Odoo 17 + 4 自定义模块）

---

## 一、环境要求

| 组件 | 版本 | 备注 |
|------|------|------|
| Docker | ≥ 20.10 | 包含 Docker Compose V2 |
| Odoo | 17.0 | 官方镜像 `odoo:17.0` |
| PostgreSQL | 16 | 官方镜像 `postgres:16` |
| 磁盘 | ≥ 2 GB | Odoo + DB 数据 |
| 内存 | ≥ 2 GB | 推荐 4 GB |

---

## 二、快速启动

```bash
# 1. 进入项目目录
cd projects/proj-001

# 2. 启动服务
docker compose up -d

# 3. 首次初始化（安装所有自定义模块）
docker compose run --rm odoo odoo -d aisep_mfg \
  -i sale_mfg,stock_mfg,purchase_mfg,mrp_mfg \
  --stop-after-init

# 4. 重启 Odoo
docker compose restart odoo

# 5. 访问
open http://localhost:18069
# 默认账户: admin / admin
```

---

## 三、模块更新

代码修改后，执行模块更新：

```bash
# 停止 Odoo
docker compose stop odoo

# 更新指定模块（-u）
docker compose run --rm odoo odoo -d aisep_mfg \
  -u mrp_mfg,stock_mfg,sale_mfg,purchase_mfg \
  --stop-after-init

# 重新启动
docker compose start odoo
```

---

## 四、自定义模块清单

| 模块 | 路径 | 功能 | 依赖 |
|------|------|------|------|
| `sale_mfg` | `addons/sale_mfg/` | 销售管理扩展（客户/报价/订单/发货跟踪） | sale_management, stock, product |
| `stock_mfg` | `addons/stock_mfg/` | 库存管理扩展（出入库/调拨/盘点菜单） | stock, product, sale_mfg |
| `purchase_mfg` | `addons/purchase_mfg/` | 采购管理扩展（供应商/询价/收货） | purchase, stock, product |
| `mrp_mfg` | `addons/mrp_mfg/` | 制造管理扩展（BOM/生产/领料/报工/MRP建议） | mrp, stock, product, sale |

**安装顺序（拓扑序）**：`sale_mfg` → `stock_mfg` → `purchase_mfg` → `mrp_mfg`

---

## 五、docker-compose.yaml 关键配置

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: postgres
    volumes:
      - pg-data:/var/lib/postgresql/data

  odoo:
    image: odoo:17.0
    depends_on: [db]
    ports:
      - "18069:8069"
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
```

---

## 六、备份与恢复

```bash
# 数据库备份
docker compose exec db pg_dump -U odoo aisep_mfg > backup_$(date +%Y%m%d).sql

# 数据库恢复
docker compose exec -T db psql -U odoo aisep_mfg < backup_20260313.sql
```

---

## 七、生产环境注意事项

> [!CAUTION]
> 以下配置在生产环境中必须调整：

1. **修改默认密码**：`admin` 账户和 PostgreSQL 密码
2. **启用 HTTPS**：通过 Nginx 反向代理 + Let's Encrypt
3. **设置 `admin_passwd`**：在 `odoo.conf` 中配置 master password
4. **禁用调试模式**：移除 URL 中的 `?debug=` 参数
5. **配置 `db_filter`**：限制可访问的数据库名
6. **日志配置**：设置 `logfile` 和 `log_level`
7. **定时备份**：配置 cron job 执行数据库备份
