# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    alternative_pricelist_policy = fields.Selection(
        selection=[
            ("use_lower_price", "Use lower price"),
            ("ignore", "Ignore alternatives"),
        ],
        default="use_lower_price",
        required=True,
    )

    def _compute_price(self, product, quantity, uom, date, currency):
        price = super(PricelistItem, self)._compute_price(
            product, quantity, uom, date, currency
        )
        if self.alternative_pricelist_policy == "ignore":
            return price

        if self.alternative_pricelist_policy == "use_lower_price":
            for alternative_pricelist in self.pricelist_id.alternative_pricelist_ids:
                alternative_price = alternative_pricelist._get_product_price(
                    product, quantity, uom, date
                )
                if alternative_price < price:
                    price = alternative_price
        return price
