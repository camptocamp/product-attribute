This module provides a weight calculation function for products based on their
packagings weight.

It uses module `stock_packaging_calculator` to get weight from packagings
having a weight defined first and fallback on product weight field if no
weight is defined on the packagings.
