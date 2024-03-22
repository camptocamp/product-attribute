# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    alternative_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Alternative pricelists",
        relation="product_pricelist_alternative_rel",
        column1="origin_id",
        column2="alternative_id",
        domain="[('id', '!=', id)]",
    )
    is_alternative_to_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Is alternative to pricelists",
        relation="product_pricelist_alternative_rel",
        column1="alternative_id",
        column2="origin_id",
    )
    is_alternative_to_pricelist_count = fields.Integer(
        compute="_compute_is_alternative_to_pricelist_count"
    )

    @api.depends("is_alternative_to_pricelist_ids")
    def _compute_is_alternative_to_pricelist_count(self):
        for pricelist in self:
            pricelist.is_alternative_to_pricelist_count = len(
                pricelist.is_alternative_to_pricelist_ids
            )

    def action_view_is_alternative_to_pricelist(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": _("Is Alternative to Pricelist"),
            "res_model": "product.pricelist",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.is_alternative_to_pricelist_ids.ids)],
            "context": dict(self.env.context, create=False),
        }
        if self.is_alternative_to_pricelist_count == 1:
            action.update(
                {"view_mode": "form", "res_id": self.is_alternative_to_pricelist_ids.id}
            )
        return action
