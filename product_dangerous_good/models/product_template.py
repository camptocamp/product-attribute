# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dangerous_class = fields.Many2one(
        comodel_name="product.dangerous.class",
        ondelete="restrict",
        string="Dangerous Class",
    )
    is_dangerous_good = fields.Boolean(
        help="This product belongs to dangerous class"
    )
    is_dangerous_waste = fields.Boolean(
        help="Waste of this product belongs to dangerous class"
    )
    dangerous_component_ids = fields.One2many('product.dangerous.component', 'product_template_id', string='')
