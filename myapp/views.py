from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm, SignUpForm, BootstrapLoginForm
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ContactSellerForm
from django.core.mail import send_mail
from django.conf import settings


def homepage(request):
    products = Product.objects.all()

    # Get filters from GET params
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    location = request.GET.get('location')
    query = request.GET.get('q')

    # Apply category filter
    if category:
        products = products.filter(category__iexact=category)

    # Apply price filters
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Apply location filter (case-insensitive contains)
    if location:
        products = products.filter(location__icontains=location)

    # Apply search filter (title or description)
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Pagination (10 items per page)
    from django.core.paginator import Paginator
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,   # products now paginated
        "page_obj": page_obj,
    }
    return render(request, "myapp/homepage.html", {"products": page_obj})
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('my_products')

    return render(request, 'myapp/product_delete.html', {'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'myapp/product_detail.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('my_products')

    return render(request, 'myapp/product_update.html', {'product': product})
# ---------- Public ----------
def home(request):
    products = Product.objects.select_related('owner')[:12]
    return render(request, 'myapp/home.html', {'products': products})

# ---------- Auth ----------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account was created.')
            return redirect('homepage')
    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = BootstrapLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Logged in successfully.')
            next_url = request.GET.get('next') or 'my_products'
            return redirect(next_url)
    else:
        form = BootstrapLoginForm(request)

    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# ---------- CRUD (protected) ----------
@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'myapp/homepage.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # include files
        if form.is_valid():
            prod = form.save(commit=False)
            prod.seller = request.user  # ⚠ assign the logged-in user here
            prod.save()
            messages.success(request, 'Product created successfully.')
            return redirect('my_products')
        else:print("Form errors:", form.errors)
        messages.error(request, "There were errors in your form. Check the fields.")
    else:
        form = ProductForm()
        


    return render(request, 'myapp/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Product updated.')
        return redirect('my_products')
    return render(request, 'myapp/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
        return redirect('my_products')
    return render(request, 'myapp/confirm_delete.html', {'product': product})

# ---------- Optional: “product2 / viewdetails / update” legacy pages ----------
@login_required
def product2(request):
    pro = Product.objects.filter(owner=request.user)
    return render(request, 'myapp/product2.html', {'pro': pro})

@login_required
def viewdetails(request, pk):
    pro = get_object_or_404(Product, pk=pk, owner=request.user)
    return render(request, 'myapp/viewdetails.html', {'pro': pro})

@login_required
def update_legacy(request, pk):
    pro = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=pro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.')
            return redirect('product2')
    else:
        form = ProductForm(instance=pro)
    # reuse product_form.html or keep your old update.html if you really want
    return render(request, 'myapp/product_form.html', {'form': form})

# ---------- New: Contact Seller ----------#
def contact_seller(request, pk):
    product = get_object_or_404(Product, pk=pk)
    seller_email = product.seller.email

    if request.method == "POST":
        form = ContactSellerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            full_message = f"Message about {product.title}\n\nFrom: {name} <{email}>\n\n{message}"

            send_mail(
                subject=f"Inquiry about {product.title}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[seller_email],
                fail_silently=False,
            )

            messages.success(request, "Your message has been sent to the seller.")
            return redirect("product_detail", pk=product.pk)
    else:
        form = ContactSellerForm()

    return render(request, "myapp/contact_seller.html", {"form": form, "product": product})