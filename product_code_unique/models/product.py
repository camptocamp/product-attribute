# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char('Internal Reference', index=True)

    _sql_constraints = [
        ('product_template_default_code_uniq', 'unique(default_code)',
            'Internal Reference must be unique across the database!')]


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', index=True)

    _sql_constraints = [
        ('product_product_default_code_uniq', 'unique(default_code)',
            'Internal Reference must be unique across the database!')]
