from psycopg2 import IntegrityError

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


def _make_attr_line(env, product, attribute, values):
    """Helper: create a product.template.attribute.line with required values."""
    return env["product.template.attribute.line"].create(
        {
            "product_tmpl_id": product.id,
            "attribute_id": attribute.id,
            "value_ids": [Command.set(values.ids)],
        }
    )


class TestProductClass(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.size_attr = cls.env["product.attribute"].create({"name": "Size"})
        cls.size_value = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.size_attr.id}
        )
        cls.color_attr = cls.env["product.attribute"].create({"name": "Color"})
        cls.color_value = cls.env["product.attribute.value"].create(
            {"name": "Red", "attribute_id": cls.color_attr.id}
        )

    def test_product_with_compatible_class(self):
        """
        Assigning a class whose attribute matches
        the product's attribute line passes.
        """
        product_class = self.env["product.class"].create(
            {"name": "Test Class", "attribute_ids": [Command.set([self.size_attr.id])]}
        )
        product = self.env["product.template"].create({"name": "Product 1"})
        _make_attr_line(self.env, product, self.size_attr, self.size_value)

        product.write({"class_id": product_class.id})

        self.assertEqual(product.class_id, product_class)

    def test_constraint_raises_on_incompatible_attribute_write(self):
        """
        Constraint raises when writing an incompatible attribute
        to a product with a class.
        """
        product_class = self.env["product.class"].create(
            {
                "name": "Test Class 2",
                "attribute_ids": [Command.set([self.size_attr.id])],
            }
        )
        product = self.env["product.template"].create({"name": "Product 2"})
        _make_attr_line(self.env, product, self.size_attr, self.size_value)
        product.class_id = product_class  # OK — size is in class

        with self.assertRaises(ValidationError) as ctx:
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.color_attr.id,
                                "value_ids": [Command.set([self.color_value.id])],
                            }
                        )
                    ]
                }
            )

        self.assertIn("do not belong to the selected class", str(ctx.exception))

    def test_constraint_raises_on_incompatible_class_change(self):
        """
        Constraint raises when class_id is changed to
        one that excludes existing lines.
        """
        color_class = self.env["product.class"].create(
            {
                "name": "Color Class",
                "attribute_ids": [Command.set([self.color_attr.id])],
            }
        )
        product = self.env["product.template"].create({"name": "Product 3"})
        _make_attr_line(self.env, product, self.color_attr, self.color_value)
        product.class_id = color_class  # OK — color is in class

        size_class = self.env["product.class"].create(
            {"name": "Size Class", "attribute_ids": [Command.set([self.size_attr.id])]}
        )
        with self.assertRaises(ValidationError) as ctx:
            product.class_id = size_class  # color is NOT in size_class → should raise
        self.assertIn(
            "Please remove these attributes or change the product class",
            str(ctx.exception),
        )

    def test_clearing_class_id_removes_constraint(self):
        """Removing class_id from a product allows any attribute afterwards."""
        product_class = self.env["product.class"].create(
            {"name": "Size Only", "attribute_ids": [Command.set([self.size_attr.id])]}
        )
        product = self.env["product.template"].create({"name": "Product 5"})
        _make_attr_line(self.env, product, self.size_attr, self.size_value)
        product.class_id = product_class

        with self.assertRaises(ValidationError) as ctx:
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.color_attr.id,
                                "value_ids": [Command.set([self.color_value.id])],
                            }
                        )
                    ]
                }
            )
        self.assertIn("do not belong to the selected class", str(ctx.exception))

        product.class_id = False

        # Now color (not in the former class) should be allowed
        product.write(
            {
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": self.color_attr.id,
                            "value_ids": [Command.set([self.color_value.id])],
                        }
                    )
                ]
            }
        )

    def test_class_with_no_attributes_rejects_any_attribute_line(self):
        """A class with no attributes prevents adding any attribute lines."""
        empty_class = self.env["product.class"].create({"name": "Empty Class"})
        product = self.env["product.template"].create(
            {"name": "Product 6", "class_id": empty_class.id}
        )

        with self.assertRaises(ValidationError) as ctx:
            product.write(
                {
                    "attribute_line_ids": [
                        Command.create(
                            {
                                "attribute_id": self.size_attr.id,
                                "value_ids": [Command.set([self.size_value.id])],
                            }
                        )
                    ]
                }
            )
        self.assertIn("do not belong to the selected class", str(ctx.exception))

    def test_classed_product_with_no_attribute_lines_is_valid(self):
        """A product with a class but no attribute lines is valid."""
        product_class = self.env["product.class"].create(
            {"name": "Hammers", "attribute_ids": [Command.set([self.size_attr.id])]}
        )
        product = self.env["product.template"].create(
            {"name": "Product 7", "class_id": product_class.id}
        )
        self.assertEqual(product.class_id, product_class)
        self.assertFalse(product.attribute_line_ids)

    def test_unique_name_constraint(self):
        """Creating two product classes with the same name raises an integrity error."""
        self.env["product.class"].create({"name": "Unique Class"})
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["product.class"].create({"name": "Unique Class"})
