# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SeasonalConfLine(models.Model):
    _name = "seasonal.config.line"
    _description = "Seasonal configuiration Line"

    seasonal_config_id = fields.Many2one(comodel_name="seasonal.config", required=True)
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain=[("sale_ok", "=", True)],
        required=True,
    )
    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime()
    monday = fields.Boolean(default=True)
    tuesday = fields.Boolean(default=True)
    wednesday = fields.Boolean(default=True)
    thursday = fields.Boolean(default=True)
    friday = fields.Boolean(default=True)
    saturday = fields.Boolean(default=True)
    sunday = fields.Boolean(default=True)

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        for line in self:
            if line.date_end and line.date_end < line.date_start:
                raise ValidationError(
                    _("The end date cannot be earlier than the start date.")
                )

    def is_sale_ok(self, date):
        # TODO: can't we just get a date and determin week day from it?
        self.ensure_one()

        weekday = date.strftime("%A").lower()
        # check if we are on the correct day of the week
        if not self[weekday]:
            return False

        # check if the provided date is between date_start and date_end
        # of the seasonal conf line
        # TODO: include limits w/ `=`?
        if date < self.date_start or self.date_end and date > self.date_end:
            return False

        return True

    # TODO: shall we use the product's company to retrieve the default config?

    def find_for_product(self, prod, config=None):
        domain = [
            ("product_id", "=", prod.id),
        ]
        if config:
            domain.append(("seasonal_config_id", "=", config.id))
        return self.search(domain)
