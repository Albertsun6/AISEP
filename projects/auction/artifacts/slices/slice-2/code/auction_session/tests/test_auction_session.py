from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class TestAuctionSession(TransactionCase):
    """auction.session 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Session = cls.env['auction.session']
        cls.category = cls.env['auction.lot.category'].create({'name': '测试分类'})
        cls.lot_1 = cls.env['auction.lot'].create({
            'name': '测试拍品1',
            'category_id': cls.category.id,
            'starting_price': 1000,
            'reserve_price': 5000,
            'currency_id': cls.env.company.currency_id.id,
        })
        cls.lot_2 = cls.env['auction.lot'].create({
            'name': '测试拍品2',
            'category_id': cls.category.id,
            'starting_price': 2000,
            'reserve_price': 8000,
            'currency_id': cls.env.company.currency_id.id,
        })
        # 先审核拍品（action_approve 需要图片）
        import base64
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        for lot in (cls.lot_1, cls.lot_2):
            cls.env['auction.lot.image'].create({
                'lot_id': lot.id,
                'image': pixel,
            })
            lot.action_approve()

    def _create_session(self, **kwargs):
        """辅助: 创建带默认值的拍卖会"""
        now = datetime.now()
        vals = {
            'name': '测试拍卖会',
            'start_time': now + timedelta(days=1),
            'end_time': now + timedelta(days=2),
            'default_increment': 100,
            'currency_id': self.env.company.currency_id.id,
        }
        vals.update(kwargs)
        return self.Session.create(vals)

    # ── CRUD (US-06) ──

    def test_create_session(self):
        """US-06: 创建拍卖会 → 状态为 draft"""
        session = self._create_session()
        self.assertTrue(session.id)
        self.assertEqual(session.state, 'draft')

    def test_create_session_with_rules(self):
        """US-06: 创建拍卖会带规则配置"""
        session = self._create_session(
            countdown_seconds=60,
            extension_seconds=15,
            conditional_sale_pct=75.0,
        )
        self.assertEqual(session.countdown_seconds, 60)
        self.assertEqual(session.extension_seconds, 15)
        self.assertEqual(session.conditional_sale_pct, 75.0)

    def test_read_session(self):
        """US-09: 读取拍卖会"""
        session = self._create_session()
        result = self.Session.search([('id', '=', session.id)])
        self.assertEqual(len(result), 1)

    # ── 时间约束 (US-06) ──

    def test_time_constraint_positive(self):
        """US-06 正向: start < end → 成功"""
        session = self._create_session()
        self.assertTrue(session.start_time < session.end_time)

    def test_time_constraint_negative(self):
        """US-06 反向: start >= end → 约束报错"""
        now = datetime.now()
        session = self._create_session()
        with self.assertRaises(Exception):
            with self.env.cr.savepoint():
                session.write({
                    'start_time': now + timedelta(days=2),
                    'end_time': now + timedelta(days=1),
                })

    # ── 阈值约束 (US-08) ──

    def test_threshold_constraint_positive(self):
        """US-08 正向: 阈值在 0-100 → 成功"""
        session = self._create_session(conditional_sale_pct=80.0)
        self.assertEqual(session.conditional_sale_pct, 80.0)

    def test_threshold_constraint_negative(self):
        """US-08 反向: 阈值 > 100 → 约束报错"""
        session = self._create_session()
        with self.assertRaises(Exception):
            with self.env.cr.savepoint():
                session.write({'conditional_sale_pct': 150.0})

    # ── 拍品编排 (US-07) ──

    def test_add_lot_to_session(self):
        """US-07: 编入拍品 → session_lot_ids 增加"""
        session = self._create_session()
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        self.assertEqual(session.lot_count, 1)

    def test_lot_sequence_ordering(self):
        """US-07: 拍品排序"""
        session = self._create_session()
        sl1 = self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
            'sequence': 20,
        })
        sl2 = self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_2.id,
            'sequence': 10,
        })
        session.invalidate_recordset()
        lots = session.session_lot_ids
        self.assertEqual(lots[0], sl2)  # sequence=10 在前
        self.assertEqual(lots[1], sl1)  # sequence=20 在后


    def test_lot_count_compute(self):
        """lot_count 正确计算"""
        session = self._create_session()
        self.assertEqual(session.lot_count, 0)
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        self.assertEqual(session.lot_count, 1)

    # ── 状态流转 ──

    def test_publish_with_lots(self):
        """发布拍卖会（有拍品）→ published"""
        session = self._create_session()
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        session.action_publish()
        self.assertEqual(session.state, 'published')

    def test_publish_without_lots_negative(self):
        """发布无拍品 → UserError"""
        session = self._create_session()
        with self.assertRaises(UserError):
            session.action_publish()

    def test_start_session(self):
        """开始 → ongoing"""
        session = self._create_session()
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        session.action_publish()
        session.action_start()
        self.assertEqual(session.state, 'ongoing')

    def test_close_session(self):
        """结束 → closed"""
        session = self._create_session()
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        session.action_publish()
        session.action_start()
        session.action_close()
        self.assertEqual(session.state, 'closed')

    def test_cancel_draft(self):
        """取消草稿 → cancelled"""
        session = self._create_session()
        session.action_cancel()
        self.assertEqual(session.state, 'cancelled')

    def test_cancel_ongoing_negative(self):
        """进行中 → 取消 → UserError"""
        session = self._create_session()
        self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot_1.id,
        })
        session.action_publish()
        session.action_start()
        with self.assertRaises(UserError):
            session.action_cancel()

    # ── 搜索过滤 (US-09) ──

    def test_search_by_state(self):
        """US-09: 按状态筛选"""
        session = self._create_session()
        result = self.Session.search([('state', '=', 'draft')])
        self.assertIn(session, result)


class TestAuctionSessionLot(TransactionCase):
    """auction.session.lot 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['auction.lot.category'].create({'name': '约束测试分类'})
        cls.lot = cls.env['auction.lot'].create({
            'name': '约束测试拍品',
            'category_id': cls.category.id,
            'starting_price': 1000,
            'reserve_price': 5000,
            'currency_id': cls.env.company.currency_id.id,
        })
        import base64
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        cls.env['auction.lot.image'].create({
            'lot_id': cls.lot.id,
            'image': pixel,
        })
        cls.lot.action_approve()

    def _create_session(self, **kwargs):
        now = datetime.now()
        vals = {
            'name': '约束测试场次',
            'start_time': now + timedelta(days=1),
            'end_time': now + timedelta(days=2),
            'default_increment': 100,
            'currency_id': self.env.company.currency_id.id,
        }
        vals.update(kwargs)
        return self.env['auction.session'].create(vals)

    def test_lot_unique_active_session(self):
        """US-07: 同一拍品不可同时在多场活跃拍卖会中"""
        session_1 = self._create_session(name='场次A')
        session_2 = self._create_session(name='场次B')
        self.env['auction.session.lot'].create({
            'session_id': session_1.id,
            'lot_id': self.lot.id,
        })
        with self.assertRaises(ValidationError):
            self.env['auction.session.lot'].create({
                'session_id': session_2.id,
                'lot_id': self.lot.id,
            })

    def test_lot_in_closed_session_can_reassign(self):
        """已结束场次的拍品可以编入新场次"""
        session_1 = self._create_session(name='旧场次')
        self.env['auction.session.lot'].create({
            'session_id': session_1.id,
            'lot_id': self.lot.id,
        })
        session_1.action_publish()
        session_1.action_start()
        session_1.action_close()

        session_2 = self._create_session(name='新场次')
        sl = self.env['auction.session.lot'].create({
            'session_id': session_2.id,
            'lot_id': self.lot.id,
        })
        self.assertTrue(sl.id)

    def test_default_lot_state(self):
        """编入拍品后默认状态为 pending"""
        session = self._create_session()
        sl = self.env['auction.session.lot'].create({
            'session_id': session.id,
            'lot_id': self.lot.id,
        })
        self.assertEqual(sl.lot_state, 'pending')
