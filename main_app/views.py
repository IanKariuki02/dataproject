from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import EmployeeForm
from main_app.models import Employee


# Create your views here.

def home(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Employee was saved")
            return redirect("home")

    else:
        form = EmployeeForm()
    return render(request, "employee.html", {"form": form})


def all_employees(request):
    employees = Employee.objects.all().all().order_by("salary")
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)
    return render(request, "all_employees.html", {"employees": data})


def employee_details(request, emp_id):
    employees = Employee.objects.get(pk=emp_id)
    return render(request, "employee_details.html", {"employees": employees})


def employee_delete(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    employee.delete()
    messages.warning(request, "This Employee was deleted permanently")
    return redirect("all")


def search_employees(request):
    search_word = request.GET["search_word"]
    employees = Employee.objects.filter(
        Q(name__icontains=search_word) | Q(email__icontains=search_word)
    )
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)

    return render(request, "all_employees.html", {"employees": data})


def employee_update(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Updated Successfully")
            return redirect('details', emp_id)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, "update.html", {"form": form})
