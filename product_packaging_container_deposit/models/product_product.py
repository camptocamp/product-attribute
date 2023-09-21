# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_product_container_deposit_quantities(self, qty):
        """
        Returns the quantity of deposit per packaging level for a given product quantity
        {
            "PL1": (CP1, QTY),
            "PLn": (CPn, QTYn)
        }
        """
        self.ensure_one()
        packaging_quantities = {}
        if qty > 0:
            for packaging in self.packaging_ids:
                container_deposit = packaging.package_type_id.container_deposit
                if not container_deposit:
                    continue
                # If there iss multiple packagings with the same level we take the biggest one
                if (
                    packaging.packaging_level_id in packaging_quantities
                    and qty // packaging.qty
                    < packaging_quantities[packaging.packaging_level_id][1]
                    or packaging.packaging_level_id not in packaging_quantities
                ):
                    packaging_quantities[packaging.packaging_level_id] = (
                        container_deposit,
                        qty // packaging.qty,
                    )
        return packaging_quantities
