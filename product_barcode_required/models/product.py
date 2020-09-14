# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import _, api, exceptions, models


class BarcodeRequiredMixin(models.AbstractModel):
    _name = "product.barcode.required.mixin"
    _description = "Barcode required mixin"

    @api.onchange("default_code")
    def _onchange_code(self):
        for rec in self:
            if rec._is_barcode_required_enabled() and rec._is_barcode_required():
                rec.barcode = rec.default_code

    def _is_barcode_required(self):
        self.ensure_one()
        return self.type != "service" and not self.barcode and self.default_code

    def _is_barcode_required_enabled(self):
        return self.env.company.product_variant_barcode_required


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.barcode.required.mixin"]


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.barcode.required.mixin"]

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec._check_barcode_required()
        return rec

    def write(self, vals):
        res = super().write(vals)
        self._check_barcode_required()
        return res

    def _check_barcode_required(self):
        for rec in self:
            if rec._is_barcode_required_enabled() and rec._is_barcode_required():
                raise exceptions.ValidationError(
                    _("Product '{0.name}' has no barcode!").format(rec)
                )
