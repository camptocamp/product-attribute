# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        res = super().write(vals)
        if vals.get("active") is False:
            query = (
                "DELETE FROM product_product_manuf_for_partner_rel "
                "WHERE partner_id IN (%s);"
            )
            self.env.cr.execute(query, (tuple(self.ids)))
        return res
