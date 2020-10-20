# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import _, api, exceptions, fields, models


class BarcodeRequiredMixin(models.AbstractModel):
    _name = "product.barcode.required.mixin"
    _description = "Barcode required mixin"

    is_barcode_required = fields.Boolean(compute="_compute_is_barcode_required")

    @api.onchange("default_code")
    def _onchange_code(self):
        for rec in self:
            if rec.is_barcode_required and rec.default_code:
                rec.barcode = rec.default_code

    @api.depends("type", "barcode")
    def _compute_is_barcode_required(self):
        for rec in self:
            rec.is_barcode_required = (
                rec._is_barcode_required_enabled() and rec._is_barcode_required()
            )

    def _is_barcode_required(self):
        self.ensure_one()
        return self.type != "service" and not self.barcode

    def _is_barcode_required_enabled(self):
        return self.env.company.product_variant_barcode_required

    def _check_barcode_required(self):
        # Make error nicer up to 30 records.
        failing = [x.name for x in self[:30] if x.is_barcode_required]
        if failing:
            failed_list = "\n  * " + "\n  * ".join(failing)
            raise exceptions.ValidationError(
                _("These products have no barcode:\n{}").format(failed_list)
            )
