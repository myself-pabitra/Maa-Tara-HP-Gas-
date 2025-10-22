from decimal import Decimal
import json
from django.shortcuts import redirect, render
from django.db import transaction
from employees.models import Employee
from inventory.models import ProductInventory
from .models import Cylender_information, DailyInvoice, DailyInvoiceExpense, DailyInvoiceLineItem, PredefinedExpense, SubDealerSKUDiscount, Subdealer
from django.contrib import messages
from django.utils import timezone
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



def create_invoice(request):
    subdealers = Subdealer.objects.all()
    products = ProductInventory.objects.all()
    employees = Employee.objects.all()

    # Predefined expenses
    predefined_expenses = PredefinedExpense.objects.values_list('name', 'default_amount')
    predefined_expenses_dict = {name: float(amount) for name, amount in predefined_expenses}
    predefined_expenses_json = json.dumps(predefined_expenses_dict)

    # Discounts map: {subdealer_code: {product_id: discount}}
    discounts_map = {}
    for d in SubDealerSKUDiscount.objects.all():
        discounts_map.setdefault(d.subdealer.subdealerCode, {})[d.product.id] = float(d.product_discount)
    discounts_map_json = json.dumps(discounts_map)

    if request.method == 'POST':
        with transaction.atomic():
            # Create invoice first
            invoice = DailyInvoice.objects.create(
                invoice_date=request.POST['invoice_date'],
                payment_mode=request.POST['payment_mode'],
                notes=request.POST.get('notes', '')
            )

            # Assign employees
            employee_ids = request.POST.getlist('employee_ids')
            invoice.employees.set(employee_ids)

            # Line items
            products_ids = request.POST.getlist('product_id[]')
            subdealers_codes = request.POST.getlist('subdealer_code[]')
            qtys = request.POST.getlist('quantity[]')
            submitted = request.POST.getlist('submitted_blank[]')
            discounted_prices = request.POST.getlist('discounted_price[]')
            line_totals = request.POST.getlist('line_total[]')
            due_cyls = request.POST.getlist('due_cyl[]')

            subtotal = Decimal('0.00')

            for i in range(len(products_ids)):
                product = ProductInventory.objects.get(id=products_ids[i])
                subdealer = Subdealer.objects.get(subdealerCode=subdealers_codes[i])
                qty = int(qtys[i])
                price = Decimal(discounted_prices[i])
                total = Decimal(line_totals[i])
                due_cyl = int(due_cyls[i])
                submitted_blank = int(submitted[i])

                subtotal += total

                # Create line item
                DailyInvoiceLineItem.objects.create(
                    invoice=invoice,  # pass the instance
                    subdealer=subdealer,
                    product=product,
                    quantity=qty,
                    submitted_blank=submitted_blank,
                    discounted_price=price,
                    line_total=total,
                    due_cyl=due_cyl
                )

                # Update or create cylinder info
                cyl_info, created = Cylender_information.objects.get_or_create(
                    Subdealer=subdealer,
                    product=product,
                    defaults={'due_cylender_qty': due_cyl}
                )
                if not created:
                    cyl_info.due_cylender_qty = due_cyl
                    cyl_info.save()

            # Expenses
            other_expense_total = Decimal('0.00')
            for key in request.POST:
                if key.startswith('expense_type_'):
                    idx = key.split('_')[-1]
                    type_ = request.POST.get(f'expense_type_{idx}')
                    amount = Decimal(request.POST.get(f'expense_amount_{idx}', '0'))
                    desc = request.POST.get(f'expense_desc_{idx}', '')

                    if amount > 0:
                        DailyInvoiceExpense.objects.create(
                            invoice=invoice,
                            expense_name=desc if type_ == 'other' else type_,
                            expense_amount=amount
                        )
                        other_expense_total += amount

            # Update totals on invoice
            invoice.subtotal = subtotal
            invoice.other_expense = other_expense_total
            invoice.grand_total = subtotal - other_expense_total
            invoice.save()

            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            return redirect('create_daily_sell_invoice')

    context = {
        'subdealers': subdealers,
        'products': products,
        'employees': employees,
        'today': timezone.now(),
        'predefined_expenses_json': predefined_expenses_json,
        'discounts_map_json': discounts_map_json,
    }
    return render(request, "billing/create_daily_sell_invoice.html", context)