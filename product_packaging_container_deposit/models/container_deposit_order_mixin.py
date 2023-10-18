# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class OrderMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order and sale.order models."""

    _name = "container.deposit.order.mixin"
    _description = "Container Deposit Order Mixin"

    def prepare_deposit_container_line(self, product, qty):
        self.ensure_one()
        values = {
            "name": product.name,
            "product_id": product.id,
            self.order_line._get_product_qty_field(): qty,
            "is_container_deposit": True,
            "order_id": self.id,
        }
        return values

    def _get_order_line_field(self):
        raise NotImplementedError()

    def update_order_container_deposit_quantity(self):
        self = self.with_context(updating_container_deposit=True)
        for order in self:
            # Lines to compute container deposit
            lines_to_comp_deposit = order[self._get_order_line_field()].filtered(
                lambda line: line.product_packaging_id.package_type_id.container_deposit
                or line.product_id.packaging_ids
            )
            deposit_container_qties = (
                lines_to_comp_deposit._get_order_lines_container_deposit_quantities()
            )
            for line in self[self._get_order_line_field()]:
                if not line.is_container_deposit:
                    continue
                qty = deposit_container_qties.pop(line["product_id"], False)
                if not qty:
                    if order.state == "draft":
                        line.unlink()
                    else:
                        line.write({line._get_product_qty_field(): 0})
                else:
                    line.write({line._get_product_qty_field(): qty})
            values_lst = []
            for product in deposit_container_qties:

                if deposit_container_qties[product] > 0:
                    values = order.prepare_deposit_container_line(
                        product, deposit_container_qties[product]
                    )
                    values_lst.append(values)
            order[self._get_order_line_field()].create(values_lst)
