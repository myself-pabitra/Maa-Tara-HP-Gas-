from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee

def add_new_employees(request):
    if request.method == "POST":
        employee_name = request.POST.get("employee_name")
        employee_phone = request.POST.get("phone")
        employee_address = request.POST.get("address")

        # Validation
        if not employee_name or not employee_phone or not employee_address:
            messages.error(request, "Please fill in all required fields.")
            return redirect("add_new_employees")

        # Save employee
        Employee.objects.create(
            name=employee_name,
            phone=employee_phone,
            address=employee_address
        )
        messages.success(request, f"Employee '{employee_name}' created successfully!")
        return redirect("add_new_employees")

    # GET request
    employees = Employee.objects.all()  # Optional: list all employees below the form
    context = {"employees": employees}
    return render(request, "employees/add_new_employees.html", context)
