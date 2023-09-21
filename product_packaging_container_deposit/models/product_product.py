# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models


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
        self.ensure_one()
        pack_qties = {}
        if qty > 0:
            for pack in self.packaging_ids:
                container_deposit = pack.package_type_id.container_deposit
                plevel = pack.packaging_level_id
                if not container_deposit:
                    continue
                # Forced packaging ? Then ignore other packagings with the same level
                if (
                    forced_packaging
                    and forced_packaging != pack
                    and plevel == forced_packaging.packaging_level_id
                ):
                    continue
                new_pack_qty = qty // pack.qty
                # If there is multiple packagings with the same level we take the biggest one
                biggest_plevel_pack = (
                    plevel in pack_qties and pack_qties[plevel][1] > new_pack_qty
                )
                if forced_packaging or biggest_plevel_pack or plevel not in pack_qties:
                    pack_qties[pack.packaging_level_id] = (
                        container_deposit,
                        new_pack_qty,
                    )
        return pack_qties
