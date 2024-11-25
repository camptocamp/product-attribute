# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class ProductPricelistXlsx(models.AbstractModel):
    _inherit = "report.product_pricelist_direct_print_xlsx.report"

    def _add_extra_header(self, book):
        if book.show_public_category:
            return _("Public Category")
        return super()._add_extra_header(book)

    def _add_extra_info(self, book, product, **kw):
        if book.show_public_category:
            if product.public_categ_ids:
                # Show category without format
                return (product.public_categ_ids[:1].display_name, None)
            # Return an empty string, as we wouldn't want to write False
            # in the result
            return "", None
        return super()._add_extra_info(book, product, **kw)
