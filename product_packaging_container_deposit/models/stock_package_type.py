# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class PackageType(models.Model):
    _inherit = "stock.package.type"

    container_deposit = fields.Many2one("product.product")
