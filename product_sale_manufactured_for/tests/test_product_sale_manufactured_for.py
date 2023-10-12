# Copyright 2023 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductSaleManufacturedFor(SavepointCase):
    def setUp(self):
        super().setUp()
        self.env = self.env(context=dict(self.env.context, tracking_disable=True))
        self.customer = self.env.ref("base.res_partner_4")
        self.product = self.env.ref("product.product_product_4")

    def test_archiving_customer(self):
        """Check archiving a customer cleans the product manufactured for field."""
        self.product.manufactured_for_partner_ids = [(4, self.customer.id, 0)]
        self.assertTrue(self.customer in self.product.manufactured_for_partner_ids)
        self.customer.active = False
        self.assertFalse(self.customer in self.product.manufactured_for_partner_ids)
