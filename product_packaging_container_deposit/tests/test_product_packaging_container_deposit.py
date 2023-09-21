# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo.tests import common


class TestProductPackagingContainerDeposit(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.package_type_box = cls.env.ref("stock.package_type_02")
        cls.package_type_box.container_deposit = cls.env["product.product"].create(
            {"name": "Container Deposit Test"}
        )
        cls.packaging = cls.env["product.packaging"].create(
            {
                "name": "Packaging Test",
                "qty": 24.0,
                "package_type_id": cls.package_type_box.id,
            }
        )
        cls.product_packaging_level_default = cls.env.ref(
            "product_packaging_level.product_packaging_level_default"
        )

        cls.product = cls.env["product.product"].create(
            {"name": "Product Test", "packaging_ids": [(6, 0, cls.packaging.ids)]}
        )

    def test_product_container_deposit_quantities_per_packaging_level(self):
        packaging_qties = self.product.get_product_container_deposit_quantities(50)
        self.assertEqual(
            packaging_qties,
            {
                self.product_packaging_level_default: (
                    self.package_type_box.container_deposit,
                    2.0,
                )
            },
        )
