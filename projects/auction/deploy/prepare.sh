#!/bin/bash
# Auction System — 部署准备脚本
# 将 Slice 代码复制到 deploy/addons/ 目录

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ADDONS_DIR="$SCRIPT_DIR/addons"
SLICES_DIR="$(cd "$SCRIPT_DIR/../artifacts/slices" && pwd)"

echo "=== Auction Deploy: 复制模块到 $ADDONS_DIR ==="

rm -rf "$ADDONS_DIR"
mkdir -p "$ADDONS_DIR"

# Slice-1: 拍品管理
cp -r "$SLICES_DIR/slice-1/code/auction_lot" "$ADDONS_DIR/"
echo "✓ auction_lot"

# Slice-2: 拍卖会编排
cp -r "$SLICES_DIR/slice-2/code/auction_session" "$ADDONS_DIR/"
echo "✓ auction_session"

# Slice-3: 竞价引擎
cp -r "$SLICES_DIR/slice-3/code/auction_bidding" "$ADDONS_DIR/"
echo "✓ auction_bidding"

echo "=== 完成! 共 $(ls -d $ADDONS_DIR/*/ | wc -l | tr -d ' ') 个模块 ==="
echo "下一步: cp .env.example .env && vim .env && docker compose up -d"
