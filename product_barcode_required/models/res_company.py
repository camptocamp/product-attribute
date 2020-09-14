# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    product_variant_barcode_required = fields.Boolean(
        help="Make variant barcode required", groups="product.group_product_variant"
    )
