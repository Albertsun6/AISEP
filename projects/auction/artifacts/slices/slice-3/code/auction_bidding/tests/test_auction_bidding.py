import base64
from datetime import datetime, timedelta

from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError, UserError


class TestAuctionBiddingRound(TransactionCase):
    """auction.bidding.round 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # 创建拍品
        cls.category = cls.env['auction.lot.category'].create({'name': '竞价测试分类'})
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)

        cls.lot = cls.env['auction.lot'].create({
            'name': '竞价测试拍品',
            'category_id': cls.category.id,
            'starting_price': 1000,
            'reserve_price': 10000,
            'currency_id': cls.env.company.currency_id.id,
        })
        cls.env['auction.lot.image'].create({
            'lot_id': cls.lot.id,
            'image': pixel,
        })
        cls.lot.action_approve()

        # 无底价拍品
        cls.lot_no_reserve = cls.env['auction.lot'].create({
            'name': '无底价拍品',
            'category_id': cls.category.id,
            'starting_price': 500,
            'is_no_reserve': True,
            'currency_id': cls.env.company.currency_id.id,
        })
        cls.env['auction.lot.image'].create({
            'lot_id': cls.lot_no_reserve.id,
            'image': pixel,
        })
        cls.lot_no_reserve.action_approve()

        # 创建场次
        now = datetime.now()
        cls.session = cls.env['auction.session'].create({
            'name': '竞价测试场次',
            'start_time': now + timedelta(days=1),
            'end_time': now + timedelta(days=2),
            'default_increment': 500,
            'conditional_sale_pct': 80.0,
            'currency_id': cls.env.company.currency_id.id,
        })

        # 编入拍品
        cls.session_lot = cls.env['auction.session.lot'].create({
            'session_id': cls.session.id,
            'lot_id': cls.lot.id,
        })
        cls.session_lot_nr = cls.env['auction.session.lot'].create({
            'session_id': cls.session.id,
            'lot_id': cls.lot_no_reserve.id,
        })

        # 竞拍者
        cls.bidder_1 = cls.env['res.partner'].create({'name': '竞拍者A'})
        cls.bidder_2 = cls.env['res.partner'].create({'name': '竞拍者B'})

    def _create_round(self, session_lot=None, **kwargs):
        """辅助: 创建竞价轮次"""
        sl = session_lot or self.session_lot
        vals = {
            'session_lot_id': sl.id,
            'starting_price': sl.lot_id.starting_price,
            'bid_increment': self.session.default_increment,
            'currency_id': self.env.company.currency_id.id,
        }
        vals.update(kwargs)
        return self.env['auction.bidding.round'].create(vals)

    # ── 创建和基本状态 (US-10) ──

    def test_create_round(self):
        """US-10: 创建竞价轮次 → 状态为 open"""
        rnd = self._create_round()
        self.assertEqual(rnd.state, 'open')
        self.assertEqual(rnd.lot_id, self.lot)
        self.assertEqual(rnd.session_id, self.session)

    def test_related_fields(self):
        """related 字段正确解析"""
        rnd = self._create_round()
        self.assertEqual(rnd.lot_id.id, self.lot.id)
        self.assertEqual(rnd.session_id.id, self.session.id)

    # ── 出价 (US-11) ──

    def test_place_bid_first(self):
        """US-11: 首次出价 >= starting_price"""
        rnd = self._create_round()
        bid = rnd.place_bid(self.bidder_1.id, 1000)
        self.assertTrue(bid.id)
        self.assertEqual(rnd.current_price, 1000)
        self.assertEqual(rnd.bid_count, 1)

    def test_place_bid_increment(self):
        """US-11: 后续出价 >= current_price + increment"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 1000)
        rnd.place_bid(self.bidder_2.id, 1500)
        self.assertEqual(rnd.current_price, 1500)
        self.assertEqual(rnd.bid_count, 2)

    def test_place_bid_too_low(self):
        """US-11 反向: 出价低于最低要求"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 1000)
        with self.assertRaises(UserError):
            rnd.place_bid(self.bidder_2.id, 1200)  # 需要 >= 1500

    def test_place_bid_closed_round(self):
        """US-11 反向: 竞价已结束"""
        rnd = self._create_round()
        rnd.state = 'hammer'
        with self.assertRaises(UserError):
            rnd.place_bid(self.bidder_1.id, 1000)

    # ── 落槌判定 (US-12) ──

    def test_hammer_above_reserve(self):
        """US-12: 最高价 >= 底价 → hammer"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 10000)
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'hammer')
        self.assertEqual(rnd.winner_id, self.bidder_1)
        self.assertEqual(rnd.hammer_price, 10000)

    def test_hammer_no_bids(self):
        """US-12: 无出价 → unsold"""
        rnd = self._create_round()
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'unsold')

    def test_hammer_below_threshold(self):
        """US-12: 最高价 < 阈值 → unsold"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 5000)  # 10000 * 80% = 8000, 5000 < 8000
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'unsold')

    def test_hammer_conditional(self):
        """US-12: 阈值 <= 最高价 < 底价 → conditional_pending"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 8000)  # 8000 >= 10000*80% 但 < 10000
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'conditional_pending')

    def test_hammer_no_reserve_lot(self):
        """US-12: 无底价拍品 → 直接成交"""
        rnd = self._create_round(session_lot=self.session_lot_nr,
                                 starting_price=500)
        rnd.place_bid(self.bidder_1.id, 500)
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'hammer')

    # ── 有条件成交 (US-13) ──

    def test_accept_conditional(self):
        """US-13: 委托方确认 → conditional_accepted"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 8000)
        rnd.action_check_hammer()
        self.assertEqual(rnd.state, 'conditional_pending')
        rnd.action_accept_conditional()
        self.assertEqual(rnd.state, 'conditional_accepted')
        self.assertEqual(rnd.winner_id, self.bidder_1)

    def test_reject_conditional(self):
        """US-13: 委托方拒绝 → conditional_rejected"""
        rnd = self._create_round()
        rnd.place_bid(self.bidder_1.id, 8000)
        rnd.action_check_hammer()
        rnd.action_reject_conditional()
        self.assertEqual(rnd.state, 'conditional_rejected')

    def test_accept_wrong_state(self):
        """US-13 反向: 非 conditional_pending → UserError"""
        rnd = self._create_round()
        with self.assertRaises(UserError):
            rnd.action_accept_conditional()

    # ── 出价次数计算 ──

    def test_bid_count(self):
        """bid_count 正确计算"""
        rnd = self._create_round()
        self.assertEqual(rnd.bid_count, 0)
        rnd.place_bid(self.bidder_1.id, 1000)
        self.assertEqual(rnd.bid_count, 1)
        rnd.place_bid(self.bidder_2.id, 1500)
        self.assertEqual(rnd.bid_count, 2)

    # ── 搜索 (US-14) ──

    def test_search_by_state(self):
        """US-14: 按状态筛选"""
        rnd = self._create_round()
        result = self.env['auction.bidding.round'].search([('state', '=', 'open')])
        self.assertIn(rnd, result)


class TestAuctionBid(TransactionCase):
    """auction.bid 单元测试"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = cls.env['auction.lot.category'].create({'name': 'bid测试分类'})
        pixel = base64.b64encode(b'\x89PNG\r\n\x1a\n' + b'\x00' * 50)
        cls.lot = cls.env['auction.lot'].create({
            'name': 'bid测试拍品',
            'category_id': cls.category.id,
            'starting_price': 1000,
            'reserve_price': 10000,
            'currency_id': cls.env.company.currency_id.id,
        })
        cls.env['auction.lot.image'].create({
            'lot_id': cls.lot.id,
            'image': pixel,
        })
        cls.lot.action_approve()

        now = datetime.now()
        cls.session = cls.env['auction.session'].create({
            'name': 'bid测试场次',
            'start_time': now + timedelta(days=1),
            'end_time': now + timedelta(days=2),
            'default_increment': 500,
            'currency_id': cls.env.company.currency_id.id,
        })
        cls.session_lot = cls.env['auction.session.lot'].create({
            'session_id': cls.session.id,
            'lot_id': cls.lot.id,
        })
        cls.bidder = cls.env['res.partner'].create({'name': 'bid测试竞拍者'})

    def _create_round_with_bid(self):
        rnd = self.env['auction.bidding.round'].create({
            'session_lot_id': self.session_lot.id,
            'starting_price': 1000,
            'bid_increment': 500,
            'currency_id': self.env.company.currency_id.id,
        })
        bid = rnd.place_bid(self.bidder.id, 1000)
        return rnd, bid

    def test_bid_immutable_write(self):
        """业务铁律: 出价记录不可修改"""
        _, bid = self._create_round_with_bid()
        with self.assertRaises(UserError):
            bid.write({'amount': 9999})

    def test_bid_immutable_unlink(self):
        """业务铁律: 出价记录不可删除"""
        _, bid = self._create_round_with_bid()
        with self.assertRaises(UserError):
            bid.unlink()

    def test_bid_is_winning(self):
        """is_winning 正确计算"""
        rnd, bid = self._create_round_with_bid()
        self.assertTrue(bid.is_winning)
        # 更高出价后，旧 bid 不再是 winning
        bidder_2 = self.env['res.partner'].create({'name': 'bid2'})
        bid2 = rnd.place_bid(bidder_2.id, 1500)
        bid.invalidate_recordset()
        self.assertFalse(bid.is_winning)
        self.assertTrue(bid2.is_winning)

    def test_amount_positive_constraint(self):
        """SQL 约束: 金额必须 > 0"""
        rnd = self.env['auction.bidding.round'].create({
            'session_lot_id': self.session_lot.id,
            'starting_price': 1000,
            'bid_increment': 500,
            'currency_id': self.env.company.currency_id.id,
        })
        with self.assertRaises(Exception):
            with self.env.cr.savepoint():
                self.env['auction.bid'].create({
                    'round_id': rnd.id,
                    'bidder_id': self.bidder.id,
                    'amount': -100,
                    'currency_id': self.env.company.currency_id.id,
                })

    def test_bid_time_default(self):
        """bid_time 默认为当前时间"""
        _, bid = self._create_round_with_bid()
        self.assertTrue(bid.bid_time)
