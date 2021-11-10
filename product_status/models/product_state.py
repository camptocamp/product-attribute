# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import ValidationError


class ProductState(models.Model):
    _inherit = "product.state"

    def write(self, vals):
        default_data = [st.code for st in self._get_defalt_data()]
        if (
            self.code in default_data
            and not self.env.context.get("install_module") == "product_status"
        ):
            raise ValidationError(
                _("Cannot modified default state, state name: %s" % (self.name))
            )
        else:
            return super(ProductState, self).write(vals)

    def unlink(self):
        default_data = [st.code for st in self._get_defalt_data()]
        for state in self:
            if state.code in default_data:
                raise ValidationError(
                    _("Cannot delete default state, state name: %s" % (state.name))
                )
        return super().unlink()

    def _get_defalt_data(self):
        return [
            self.env.ref("product_status.product_state_new"),
            self.env.ref("product_status.product_state_discontinued"),
            self.env.ref("product_status.product_state_phaseout"),
            self.env.ref("product_status.product_state_endoflife"),
        ]
