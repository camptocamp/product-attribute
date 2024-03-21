# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestMargin(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "default_code": "pricelist-margin-product",
                "name": "Demo Margin Product",
                "list_price": 40.0,
                "standard_price": 20.0,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "pricelist",
            }
        )

    def test_margin_computation(self):

        line = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "compute_price": "fixed",
                "applied_on": "1_product",
                "fixed_price": 35,
            }
        )
        self.assertEqual(line.cost, 20.0)
        self.assertEqual(line.margin, (35 - 20))
        self.assertEqual(line.margin_percent, ((35 - 20) / 35) * 100)
