# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slugify


class ProductTemplateTag(models.Model):

    _inherit = "product.template.tag"

    code = fields.Char(
        string="Code", compute="_compute_code", readonly=False, store=True,
    )

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Product template code already exists",)
    ]

    @api.depends("name")
    def _compute_code(self):
        for rec in self:
            if rec.code and not rec.code == slugify(rec.code):
                # make sure the code is always clean
                rec.code = slugify(rec.code)
            elif rec.name and rec.name.strip():
                rec.code = slugify(rec.name)
            else:
                rec.code = False
