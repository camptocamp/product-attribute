# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    uom_id = fields.Many2one(
        string="Packaging",
        comodel_name="uom.uom",
        help="Restrict this rule to a specific packaging of the product. "
        "When empty, the rule applies to the product base unit of measure.",
    )
    allowed_uom_ids = fields.Many2many("uom.uom", compute="_compute_allowed_uom_ids")

    @api.depends("product_tmpl_id", "product_tmpl_id.uom_id", "product_tmpl_id.uom_ids")
    def _compute_allowed_uom_ids(self):
        for item in self:
            item.allowed_uom_ids = (
                item.product_tmpl_id.uom_id | item.product_tmpl_id.uom_ids
            )

    @api.model_create_multi
    def create(self, vals_list):
        items = super().create(vals_list)
        items.filtered(
            lambda item: item.applied_on == "2_product_category"
        ).uom_id = False
        return items

    def write(self, vals):
        if vals.get("applied_on") == "2_product_category":
            vals["uom_id"] = False
        return super().write(vals)

    def _is_applicable_for(
        self, product, quantity, *, uom=None, qty_in_product_uom=False, **kwargs
    ):
        self.ensure_one()
        product.ensure_one()
        product_uom = product.uom_id
        uom = uom or product_uom
        if self.uom_id and uom != self.uom_id:
            return False
        qty_to_consider = quantity
        if uom not in product_uom + self.uom_id:
            # The requested UoM is not one of the UoMs the rule is expressed in,
            # so the quantity has to be converted to the product base UoM.
            qty_to_consider = uom._compute_quantity(quantity, product_uom)

        return super()._is_applicable_for(product, qty_to_consider)
