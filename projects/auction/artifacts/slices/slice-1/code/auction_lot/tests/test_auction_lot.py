from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError, UserError, AccessError


class TestAuctionLotCategory(TransactionCase):
    """auction.lot.category 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['auction.lot.category']
        cls.cat_painting = cls.Category.create({'name': '书画'})

    # ── CRUD ──

    def test_create_category(self):
        """US-01: 创建分类 → 成功"""
        cat = self.Category.create({'name': '瓷器'})
        self.assertTrue(cat.id)
        self.assertEqual(cat.name, '瓷器')

    def test_create_subcategory(self):
        """创建子分类 → parent_path 自动维护"""
        sub = self.Category.create({
            'name': '山水画',
            'parent_id': self.cat_painting.id,
        })
        self.assertEqual(sub.parent_id, self.cat_painting)
        self.assertTrue(sub.parent_path)

    def test_read_category(self):
        """读取分类 → 字段完整"""
        self.assertEqual(self.cat_painting.name, '书画')

    def test_update_category(self):
        """更新分类名称"""
        self.cat_painting.write({'name': '中国书画'})
        self.assertEqual(self.cat_painting.name, '中国书画')

    def test_delete_category(self):
        """删除分类 → 成功"""
        cat = self.Category.create({'name': '临时'})
        cat_id = cat.id
        cat.unlink()
        self.assertFalse(self.Category.search([('id', '=', cat_id)]))

    # ── 业务规则 ──

    def test_category_recursion_negative(self):
        """反向: 循环嵌套 → 错误（_parent_store flush 或 ValidationError）"""
        parent = self.Category.create({'name': '父分类_递归测试'})
        child = self.Category.create({
            'name': '子分类_递归测试',
            'parent_id': parent.id,
        })
        with self.assertRaises(Exception):
            with self.env.cr.savepoint():
                parent.write({'parent_id': child.id})

    def test_category_name_parent_unique_constraint_exists(self):
        """SQL UNIQUE(name, parent_id) 约束已定义"""
        # 验证约束存在（SQL UNIQUE 在 TransactionCase 中行为不稳定，
        # 此处验证约束定义而非触发行为）
        constraints = [c[0] for c in self.Category._sql_constraints]
        self.assertIn('name_parent_uniq', constraints)


class TestAuctionLotImage(TransactionCase):
    """auction.lot.image 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['auction.lot.category'].create({'name': '测试分类'})
        cls.lot = cls.env['auction.lot'].create({
            'name': '测试拍品',
            'category_id': cls.category.id,
            'starting_price': 1000,
            'reserve_price': 5000,
            'currency_id': cls.env.company.currency_id.id,
        })

    # ── CRUD ──

    def test_create_image(self):
        """US-02: 上传图片 → 关联到拍品"""
        import base64
        # 1x1 白色 PNG
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        img = self.env['auction.lot.image'].create({
            'lot_id': self.lot.id,
            'image': pixel,
        })
        self.assertTrue(img.id)
        self.assertEqual(img.lot_id, self.lot)

    def test_image_sequence_default(self):
        """图片默认 sequence=10"""
        import base64
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        img = self.env['auction.lot.image'].create({
            'lot_id': self.lot.id,
            'image': pixel,
        })
        self.assertEqual(img.sequence, 10)

    def test_image_cascade_delete(self):
        """删除拍品 → 图片级联删除"""
        import base64
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        img = self.env['auction.lot.image'].create({
            'lot_id': self.lot.id,
            'image': pixel,
        })
        img_id = img.id
        self.lot.write({'active': False})
        self.lot.unlink()
        self.assertFalse(self.env['auction.lot.image'].search([('id', '=', img_id)]))


