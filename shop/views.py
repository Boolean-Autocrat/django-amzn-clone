from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category, Rating
from django.views.generic import ListView
from django.urls import reverse
from .forms import SignupForm, SignInForm, RatingForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout as logout_user
from django.conf import settings
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(
        request, "shop/index.html", {"products": products, "categories": categories}
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    similar_items = Product.objects.filter(category=product.category).exclude(slug=slug)
    rating_form = RatingForm()

    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            if not Rating.objects.filter(product=product, user=request.user).exists():
                rating_value = rating_form.cleaned_data["stars"]
                comment = rating_form.cleaned_data["comment"]
                Rating.objects.create(
                    product=product,
                    user=request.user,
                    stars=rating_value,
                    comment=comment,
                )
            else:
                messages.add_message(
                    request, messages.WARNING, "You have already rated this product."
                )

    return render(
        request,
        "shop/detail.html",
        {
            "product": product,
            "similar_items": similar_items,
            "categories": categories,
            "rating_form": rating_form,
        },
    )


def category(request, slug):
    products = Product.objects.filter(category__slug=slug)
    categories = Category.objects.all()
    return render(
        request,
        "shop/index.html",
        {"products": products, "name": slug, "categories": categories},
    )


def search(request):
    query = request.GET.get("q")
    categories = Category.objects.all()
    if not query:
        return redirect("shop:home")

    # search in title, description, or features
    products = (
        Product.objects.filter(category__name__icontains=query)
        | Product.objects.filter(name__icontains=query)
        | Product.objects.filter(description__icontains=query)
        | Product.objects.filter(features__icontains=query)
    )

    return render(
        request,
        "shop/index.html",
        {"products": products, "name": "Search Results", "categories": categories},
    )


def signup(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            # create a new user
            form.save()

            messages.add_message(
                request, messages.SUCCESS, "Your Account has been created successfully!"
            )
            messages.add_message(
                request, messages.SUCCESS, "Now Sign-In to continue..."
            )
            return redirect("shop:signin")

    else:
        form = SignupForm()
    return render(request, "auth/signup.html", {"form": form})


def signin(request):
    next_url = request.GET.get("next")

    if request.user.is_authenticated:
        return redirect("shop:home")

    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Signed In successfully!")
                return redirect(next_url) if next_url else redirect("shop:home")
            else:
                messages.error(request, "Email or Password doesn't match!")
        else:
            messages.error(request, "Invalid form submission. Please check the form.")

    else:
        form = SignInForm()

    return render(request, "auth/signin.html", {"form": form})


def logout(request):
    logout_user(request)
    return redirect("shop:signin")


@login_required()
def shopping_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        categories = Category.objects.all()
        products = CartItem.objects.filter(cart=cart)
    except ObjectDoesNotExist:
        cart = Cart(user=request.user)
        cart = Cart.objects.get(user=request.user)
        categories = Category.objects.all()
        products = CartItem.objects.filter(cart=cart)
    return render(
        request,
        "shop/shopping_cart.html",
        {"products": products, "name": "Shopping Cart", "categories": categories},
    )


@login_required
def checkout_page(request):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart).delete()
    return render(request, "shop/checkout.html", {"name": "Checkout Page"})
