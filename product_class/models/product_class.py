from odoo import fields, models


class ProductClass(models.Model):
    _name = "product.class"
    _description = "Product Class"
    _order = "name"

    _name_uniq = models.Constraint(
        "unique(name)",
        "A product class with this name already exists.",
    )

    name = fields.Char()
    attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        relation="product_class_attribute_rel",
        column1="product_class_id",
        column2="attribute_id",
        string="Attributes",
        help="Allowed attributes for products of this class",
    )
