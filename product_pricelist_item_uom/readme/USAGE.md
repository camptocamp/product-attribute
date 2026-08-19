Configuration
-------------

1. Enable *Sales → Configuration → Settings → Units of Measure & Packagings*.
2. Open a product and add the packagings it is sold in
   (*Sales* tab, *Packagings*).

Defining a rule per packaging
-----------------------------

1. Go to *Sales → Products → Pricelists* and open a pricelist.
2. Add a price rule applied on a single product.
3. Set the *Packaging* field to one of the product's packagings, and the
   *Min. Quantity* in that same packaging.

Leaving *Packaging* empty keeps the standard behaviour: the rule applies to any
unit of measure and its *Min. Quantity* is expressed in the product base unit.

Example, for a product sold per *Units* and per *Dozens*:

| Packaging | Min. Quantity | Price |
|-----------|---------------|-------|
| Units     | 0             | 10.00 |
| Units     | 5             |  9.00 |
| Dozens    | 0             |  8.00 |
| Dozens    | 5             |  7.00 |

Ordering 5 dozens selects the last rule, while ordering 5 units selects the
second one.

Report
------

Select the products, then *Print → Pricelist*. Products having a rule per
packaging are printed with one price row per packaging.
