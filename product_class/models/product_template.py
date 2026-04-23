from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    class_id = fields.Many2one(
        comodel_name="product.class",
        string="Product Class",
        help="Product class that constrains which attributes can be used",
    )

    class_attribute_ids = fields.Many2many(
        related="class_id.attribute_ids",
        string="Class Attributes",
        help="Attributes allowed by the selected product class",
    )

    @api.constrains("class_id", "attribute_line_ids")
    def _check_class_attributes(self):
        """
        Ensure all attribute_line_ids belong to the selected class.
        """
        for product in self:
            if not product.class_id:
                continue

            class_attributes = product.class_id.attribute_ids
            invalid_attributes = (
                product.attribute_line_ids.attribute_id - class_attributes
            )

            if invalid_attributes:
                invalid_names = ", ".join(invalid_attributes.mapped("display_name"))
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
