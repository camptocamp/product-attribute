# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    packaging_multiple = fields.Boolean(
        related="company_id.packaging_multiple",
        readonly=False,
    )
