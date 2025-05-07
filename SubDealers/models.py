from django.db import models
from inventory.models import ProductInventory


class Subdealer(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the subdealer")
    phone_number = models.CharField(
        max_length=15, help_text="Phone number of the subdealer"
    )
    address = models.TextField(help_text="Address of the subdealer")
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Discount percentage for the subdealer",
    )

    def __str__(self):
        return self.name

    def get_item_price_with_discount(self, inventory_item):
        """
        Get the price of the inventory item after applying the subdealer's discount.
        """
        return inventory_item.price_with_discount(self.discount)


class SubdealerInventory(models.Model):
    subdealer = models.ForeignKey(Subdealer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Override save to automatically set discounted_price when a subdealer is added to inventory.
        """
        self.discounted_price = self.subdealer.get_item_price_with_discount(
            self.product
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subdealer.name} - {self.product.product_name} (Discounted Price: {self.discounted_price})"
