# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import random
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_default_code(self):
        return random.randint(100000000000,999999999999)

    default_code = fields.Char('Internal Reference', index=True, required=True,
                               default=_get_default_code)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_default_code(self):
        return random.randint(100000000000,999999999999)

    default_code = fields.Char('Internal Reference', index=True, required=True,
                               default=_get_default_code)
