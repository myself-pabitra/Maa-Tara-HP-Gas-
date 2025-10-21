import random
import string
from django.db import models
from inventory.models import ProductInventory


class Subdealer(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the subdealer")
    subdealerCode = models.CharField(max_length=50,unique=True,help_text="Unique Subdealer Code")
    phone_number = models.CharField(
        max_length=15, help_text="Phone number of the subdealer"
    )
    address = models.TextField(help_text="Address of the subdealer")

    class Meta:
        db_table = "SubDealers"

    def __str__(self):
        return self.name
    
    def create_subdealer_code(self):
        """
        Generate a subdealer code like:
        First 4 letters of the name + last 6 digits of the phone number + 2 random alphabets.
        """
        name_part = self.name[:4].upper()
        phone_part = self.phone_number[-6:]
        random_part = ''.join(random.choices(string.ascii_uppercase, k=2))
        return f"{name_part}{phone_part}{random_part}"
    
    def save(self, *args, **kwargs):
        """
        Automatically assign subdealerCode before saving.
        """
        if not self.subdealerCode:  # Only generate if not already set
            self.subdealerCode = self.create_subdealer_code()
        super().save(*args, **kwargs)


class SubDealerSKUDiscount(models.Model):
    subdealer = models.ForeignKey(Subdealer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    product_discount = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "SubDealer_SKU_Discount"
        # Ensure each subdealer-product combination is unique
        unique_together = ('subdealer', 'product')

    def __str__(self):
        return f"{self.subdealer.name} - {self.product.product_name} (Discount: {self.product_discount}%)"
    
    def get_subdealer_discounted_product_price(self, product):
        return product.price_after_discount(self.product_discount)
    


class Cylender_information(models.Model):
    Subdealer = models.ForeignKey(Subdealer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    due_cylender_qty = models.IntegerField()

    def __str__(self):
        return f"{self.Subdealer.name} - {self.product.product_name} (Due Cylender: {self.due_cylender_qty})"
    
    class Meta:
        db_table = "Cylender_information"