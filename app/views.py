from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Dish, Order, Menu, Cart , Review
from .forms import DishForm, OrderForm, CartForm, UserProfileForm 
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserChangeForm
from .forms import ReviewForm


# Create your views here.

def home(request):
    # Fetch available dishes
    available_dishes = Dish.objects.filter(availability=True)
    data = Dish.objects.all()

    # Count items in the cart for the logged-in user
    cart_item_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

    context = {
        'home': available_dishes,
        'cart_item_count': cart_item_count,
    }

    return render(request, 'index.html', context)


def reviews(request):
    # Handle review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate review with logged-in user
            review.save()  # Save the review to the database
            return redirect('reviews')  # Redirect to the reviews page to see the review

    else:
        form = ReviewForm()

    # Fetch all reviews to display on the reviews page
    reviews = Review.objects.all().order_by('-date_posted')

    context = {
        'form': form,
        'reviews': reviews,
    }

    return render(request, 'review.html', context)

def home1(request):
    data = Dish.objects.all()
    if request.user.is_authenticated:
        print("User is authenticated")
    else:
        print("User is not authenticated")
    context = {
        'home1': data
    }
    return render(request, 'home.html',context)


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already taken")
            return redirect("/register/")
        
        user_email = User.objects.filter(email=email)
        
        if user_email.exists():
            messages.info(request, "Email already taken")
            return redirect("/register/")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully. Please log in.")
        return redirect("/login/")  
    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username = username)
        
        if not user.exists():
            messages.error(request, "Invalid username")
            return redirect("/login/")
        
        user_auth = authenticate(username = username, password = password)
        
        if user_auth is None:
            messages.error(request, "Invalid password")
            return redirect("/login/")
        
        else:
            login(request,user_auth)
            return redirect("/home/")
    return render(request, 'login.html')

@login_required(login_url='/login/')
def view_menu(request):
    # Get all dishes from the menu
    menu = Dish.objects.all()

    # Get the user's cart items
    user_cart = Cart.objects.filter(user=request.user)

    # Extract the dish IDs that the user has in their cart
    user_cart_dish_ids = [item.dish.id for item in user_cart]

    return render(request, 'view_menu.html', {
        'menu': menu,
        'user_cart': user_cart_dish_ids,  # Pass the user's cart dish IDs
    })

def logout_page(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login/")
def add_dish(request):
    if request.method == "POST":
        dish_name = request.POST.get("dish_name")
        dish_dis = request.POST.get("dish_dis")
        price = request.POST.get("price")
        dish_image = request.POST.get("dish_image")
        availability = request.POST.get("availability", "off") == "on"

        # Validate fields
        if not dish_name or not price:
            messages.error(request, "Dish Name and Price are required.")
            return render(request, "add_dish.html")

        try:
            # Save Dish (without assigning user if unnecessary)
            Dish.objects.create(
                user=request.user,  # Only include this if the model has a `user` field
                dish_name=dish_name,
                price=price,
                dish_dis=dish_dis,
                dish_image=dish_image,
                availability=availability
            )
            messages.success(request, "Dish added successfully!")
            return redirect("home")  # Redirect to home page after adding the dish

        except Exception as e:
            messages.error(request, f"Error while adding dish: {e}")
            return render(request, 'add_dish.html')  # Return to the same page if there's an error

    return render(request, 'add_dish.html')  # Render the Add Dish form

@login_required(login_url="/login/")
def update_availability(request, dish_id):
    try:
        dish = Dish.objects.get(pk=dish_id)
        dish.availability = not dish.availability
        dish.save()
        return redirect("dish")
    except Dish.DoesNotExist:
        return HttpResponse("dish")
        
@login_required(login_url="/login/")
def update_dish(request, dish_id):
    queryset = Dish.objects.get(id=dish_id)
    
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dish item updated successfully.')
            return redirect('dish')
    else:
        form = DishForm(instance=queryset)
    return render(request, 'update_dish.html', {'form': form, 'item': queryset})    
        
@login_required(login_url='/login/')
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        
        # Update the quantity of the cart item
        if new_quantity.isdigit() and int(new_quantity) > 0:
            cart_item.quantity = int(new_quantity)
            cart_item.save()
    
    return redirect('view_cart')

@login_required(login_url='/login/')
def remove_cart_item(request, dish_id):
    try:
        # Remove the item from the cart
        cart_items = Cart.objects.filter(user=request.user, dish_id=dish_id)
        cart_items.delete()  # Remove all matching cart items for the user and dish
        
        # Show a success message and redirect to the cart page
        messages.success(request, "Dish removed from cart")
        return redirect('view_cart')
    except Cart.DoesNotExist:
        messages.error(request, "Dish not found in cart")
        return redirect('view_cart')
    
@login_required(login_url='/login/')
def view_cart(request):
    # Handle form submission for cart updates
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        form = CartForm(request.POST, prefix=form_id)
        
        if form.is_valid():
            form.save()  # Update the cart with the new data
            return redirect('view_cart')  # Redirect to the same page to reflect changes
    
    # Fetch the cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Create a dictionary of cart forms for each cart item
    cart_forms = {item.dish.id: CartForm(instance=item, prefix=f'form_{item.id}') for item in cart_items}
    
    # Calculate the total price of the cart
    total_price = sum(item.dish.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_forms': cart_forms,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)

def delete_dish(request, id):
    queryset = Dish.objects.get(id = id)
    queryset.delete()
    return redirect("/dish/")

@login_required(login_url='/login/')
def place_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user, quantity__gt=0)
    total_price = sum(item.dish.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Validate address and payment method
        if not address or not payment_method:
            messages.error(request, "Please provide all required details.")
            return redirect('place_order')

        # Create an order for each dish in the cart
        for item in cart_items:
            Order.objects.create(
                user=user,
                dishes=item.dish,
                quantity=item.quantity,
                total_price=item.dish.price * item.quantity,
                status='received',
                delivery_address=address,
                payment_method=payment_method
            )
            # Set the quantity to 0 after the order is created
            item.quantity = 0
            item.save()

        # Clear the cart completely by setting all quantities to 0
        cart_items.update(quantity=0)

        # Show success message
        messages.success(request, "Order placed successfully!")
        
        return render(request, 'place_order.html', {
            'cart_items': cart_items,
            'total_price': total_price,
        })

    return render(request, 'place_order.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required(login_url='/login/')
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'order_history.html', context)

def serialize_decimal(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

from django.http import JsonResponse

@login_required(login_url='/login/')
def add_to_cart(request, dish_id):
    if request.method == 'POST':
        try:
            # Get the dish and quantity from the POST request
            dish = Dish.objects.get(id=dish_id)
            quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is provided
            
            # Check if the user already has the dish in the cart
            cart_item, created = Cart.objects.get_or_create(user=request.user, dish=dish)
            
            # If the item already exists, update the quantity
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            return JsonResponse({"success": True, "message": "Dish added to cart"})
        except Dish.DoesNotExist:
            return JsonResponse({"success": False, "message": "Dish not found"})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
        else:
            messages.error(request, "There was an error updating your profile.")
            print(form.errors)  # Debug print to track form errors
    else:
        form = UserProfileForm(instance=request.user)

    # Debugging: Make sure the form is correctly populated with user data
    print(request.user.first_name, request.user.last_name, request.user.email)  # Check the logged-in user

    return render(request, 'profile.html', {'form': form})
