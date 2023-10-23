# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    purchases = fields.Boolean(
        compute="_compute_purchases",
        readonly=False,
        store=True,
        default=None,
        help="If true, the packaging can be used for purchase orders",
    )

    @api.depends("packaging_level_id")
    def _compute_purchases(self):
        for record in self:
            record.purchases = record.packaging_level_id.can_be_purchased
