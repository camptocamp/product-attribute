# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import models


class OrderMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order and sale.order models."""

    _name = "order.mixin"
    _description = "Order Mixin"

    def prepare_deposit_container_line(self, product, qty):
        values = {
            "name": product.name,
            "product_id": product.id,
            "product_uom_qty": qty,
            "is_container_deposit": True,
            "order_id": self.id,
        }
        return values

    def update_order_product_packaging_quantity(self):
        self = self.with_context(updating_product_packaging=True)
        for order in self:
            # Lines to compute container deposit
            lines_to_comp_deposit = order.order_line.filtered(
                lambda line: line.product_packaging_id.package_type_id.container_deposit
                or line.product_id.packaging_ids
            )
            deposit_container_qties = (
                lines_to_comp_deposit._get_order_lines_container_deposit_quantities()
            )
            for line in self.order_line.filtered("is_container_deposit"):
                qty = deposit_container_qties.pop(line["product_id"], False)
                if not qty:
                    if order.state == "draft":
                        line.unlink()
                    else:
                        line.product_uom_qty = 0
                else:
                    line.product_uom_qty = qty
            values_lst = []
            for product in deposit_container_qties:

                if deposit_container_qties[product] > 0:
                    values = self.prepare_deposit_container_line(
                        product, deposit_container_qties[product]
                    )
                    values_lst.append(values)
            order.order_line.create(values_lst)
