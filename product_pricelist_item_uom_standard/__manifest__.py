# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Item UoM (Standard)",
    "summary": "Restrict pricelist rules to a specific product packaging (UoM)",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "author": "Camptocamp SA, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "product",
        "uom",
    ],
    # ``product_pricelist_item_uom`` (OCA/product-attribute) declares a
    # ``uom_id`` field on ``product.pricelist.item`` with incompatible
    # semantics: it is computed and always defaulted to the product base UoM,
    # and it never filters rule selection. Both modules cannot coexist.
    # This module is a backport of the standard Odoo 19.3 implementation
    # https://github.com/odoo/odoo/commit/d2648b1d983927b5df7260a16d6d1d33c213ddeb
    "excludes": ["product_pricelist_item_uom"],
    "data": [
        "views/product_pricelist_item_views.xml",
        "views/product_pricelist_views.xml",
        "views/product_views.xml",
        "report/product_pricelist_report_templates.xml",
    ],
    "installable": True,
}
