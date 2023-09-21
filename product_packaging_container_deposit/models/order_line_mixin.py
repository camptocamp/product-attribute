# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class OrderLineMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order.line and sale.order.line models."""

    _name = "order.line.mixin"
    _description = "Order Line Mixin"

    system_added = fields.Boolean(
        default=False,
        help="""Line automaticaly added by the system. This lines are deleted and
        regenerated when product packaging quantity is recomputed""",
    )

    def _get_order_lines_container_deposit_quantities(self):
        """
        Returns a dict with quantity of product(container deposit)
        per package level for a set of lines
        {
            package_level: {
                container_deposit_product: quantity
                }
        }
        """

        def update_container_deposit_product_qties(line_deposit_qties):
            for plevel in line_deposit_qties:
                if deposit_product_qties[plevel].get(
                    line_deposit_qties[plevel][0], False
                ):
                    deposit_product_qties[plevel][
                        line_deposit_qties[plevel][0]
                    ] += line_deposit_qties[plevel][1]
                else:
                    deposit_product_qties[plevel][
                        line_deposit_qties[plevel][0]
                    ] = line_deposit_qties[plevel][1]

        deposit_product_qties = {
            package_level_id: {}
            for package_level_id in self.mapped(
                "product_id.packaging_ids.packaging_level_id"
            )
        }

        for line in self:
            line_deposit_qties = (
                line.product_id.get_product_container_deposit_quantities(
                    line.product_uom_qty, forced_packaging=line.product_packaging_id
                )
            )
            update_container_deposit_product_qties(line_deposit_qties)
        return deposit_product_qties
