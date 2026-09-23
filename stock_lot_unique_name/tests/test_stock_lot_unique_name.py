# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestStockLotUniqueName(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Tracked product", "tracking": "serial"}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Other tracked product", "tracking": "serial"}
        )

    def _enable(self, value="True"):
        self.env["ir.config_parameter"].set_param(
            "stock_lot_unique_name.enabled", value
        )

    def _create_lot(self, name, product=None):
        return self.env["stock.lot"].create(
            {"name": name, "product_id": (product or self.product).id}
        )

    def test_disabled_by_default(self):
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000101")
        self.assertEqual(lot.name, "ABC0000101")

    def test_unparseable_value_reads_as_disabled(self):
        self._enable("maybe")
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000101")
        self.assertEqual(lot.name, "ABC0000101")

    def test_duplicate_across_products_is_refused(self):
        self._enable()
        self._create_lot("ABC0000101", product=self.other_product)
        with self.assertRaises(UserError):
            self._create_lot("ABC0000101")

    def test_same_name_on_the_same_product_is_left_to_odoo(self):
        self._enable()
        self._create_lot("ABC0000101")
        # core's _check_unique_lot owns this case
        with self.assertRaises(ValidationError):
            self._create_lot("ABC0000101")

    def test_distinct_names_are_allowed(self):
        self._enable()
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000102")
        self.assertEqual(lot.name, "ABC0000102")

    def test_batch_with_an_internal_duplicate_is_refused(self):
        self._enable()
        with self.assertRaises(UserError):
            self.env["stock.lot"].create(
                [
                    {"name": "ABC0000101", "product_id": self.product.id},
                    {"name": "ABC0000101", "product_id": self.other_product.id},
                ]
            )

    def test_rename_onto_another_product_name_is_refused(self):
        self._enable()
        self._create_lot("ABC0000101", product=self.other_product)
        lot = self._create_lot("ABC0000102")
        with self.assertRaises(UserError):
            lot.name = "ABC0000101"

    def test_rename_without_collision_is_allowed(self):
        self._enable()
        lot = self._create_lot("ABC0000101")
        lot.name = "ABC0000102"
        self.assertEqual(lot.name, "ABC0000102")