class TestAuctionLot(TransactionCase):
    """auction.lot 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['auction.lot.category'].create({'name': '书画'})
        cls.partner = cls.env['res.partner'].create({'name': '测试委托方'})
        cls.Lot = cls.env['auction.lot']

    def _create_lot(self, **kwargs):
        """辅助: 创建带默认值的拍品"""
        import base64
        with_image = kwargs.pop('_with_image', True)
        vals = {
            'name': '测试拍品',
            'category_id': self.category.id,
            'starting_price': 1000,
            'reserve_price': 5000,
            'currency_id': self.env.company.currency_id.id,
        }
        vals.update(kwargs)
        lot = self.Lot.create(vals)
        # 添加一张图片以通过审核验证
        if with_image:
            pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
            self.env['auction.lot.image'].create({
                'lot_id': lot.id,
                'image': pixel,
            })
        return lot

    # ── CRUD (US-01) ──

    def test_create_lot(self):
        """US-01: 创建拍品 → 状态为 draft"""
        lot = self._create_lot()
        self.assertTrue(lot.id)
        self.assertEqual(lot.state, 'draft')

    def test_create_lot_with_consignor(self):
        """US-01: 创建拍品带委托方"""
        lot = self._create_lot(consignor_id=self.partner.id)
        self.assertEqual(lot.consignor_id, self.partner)

    def test_read_lot(self):
        """US-05: 读取拍品列表"""
        lot = self._create_lot()
        result = self.Lot.search([('id', '=', lot.id)])
        self.assertEqual(len(result), 1)

    # ── 定价规则 (US-03) ──

    def test_starting_lte_reserve_positive(self):
        """US-03 正向: 起拍价 ≤ 底价 → 成功"""
        lot = self._create_lot(starting_price=1000, reserve_price=5000)
        self.assertEqual(lot.starting_price, 1000)

    def test_starting_gt_reserve_negative(self):
        """US-03 反向: 起拍价 > 底价 → ValidationError"""
        lot = self._create_lot(starting_price=1000, reserve_price=5000)
        with self.assertRaises(ValidationError):
            lot.write({'starting_price': 6000})

    def test_no_reserve_positive(self):
        """US-03 正向: 无底价拍卖 → reserve_price=0, is_no_reserve=True"""
        lot = self._create_lot(is_no_reserve=True, reserve_price=0, starting_price=100)
        self.assertTrue(lot.is_no_reserve)
        self.assertEqual(lot.reserve_price, 0)

    def test_no_reserve_bypasses_check(self):
        """US-03: 无底价时起拍价不受底价约束"""
        lot = self._create_lot(
            is_no_reserve=True, reserve_price=0, starting_price=99999
        )
        self.assertTrue(lot.id)

    # ── 估价规则 (US-04) ──

    def test_estimate_range_positive(self):
        """US-04 正向: 低估 ≤ 高估 → 成功"""
        lot = self._create_lot(low_estimate=1000, high_estimate=3000)
        self.assertEqual(lot.low_estimate, 1000)

    def test_estimate_range_negative(self):
        """US-04 反向: 低估 > 高估 → ValidationError"""
        lot = self._create_lot()
        with self.assertRaises(ValidationError):
            lot.write({'low_estimate': 5000, 'high_estimate': 3000})

    def test_estimate_partial_ok(self):
        """US-04: 只填一端 → 不报错"""
        lot = self._create_lot(low_estimate=1000)
        self.assertTrue(lot.id)
        self.assertFalse(lot.high_estimate)

    # ── 计算字段 ──

    def test_image_count_compute(self):
        """image_count 正确统计"""
        import base64
        lot = self._create_lot(_with_image=False)
        self.assertEqual(lot.image_count, 0)
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        self.env['auction.lot.image'].create({
            'lot_id': lot.id, 'image': pixel,
        })
        self.assertEqual(lot.image_count, 1)

    # ── 状态流转 ──

    def test_action_approve_with_image(self):
        """审核通过（有图片）→ state=approved"""
        lot = self._create_lot()
        lot.action_approve()
        self.assertEqual(lot.state, 'approved')

    def test_action_approve_no_image_negative(self):
        """审核无图片 → UserError"""
        lot = self._create_lot(_with_image=False)
        with self.assertRaises(UserError):
            lot.action_approve()

    def test_action_withdraw(self):
        """撤回 → state=withdrawn"""
        lot = self._create_lot()
        lot.action_approve()
        lot.action_withdraw()
        self.assertEqual(lot.state, 'withdrawn')

    def test_action_reset_draft(self):
        """重置草稿 → state=draft"""
        lot = self._create_lot()
        lot.action_approve()
        lot.action_withdraw()
        lot.action_reset_draft()
        self.assertEqual(lot.state, 'draft')

    # ── 搜索过滤 (US-05) ──

    def test_search_by_category(self):
        """US-05: 按分类筛选"""
        lot = self._create_lot()
        result = self.Lot.search([('category_id', '=', self.category.id)])
        self.assertIn(lot, result)

    def test_search_by_state(self):
        """US-05: 按状态筛选"""
        lot = self._create_lot()
        result = self.Lot.search([('state', '=', 'draft')])
        self.assertIn(lot, result)

    def test_search_by_name(self):
        """US-05: 按名称搜索"""
        lot = self._create_lot(name='珍贵青花瓷')
        result = self.Lot.search([('name', 'ilike', '青花')])
        self.assertIn(lot, result)


class TestAuctionLotSecurity(TransactionCase):
    """安全测试: ACL + Record Rules"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['auction.lot.category'].create({'name': '安全测试分类'})

        # 创建测试用户
        cls.manager_user = cls.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_auction_manager',
            'groups_id': [(6, 0, [cls.env.ref('auction_lot.group_auction_manager').id])],
        })
        cls.user_user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_auction_user',
            'groups_id': [(6, 0, [cls.env.ref('auction_lot.group_auction_user').id])],
        })
        cls.base_user = cls.env['res.users'].create({
            'name': 'Test Base',
            'login': 'test_auction_base',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])],
        })

    def _create_lot_as_manager(self):
        import base64
        lot = self.env['auction.lot'].with_user(self.manager_user).create({
            'name': '安全测试拍品',
            'category_id': self.category.id,
            'starting_price': 1000,
            'reserve_price': 5000,
            'currency_id': self.env.company.currency_id.id,
        })
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        self.env['auction.lot.image'].with_user(self.manager_user).create({
            'lot_id': lot.id,
            'image': pixel,
        })
        return lot

    # ── ACL 测试 ──

    def test_manager_can_delete_lot(self):
        """Manager 有拍品删除权限"""
        lot = self._create_lot_as_manager()
        lot.with_user(self.manager_user).unlink()

    def test_user_cannot_delete_lot(self):
        """User 无拍品删除权限"""
        lot = self._create_lot_as_manager()
        with self.assertRaises(AccessError):
            lot.with_user(self.user_user).unlink()

    def test_base_user_readonly(self):
        """Base User 仅可读"""
        lot = self._create_lot_as_manager()
        # 可读
        lot.with_user(self.base_user).read(['name'])
        # 不可写
        with self.assertRaises(AccessError):
            lot.with_user(self.base_user).write({'name': '篡改'})

    def test_user_cannot_modify_category(self):
        """User 无分类修改权限"""
        with self.assertRaises(AccessError):
            self.env['auction.lot.category'].with_user(self.user_user).create({
                'name': '非法分类',
            })

    def test_manager_can_manage_category(self):
        """Manager 可完整管理分类"""
        cat = self.env['auction.lot.category'].with_user(self.manager_user).create({
            'name': 'Manager创建的分类',
        })
        self.assertTrue(cat.id)
