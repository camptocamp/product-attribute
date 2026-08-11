# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.fields import Domain


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(
        self,
        products,
        quantity,
        *,
        currency=None,
        uom=None,
        date=False,
        compute_price=True,
        **kwargs,
    ):
        self and self.ensure_one()
        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()
        if not products:
            return {}
        if not date:
            date = fields.Datetime.now()
        rules = self._get_applicable_rules(
            products, date, quantity=quantity, uom=uom, **kwargs
        )
        results = {}
        for product in products:
            suitable_rule = self.env["product.pricelist.item"]
            target_uom = uom or product.uom_id
            for rule in rules:
                if rule._is_applicable_for(product, quantity, uom=target_uom, **kwargs):
                    suitable_rule = rule
                    break
            if compute_price:
                price = suitable_rule._compute_price(
                    product,
                    quantity,
                    target_uom,
                    date=date,
                    currency=currency,
                    **kwargs,
                )
            else:
                price = 0.0
            results[product.id] = (price, suitable_rule.id)
        return results

    def _get_applicable_rules_domain(
        self, products, date, *, quantity=None, uom=None, **kwargs
    ):
        domain = Domain(super()._get_applicable_rules_domain(products, date, **kwargs))
        if uom:
            domain &= Domain("uom_id", "=", False) | Domain("uom_id", "=", uom.id)
        elif quantity:
            domain &= Domain("min_quantity", "=", 0) | Domain(
                "min_quantity", "<=", quantity
            )
        return domain

    def _get_related_uoms(self, product):
        """Return the packagings having their own rule in this pricelist.

        :param product: product template or product variant record.
        :return: UoMs defined on the matching pricelist items.
        :rtype: uom.uom
        """
        domain = self._get_applicable_rules_domain(
            product, fields.Datetime.now()
        ) & Domain("uom_id", "!=", False)
        return (
            self.env["product.pricelist.item"].search_fetch(domain, ["uom_id"]).uom_id
        )
