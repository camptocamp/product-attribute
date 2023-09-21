# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models
from odoo.tools import groupby


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_product_container_deposit_quantities(self, qty, forced_packaging=False):
        """
        Returns the quantity of deposit per packaging level for a given product quantity
        {
            "PL1": (CP1, QTY),
            "PLn": (CPn, QTYn)
        }
        """

        def get_sort_key(packaging):
            return (
                packaging.packaging_level_id,
                packaging != forced_packaging,
                packaging.qty < qty,
                -packaging.qty,
            )

        self.ensure_one()
        pack_qties = {}
        if qty > 0:
            # Sort by forced_packaging, fitting packagings, biggest packaging
            packagings = self.packaging_ids.sorted(key=get_sort_key)
            for plevel, packs in groupby(packagings, lambda p: p.packaging_level_id):
                pack_qties[plevel] = (
                    packs[0].package_type_id.container_deposit,
                    qty // packs[0].qty,
                )
        return pack_qties
