# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models, fields


class ProductDangerousComponent(models.Model):
    _name = "product.dangerous.component"
    _description = "Product Dangerous Component"

    dangerous_product = fields.Many2one(comodel_name='product.dangerous.class', string='Dangerous product')
    weight = fields.Float(help="The weight of dangerous product in main product.")
    volume = fields.Float(help="The volume of dangerous product in main product.")
    dangerous_class = fields.Many2one(
        comodel_name="product.dangerous.class",
        ondelete="restrict",
        string="Dangerous Class",
    )
    product_template_id = fields.One2many('product.template', 'dangerous_component_ids', string='Product')
