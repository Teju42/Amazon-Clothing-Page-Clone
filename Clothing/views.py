from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

# Home View
def home(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, 'Please sign in to add products.')
            return redirect('signin')
            
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    prod = Product.objects.all().order_by('-id')  # Show newest first
    return render(request, 'Clothing/home.html', {'prod': prod, 'form': form})

# Update View
@login_required
def update_data(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, "Clothing/update.html", {'form': form, 'product': product})

# Delete View
@login_required
def delete_data(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('home')
    else:
        # If someone tries to access this via GET, redirect to home
        return redirect('home')