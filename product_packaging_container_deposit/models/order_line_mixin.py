# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class OrderLineMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order.line and sale.order.line models."""

    _name = "order.line.mixin"
    _description = "Order Line Mixin"

    is_container_deposit = fields.Boolean()

    def _get_product_qty_field(self):
        return (
            self._name == "sale.order.line"
            and "product_uom_qty"
            or self._name == "purchase.order.line"
            and "product_qty"
        )

    def _get_order_lines_container_deposit_quantities(self):
        """
        Returns a dict with quantity of container deposit {container_deposit_product: quantity}
        """
        deposit_product_qties = {}
        for line in self:
            line_deposit_qties = (
                line.product_id.get_product_container_deposit_quantities(
                    getattr(line, self._get_product_qty_field()),
                    forced_packaging=line.product_packaging_id,
                )
            )
            for plevel in line_deposit_qties:
                product = line_deposit_qties[plevel][0]
                qty = line_deposit_qties[plevel][1]
                if qty == 0:
                    continue
                if product in deposit_product_qties:
                    deposit_product_qties[product] += qty
                else:
                    deposit_product_qties[product] = qty
        return deposit_product_qties

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if not self.env.context.get("updating_product_packaging"):
            orders = lines.mapped("order_id")
            orders.update_order_product_packaging_quantity()
        return lines

    def write(self, vals):
        res = super().write(vals)
        # Context var to avoid recursive calls when updating product packaging
        if not self.env.context.get("updating_product_packaging"):
            self.order_id.update_order_product_packaging_quantity()
        return res
