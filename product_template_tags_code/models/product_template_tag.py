# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slugify


class ProductTemplateTag(models.Model):

    _inherit = "product.template.tag"

    code = fields.Char(string="Code")

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Product template code already exists",)
    ]

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._update_code()
        return res

    def write(self, vals):
        res = super().write(vals)
        self._update_code()
        return res

    def _update_code(self):
        for rec in self:
            code = False
            if rec.code and rec.code != slugify(rec.code):
                # make sure the code is always clean
                code = slugify(rec.code)
            elif rec.name and rec.name.strip():
                code = slugify(rec.name)
            super(ProductTemplateTag, rec).write({"code": code})
