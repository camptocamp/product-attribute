from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    classes_count = fields.Integer(
        string="Product Classes Count",
        compute="_compute_classes_count",
    )

    class_ids = fields.Many2many(
        comodel_name="product.class",
        relation="product_class_attribute_rel",
        column1="attribute_id",
        column2="product_class_id",
        string="Product Classes",
        help="Product classes that include this attribute",
    )

    @api.depends("class_ids")
    def _compute_classes_count(self):
        for attribute in self:
            attribute.classes_count = len(attribute.class_ids)

    def action_open_product_classes(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product_class.product_class_action"
        )
        action["domain"] = [("id", "in", self.class_ids.ids)]
        return action
