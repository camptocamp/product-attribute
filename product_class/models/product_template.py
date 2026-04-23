from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    class_id = fields.Many2one(
        comodel_name="product.class",
        string="Product Class",
        help="Product class that constrains which attributes can be used",
    )

    attribute_line_ids = fields.One2many(
        "product.template.attribute.line",
        domain="[('attribute_id', 'in', class_id.attribute_ids.ids)]",
    )

    @api.constrains("class_id", "attribute_line_ids")
    def _check_class_attributes(self):
        """
        Ensure all attribute_line_ids belong to the selected class.
        """
        for product in self:
            if not product.class_id:
                continue

            class_attribute_ids = product.class_id.attribute_ids.ids
            invalid_lines = [
                line
                for line in product.attribute_line_ids
                if line.attribute_id.id not in class_attribute_ids
            ]

            if invalid_lines:
                invalid_names = ", ".join([line.display_name for line in invalid_lines])
                raise ValidationError(
                    self.env._(
                        "Product '%(product)s' has attribute lines that do not belong "
                        "to the selected class '%(product_class)s': %(attrs)s. "
                        "Please remove these attributes or change the product class.",
                        product=product.name,
                        product_class=product.class_id.name,
                        attrs=invalid_names,
                    )
                )
