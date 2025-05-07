from django.db import models


class ProductInventory(models.Model):
    product_name = models.CharField(max_length=100)
    product_quantity = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=False)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applicable = models.BooleanField(default=False)

    class Meta:
        db_table = "product_inventory"

    def __str__(self):
        return self.product_name

    def price_with_discount(self, discount):
        """
        Calculate the selling price after applying the subdealer's discount.
        """
        if self.discount_applicable:
            return self.selling_price * (1 - (discount / 100))
        return self.selling_price
