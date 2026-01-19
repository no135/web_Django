from django.shortcuts import render, redirect
from .models import Catagory, Speciality, Asset, Technician, Order, Comment, client

# --- ORDER VIEWS ---
def order(request):
    order = Order.objects.filter(visibility=True).order_by('-created_at')
    return render(request, 'home.html', {'orders': order})

def order_detail(request, order_name):
    order = Order.objects.get(name=order_name)
    comments = Comment.objects.filter(order=order).order_by('-date')
    if request.method == 'POST':
        Comment.objects.create(
            order=order,
            email=request.POST.get('email'),
            comment=request.POST.get('comment')
        )
        return redirect('order_detail', order_name=order_name)
    return render(request, 'detail.html', {'order': order, 'comments': comments})

def add_order(request):
    assets = Asset.objects.all()
    technicians = Technician.objects.all()
    orders = Order.objects.filter(visibility=True) 
    if request.method == 'POST':
        order_obj = Order()
        order_obj.name = request.POST.get('name')
        order_obj.image = request.FILES.get('image')
        order_obj.asset = Asset.objects.get(name=request.POST.get('asset'))
        order_obj.technician = Technician.objects.get(name=request.POST.get('technician'))
        order_obj.save()
        return redirect('add_order')
    return render(request, 'add_order.html', {'assets': assets, 'technicians': technicians, 'orders': orders})

def edit_order(request, order_name):
    order_obj = Order.objects.get(name=order_name)
    assets = Asset.objects.all()
    technicians = Technician.objects.all()
    if request.method == 'POST':
        order_obj.name = request.POST.get('name')
        if request.FILES.get('image'):
            order_obj.image = request.FILES.get('image')
        order_obj.asset = Asset.objects.get(name=request.POST.get('asset'))
        order_obj.technician = Technician.objects.get(name=request.POST.get('technician'))
        order_obj.save()
        return redirect('add_order')
    return render(request, 'edit_order.html', {'order': order_obj, 'assets': assets, 'technicians': technicians})

def delete_order(request, order_name):
    order = Order.objects.get(name=order_name)
    order.visibility = False
    order.save()
    return redirect('add_order')

# --- CATEGORY VIEWS ---
def category_list(request):
    categories = Catagory.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        Catagory.objects.create(name=request.POST.get('name'))
        return redirect('category_list')
    return render(request, 'add_category.html')

def edit_category(request, cat_name):
    cat = Catagory.objects.get(name=cat_name)
    if request.method == 'POST':
        cat.name = request.POST.get('name')
        cat.save()
        return redirect('category_list')
    return render(request, 'edit_category.html', {'category': cat})

def delete_category(request, cat_name):
    Catagory.objects.get(name=cat_name).delete()
    return redirect('category_list')

# --- SPECIALITY VIEWS ---
def speciality_list(request):
    specialities = Speciality.objects.all()
    return render(request, 'speciality_list.html', {'specialities': specialities})

def add_speciality(request):
    if request.method == 'POST':
        Speciality.objects.create(name=request.POST.get('name'))
        return redirect('speciality_list')
    return render(request, 'add_speciality.html')

def edit_speciality(request, spec_name):
    spec = Speciality.objects.get(name=spec_name)
    if request.method == 'POST':
        spec.name = request.POST.get('name')
        spec.save()
        return redirect('speciality_list')
    return render(request, 'edit_speciality.html', {'speciality': spec})

def delete_speciality(request, spec_name):
    Speciality.objects.get(name=spec_name).delete()
    return redirect('speciality_list')

# --- ASSET VIEWS ---
def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'asset_list.html', {'assets': assets})

def add_asset(request):
    categories = Catagory.objects.all()
    if request.method == 'POST':
        asset = Asset()
        asset.name = request.POST.get('name')
        asset.owner_name = request.POST.get('owner_name')
        asset.serial_number = request.POST.get('serial_number')
        asset.catagory = Catagory.objects.get(name=request.POST.get('category'))
        asset.save()
        return redirect('asset_list')
    return render(request, 'add_asset.html', {'categories': categories})

def edit_asset(request, asset_name):
    asset = Asset.objects.get(name=asset_name)
    categories = Catagory.objects.all()
    if request.method == 'POST':
        asset.name = request.POST.get('name')
        asset.owner_name = request.POST.get('owner_name')
        asset.serial_number = request.POST.get('serial_number')
        asset.catagory = Catagory.objects.get(name=request.POST.get('category'))
        asset.save()
        return redirect('asset_list')
    return render(request, 'edit_asset.html', {'asset': asset, 'categories': categories})

def delete_asset(request, asset_name):
    Asset.objects.get(name=asset_name).delete()
    return redirect('asset_list')

# --- TECHNICIAN VIEWS ---
def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'technician_list.html', {'technicians': technicians})

def add_technician(request):
    specs = Speciality.objects.all()
    if request.method == 'POST':
        tech = Technician()
        tech.name = request.POST.get('name')
        tech.Speciality = Speciality.objects.get(name=request.POST.get('speciality'))
        tech.save()
        return redirect('technician_list')
    return render(request, 'add_technician.html', {'specialities': specs})

def edit_technician(request, tech_name):
    tech = Technician.objects.get(name=tech_name)
    specs = Speciality.objects.all()
    if request.method == 'POST':
        tech.name = request.POST.get('name')
        tech.Speciality = Speciality.objects.get(name=request.POST.get('speciality'))
        tech.save()
        return redirect('technician_list')
    return render(request, 'edit_technician.html', {'technician': tech, 'specialities': specs})

def delete_technician(request, tech_name):
    Technician.objects.get(name=tech_name).delete()
    return redirect('technician_list')

def clientn(request):
    if request.method == 'POST':
        name = request.POST.get('cname')
        fathername = request.POST.get('cfname') 

        clientdata = client()
        clientdata.name = name
        clientdata.fname = fathername
        clientdata.save()
    clients = client.objects.all()
    return render(request,'add_client.html',{'client':clients})