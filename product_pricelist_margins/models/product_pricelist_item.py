# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    cost = fields.Float(
        related="product_tmpl_id.standard_price",
        digits="Product Price",
    )
    margin = fields.Float(
        compute="_compute_margin",
        digits="Product Price",
    )
    margin_percent = fields.Float(
        string="Margin (%)",
        compute="_compute_margin",
    )

    @api.depends(
        "compute_price",
        "applied_on",
        "percent_price",
        "base",
        "price_discount",
        "price_surcharge",
        "price_round",
        "price_min_margin",
        "product_tmpl_id",
        "cost",
        "min_quantity",
    )
    def _compute_margin(self):
        for item in self.filtered(
            lambda x: x.applied_on in ("1_product", "0_product_variant")
        ):
            margin = percentage = 0

            price_rule = item.pricelist_id._compute_price_rule(
                item.product_tmpl_id, item.min_quantity
            )

            price = price_rule.get(item.product_tmpl_id.id, [0])[0]

            if not float_is_zero(price, precision_digits=item.currency_id.rounding):
                res = item.product_tmpl_id.taxes_id.compute_all(
                    price,
                    item.currency_id,
                    product=item.product_tmpl_id,
                )

                price_vat_excl = res["total_excluded"]

                cost = self.env.user.company_id.currency_id.compute(
                    item.cost, item.currency_id
                )

                margin = price_vat_excl - cost
                percentage = price_vat_excl and (margin / price_vat_excl) * 100

            item.margin = margin
            item.margin_percent = percentage

        for item in self.filtered(
            lambda x: x.applied_on not in ("1_product", "0_product_variant")
        ):
            item.margin = 0
            item.margin_percent = 0
