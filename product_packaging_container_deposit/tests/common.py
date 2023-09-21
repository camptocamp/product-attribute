# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from odoo import Command
from odoo.tests import common


class Common(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.ref("stock.group_tracking_lot").users = [Command.link(cls.env.user.id)]
        cls.package_type_pallet = cls.env.ref("stock.package_type_01")
        cls.package_type_box = cls.env.ref("stock.package_type_02")
        cls.package_type_pallet.container_deposit = cls.env["product.product"].create(
            {"name": "EUROPAL"}
        )
        cls.package_type_box.container_deposit = cls.env["product.product"].create(
            {"name": "Box"}
        )
        cls.product_packaging_level_pallet = cls.env["product.packaging.level"].create(
            {
                "name": "PALLET",
                "code": "PAL",
                "sequence": 1,
                "name_policy": "by_package_type",
            }
        )
        cls.product_packaging_level_box = cls.env["product.packaging.level"].create(
            {
                "name": "BOX",
                "code": "BOX",
                "sequence": 1,
                "name_policy": "by_package_type",
            }
        )
        cls.packaging = cls.env["product.packaging"].create(
            [
                {
                    "name": "Box of 12",
                    "qty": 12,
                    "package_type_id": cls.package_type_box.id,
                    "packaging_level_id": cls.product_packaging_level_box.id,
                },
                {
                    "name": "Box of 24",
                    "qty": 24,
                    "package_type_id": cls.package_type_box.id,
                    "packaging_level_id": cls.product_packaging_level_box.id,
                },
                {
                    "name": "EU pallet",
                    "qty": 240,
                    "package_type_id": cls.package_type_pallet.id,
                    "packaging_level_id": cls.product_packaging_level_pallet.id,
                },
            ]
        )

        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "packaging_ids": [(6, 0, cls.packaging.ids)]}
        )
