# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Edits the single variant's packaging (only meaningful, and only shown,
    # when the template has exactly one variant).
    packaging_ids = fields.One2many(
        comodel_name="product.packaging",
        compute="_compute_packaging_ids",
        inverse="_inverse_packaging_ids",
        string="Packaging",
    )
    # Keep ``uom_ids`` as the single source of truth at the UoM level, but
    # derive it from the variants' packagings and reconcile back through them.
    uom_ids = fields.Many2many(
        compute="_compute_uom_ids",
        inverse="_inverse_uom_ids",
        store=True,
        readonly=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        # ``uom_ids`` and ``packaging_ids`` are materialized into per-variant
        # packagings, which can only be created once the variants exist. On
        # create the variants are built after these values are first processed
        # (``uom_ids`` even gets wiped by its own recompute when no packaging
        # exists yet), so re-apply the requested values now to (re)create them.
        # When ``create_product_product`` is False the template is only being
        # delegated from ``product.product.create`` (the variant doesn't exist
        # yet); that flow re-applies the values itself, so skip it here.
        if self.env.context.get("create_product_product", True):
            for template, vals in zip(templates, vals_list, strict=True):
                if vals.get("uom_ids"):
                    template.uom_ids = vals["uom_ids"]
                if vals.get("packaging_ids"):
                    template.packaging_ids = vals["packaging_ids"]
        return templates

    @api.depends("product_variant_ids.packaging_ids.uom_id")
    def _compute_uom_ids(self):
        for template in self:
            template.uom_ids = template.product_variant_ids.packaging_ids.uom_id

    def _inverse_uom_ids(self):
        self.product_variant_ids._recompute_packagings()

    @api.depends("product_variant_ids.packaging_ids")
    def _compute_packaging_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.packaging_ids = template.product_variant_ids.packaging_ids
            else:  # pragma: no cover
                template.packaging_ids = False

    def _inverse_packaging_ids(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.packaging_ids = template.packaging_ids
