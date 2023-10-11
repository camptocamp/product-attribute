# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, models


class OrderMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order and sale.order models."""

    _name = "order.mixin"
    _description = "Order Mixin"

    def prepare_order_lines_with_deposit_container_values(
        self, deposit_container_qties
    ):
        values = []
        for package_level in deposit_container_qties:
            for product in deposit_container_qties[package_level]:
                product_uom_qty = deposit_container_qties[package_level][product]
                if product_uom_qty > 0:
                    values.append(
                        (
                            0,
                            0,
                            {
                                "name": product.name,
                                "product_id": product.id,
                                "product_uom_qty": deposit_container_qties[
                                    package_level
                                ][product],
                                "system_added": True,
                            },
                        )
                    )
        return values

    @api.depends("order_line.product_uom_qty", "order_line.product_packaging_id")
    def _compute_order_product_packaging_quantity(self):
        self.ensure_one()
        if self.state != "draft":
            return

        # Delete existing deposit lines (only the ones automatically added)
        system_added_lines = self.order_line.filtered(
            lambda order_line: order_line.system_added
        )
        system_added_lines.unlink()

        # Lines to compute container deposit
        lines_to_comp_deposit = self.order_line.filtered(
            lambda order_line: order_line.product_packaging_id.package_type_id.container_deposit
            or order_line.product_id.packaging_ids
        )
        deposit_container_qties = (
            lines_to_comp_deposit._get_order_lines_container_deposit_quantities()
        )
        order_line_vals = self.prepare_order_lines_with_deposit_container_values(
            deposit_container_qties
        )
        self.write({"order_line": order_line_vals})
