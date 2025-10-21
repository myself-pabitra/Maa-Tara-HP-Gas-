from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProductInventory


def manage_products(request):
    products = ProductInventory.objects.all()

    if request.method == "POST":
        for product in products:
            # Update stock status
            stock_key = f"in_stock_{product.id}"
            product.in_stock = bool(request.POST.get(stock_key))

            # Update prices
            buy_key = f"buy_price_{product.id}"
            product_price_key = f"product_price_{product.id}"
            quantity_key = f"product_quantity_{product.id}"

            product.buy_price = float(request.POST.get(buy_key, product.buy_price))
            product.product_price = float(request.POST.get(product_price_key, product.product_price))
            product.product_quantity = int(request.POST.get(quantity_key, product.product_quantity))

            product.save()
        
        messages.success(request, "Products updated successfully!")
        return redirect("manage_products")  # your URL name

    context = {"products": products}
    return render(request, "inventory/manage_products.html", context)


def add_product(request):
    if request.method == "POST":
        # Extract form data
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")
        product_quantity = request.POST.get("product_quantity")
        buy_price = request.POST.get("buy_price")
        in_stock = request.POST.get("in_stock") == "on"

        # Validate required fields
        if not product_name or not product_quantity or not buy_price or not product_price:
            messages.error(request, "Please fill in all required fields.")
            return redirect("Add_product")  # Replace with your URL name

        # Create ProductInventory instance
        product = ProductInventory.objects.create(
            product_name=product_name,
            product_price = product_price,
            product_quantity=int(product_quantity),
            buy_price=float(buy_price),
            in_stock=in_stock
        )

        # Trigger success message
        messages.success(request, f"Product '{product_name}' added successfully!")
        return redirect("Add_product")  # Redirect to the same form or product list

    # GET request: render the form
    return render(request, 'inventory/Add_product_to_inventory.html')
