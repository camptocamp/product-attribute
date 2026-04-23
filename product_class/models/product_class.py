from odoo import api, fields, models
from odoo.exceptions import ValidationError


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

    @api.constrains("attribute_ids")
    def _check_attribute_ids_used_by_products(self):
        for product_class in self:
            invalid_lines = self.env["product.template.attribute.line"].search(
                [
                    ("product_tmpl_id.class_id", "=", product_class.id),
                    ("attribute_id", "not in", product_class.attribute_ids.ids),
                ]
            )
            if not invalid_lines:
                continue

            invalid_names = ", ".join(
                sorted(set(invalid_lines.mapped("attribute_id.display_name")))
            )
            raise ValidationError(
                self.env._(
                    "Cannot remove attributes used in products assigned to class "
                    "'%(product_class)s': %(attrs)s. Please remove these attributes "
                    "or change the product class.",
                    product_class=product_class.name,
                    attrs=invalid_names,
                )
            )
