# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import api, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.barcode.required.mixin"]

    @api.model_create_multi
    def create(self, vals_list):
        return super(
            ProductTemplate, self.with_context(_bypass_barcode_required_check=True)
        ).create(vals_list)

    def write(self, vals):
        return super(
            ProductTemplate, self.with_context(_bypass_barcode_required_check=True)
        ).write(vals)
