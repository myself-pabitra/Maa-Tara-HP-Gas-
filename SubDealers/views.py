from django.shortcuts import redirect, render

from inventory.models import ProductInventory
from .models import SubDealerSKUDiscount, Subdealer
from django.contrib import messages
# Create your views here.

def CreateNewSubDealers(request):
    subDealer_name = request.POST.get("name")
    phone_number = request.POST.get("phone_number")
    address = request.POST.get("address")


    if subDealer_name and phone_number and address:
        subdealer = Subdealer(
            name=subDealer_name,
            phone_number=phone_number,
            address=address,
        )
        subdealer.save()
        messages.success(request, f"Subdealer '{subDealer_name}' created successfully!")
        return redirect("CreateNewSubDealers")

    return render(request,"SubDealers/Createnew_subdealers.html")



def addSubDealersProductDiscount(request):
    subdealer_code = request.GET.get("subdealer_code")
    product_id = request.GET.get("product_id")

    existing_discount = None
    if subdealer_code and product_id:
        existing_discount = SubDealerSKUDiscount.objects.filter(
            subdealer__subdealerCode=subdealer_code,
            product__id=product_id
        ).first()

    if request.method == "POST":
        subdealer_code = request.POST.get("subdealer_code")
        product_id = request.POST.get("product_name")
        discount_amount = request.POST.get("discount_amount")

        if not subdealer_code or not product_id or not discount_amount:
            messages.error(request, "Please fill in all required fields.")
            return redirect("addSubDealersProductDiscount")

        subdealer = Subdealer.objects.get(subdealerCode=subdealer_code)
        product = ProductInventory.objects.get(id=product_id)

        existing_discount = SubDealerSKUDiscount.objects.filter(subdealer=subdealer, product=product).first()
        if existing_discount:
            old_discount = existing_discount.product_discount
            existing_discount.product_discount = discount_amount
            existing_discount.save()
            messages.info(
                request,
                f"Discount updated for {subdealer.name} on {product.product_name}: {old_discount} to {discount_amount}"
            )
        else:
            SubDealerSKUDiscount.objects.create(
                subdealer=subdealer,
                product=product,
                product_discount=discount_amount
            )
            messages.success(request, f"New discount added for {subdealer.name} on {product.product_name} ({discount_amount})!")

        return redirect("view_subdealer_discounts")

    subdealers = Subdealer.objects.all()
    products = ProductInventory.objects.all()

    context = {
        "subdealers": subdealers,
        "products": products,
        "existing_discount": existing_discount
    }
    return render(request, "SubDealers/add_subdealer_product_discount.html", context)





def view_subdealer_discounts(request):
    subdealer_filter = request.GET.get("subdealer")
    product_filter = request.GET.get("product")

    discounts = SubDealerSKUDiscount.objects.select_related("subdealer", "product").all()

    if subdealer_filter:
        discounts = discounts.filter(subdealer__id=subdealer_filter)
    if product_filter:
        discounts = discounts.filter(product__id=product_filter)

    subdealers = Subdealer.objects.all()
    products = ProductInventory.objects.all()

    context = {
        "discounts": discounts,
        "subdealers": subdealers,
        "products": products,
        "selected_subdealer": subdealer_filter,
        "selected_product": product_filter,
    }
    return render(request, "SubDealers/view_subdealer_discounts.html", context)