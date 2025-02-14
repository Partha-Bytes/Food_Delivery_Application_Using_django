from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Dish, Menu, Order, Cart
from django.contrib.auth.models import User
from .models import Review


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['dish_name', 'price', 'availability', 'dish_dis', 'dish_image']
        widgets = {
            'dish_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dish_dis': forms.Textarea(attrs={'class': 'form-control'}),
            # 'dish_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'dish_image': forms.URLInput(attrs={'class': 'form-control'}),
            
        }
        labels = {
            'dish_name': 'Item Name',
            'price': 'Price',
            'availability': 'Available',
            'dish_dis': 'Description',
            'dish_image': 'Image',
        }
        
        
        
        
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['quantity']
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'quantity': 'Quantity',
        }
        
        
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'quantity': 'Quantity',
        }
        
class UpdateCartItemForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]), 
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 50}),  
        }