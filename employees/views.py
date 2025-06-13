from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Employee
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/list.html', {'employees':employees})

@login_required
def employee_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = int(request.POST['age'])
        email = request.POST['email']
        position = request.POST['position']
        
        Employee.objects.create(name=name, age=age, email=email, position=position)
        return HttpResponseRedirect(reverse('employee_list'))
        
    return render(request, 'employees/create.html')

@login_required
def employee_update(request, id):
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.age = int(request.POST['age'])
        employee.email = request.POST['email']
        employee.position = request.POST['position']
        employee.save()
        return HttpResponseRedirect(reverse('employee_list'))
    
    return render(request, 'employees/edit.html', {'employee':employee})

@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return HttpResponseRedirect(reverse('employee_list'))
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('employee_list')
        else:
            return render(request, 'employees/login.html', {'error':'Invalid credentials'})
                          
    return render(request, 'employees/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')