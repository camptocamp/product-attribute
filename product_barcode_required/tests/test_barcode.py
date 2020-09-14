# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo import exceptions
from odoo.tests import Form, SavepointCase


class TestBarcodeBase(SavepointCase):

    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))


class TestBarcodeDefault(TestBarcodeBase):
    def test_barcode_is_required(self):
        self.assertFalse(self.env["product.template"]._is_barcode_required_enabled())
        self.assertFalse(self.env["product.product"]._is_barcode_required_enabled())

    def test_onchange_default_template(self):
        """Nothing changes since the constraint is not enabled."""
        form = Form(self.env["product.template"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertFalse(form.barcode)
        record = form.save()
        self.assertFalse(record.barcode)

    def test_onchange_default_variant(self):
        """Nothing changes since the constraint is not enabled."""
        form = Form(self.env["product.product"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertFalse(form.barcode)
        record = form.save()
        self.assertFalse(record.barcode)


class TestBarcodeTemplateRequired(TestBarcodeBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.product_variant_barcode_required = True

    def test_barcode_is_required(self):
        self.assertTrue(self.env["product.template"]._is_barcode_required_enabled())
        self.assertTrue(self.env["product.product"]._is_barcode_required_enabled())

    def test_onchange_required_template(self):
        """Requirement enabled, default barcode to default_code."""
        form = Form(self.env["product.template"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertEqual(form.barcode, "PROD-A")
        record = form.save()
        self.assertEqual(record.barcode, "PROD-A")

    def test_onchange_required_variant(self):
        """Requirement enabled, default barcode to default_code."""
        form = Form(self.env["product.product"])
        form.name = "Prod A"
        form.default_code = "PROD-A"
        self.assertEqual(form.barcode, "PROD-A")
        record = form.save()
        self.assertEqual(record.barcode, "PROD-A")

    def test_validation_create(self):
        """Can create a record w/out barcode since the constraint is not enabled."""
        with self.assertRaises(exceptions.ValidationError) as err:
            self.env["product.product"].create(
                {"name": "Variant A", "default_code": "VAR-A"}
            )

        self.assertEqual(err.exception.name, "Product 'Variant A' has no barcode!")

    def test_validation_write(self):
        """Can create a record w/out barcode since the constraint is not enabled."""
        prod = self.env["product.product"].create(
            {"name": "Variant A", "default_code": "VAR-A", "barcode": "VAR-A"}
        )
        with self.assertRaises(exceptions.ValidationError) as err:
            prod.barcode = False

        self.assertEqual(err.exception.name, "Product 'Variant A' has no barcode!")
