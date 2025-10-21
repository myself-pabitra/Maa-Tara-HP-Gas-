from django.db import models


class ProductInventory(models.Model):
    product_name = models.CharField(max_length=100)
    product_quantity = models.IntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2,help_text="MRP of the Product")
    in_stock = models.BooleanField(default=False)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2,help_text="Buying Price of the Product")


    class Meta:
        db_table = "product_inventory"

    def __str__(self):
        return self.product_name
    
    def price_after_discount(self,discount_amount):
        '''Product price after discount will be product MRP - discount amount'''
        return self.product_price - discount_amount
