# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char('Internal Reference', index=True, required=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_default_code(self):
        return self.product_tmpl_id.default_code

    default_code = fields.Char('Internal Reference', index=True, required=True,
                               default=_get_default_code)
