The check is off until you turn it on, so installing the module changes
nothing by itself.

Set the System Parameter \`stock_lot_unique_name.enabled\` to "True" under
Settings \> Technical \> System Parameters.

The check then applies to every user and to every lot or serial number,
whether it was typed by hand or produced by a sequence. Numbers a vendor
supplies are included, so review existing data before turning it on: two
products legitimately sharing a vendor's number will be refused from that
point on.

Existing duplicates are left alone. Only records created or renamed after
the parameter is set are checked.
