from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from django import forms

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        
        return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Get in Touch",
            "email": "info@onlinestore.com",
            "address": "123 Main Street, Suite 100<br>New York, NY 10001<br>United States",
            "phone": "+1 (555) 123-4567",
        })
        
        return context


class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":"$599.99"},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":"$999.99"},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":"$49.99"},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":"$199.99"}
    ]

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] =  "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1 or product_id > len(Product.products):
                return HttpResponseRedirect(reverse('home'))
            
            product = Product.products[product_id-1]
            viewData = {}
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] =  product["name"] + " - Product information"
            viewData["product"] = product

            return render(request, self.template_name, viewData)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect('success')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class SuccessView(TemplateView):
    template_name = 'products/success.html'
