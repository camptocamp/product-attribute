# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    "name": "Product Packaging Container Deposit",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "summary": "Product Packaging Container Deposit",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "product_packaging_level",
    ],
    "data": [
        "views/stock_package_type_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
