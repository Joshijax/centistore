from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Coupon, Images, Order, Products, Category, sub_Category, colors, size
from django.contrib.auth.models import User
from django.contrib import messages
from dashboard.forms import ImageForm, ProductForm, updProductForm, CategoryForm, SubCategoryForm, ColorForm, SizeForm, CouponForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from .mixins import AdminRequiredMixin



class DashboardHomeView(LoginRequiredMixin, AdminRequiredMixin, View):
     """
    Display homepage of the dashboard.
    """
     context = {}
     template_name = 'dashboard/index.html'
     context_object = {}
     def get(self, request, *args, **kwargs):

        product_create_form = ProductForm()
        self.context_object["all_users"] = User.objects.all().order_by("-id")
        self.context_object["all_order"] = Order.objects.all().order_by("-id")
        self.context_object["all_products"] = Products.objects.all()
        self.context_object["sales"] = Order.objects.filter(ordered=True).count()
        self.context_object["product_create_form"] = product_create_form
        self.context_object["product_create_form"] = product_create_form

        return render(request, self.template_name, self.context_object)
     
class ProductDashboardView(LoginRequiredMixin, AdminRequiredMixin, View):
     """
    Display homepage of the dashboard.
    """
     context = {}
     template_name = 'dashboard/products.html'
     context_object = {}
     def get(self, request, *args, **kwargs):

        product_create_form = ProductForm()
        self.context_object["all_users"] = User.objects.all().order_by("-id")
        self.context_object["all_order"] = Order.objects.all().order_by("-id")
        self.context_object["all_products"] = Products.objects.all()
        self.context_object["product_create_form"] = product_create_form
        self.context_object["product_create_form"] = product_create_form

        return render(request, self.template_name, self.context_object)
     


class AddProductsView(LoginRequiredMixin, AdminRequiredMixin, View):

    SAVE_AS_DRAFT = "SAVE_AS_DRAFT"
    PUBLISH = "PUBLISH"

    template_name = 'dashboard/addproducts.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        self.context_object["product_form"] = ProductForm()
        self.context_object["image_form"] = ImageForm()
        

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        product_form = ProductForm(request.POST, request.FILES)
        image_form = ImageForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save()
            if image_form.is_valid():
                for file in request.FILES.getlist('file'):
                    Images.objects.create(post=product, file=file)
            return redirect('dashboard:products')
        else:
            # If ProductForm is not valid, pass the form to the template with errors
            context = {'product_form': product_form, 'image_form': image_form}
            return render(request, 'dashboard/addproducts.html', context)

            # return redirect('dashboard:products', slug=product.slug)
 

class UpdateProductsView(LoginRequiredMixin, AdminRequiredMixin, View):


    template_name = 'dashboard/updProduct.html'
    context_object = {}

    def get(self, request, *args, **kwargs):

        old_product = get_object_or_404(Products, slug=self.kwargs.get("slug"))
        self.context_object["product_images"] = old_product.picture
        self.context_object["product_form"] = updProductForm(instance=old_product)
        self.context_object["image_form"] = ImageForm()
        

        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        old_product = get_object_or_404(Products, slug=self.kwargs.get("slug"))
        product_form = updProductForm(request.POST, request.FILES, instance=old_product)
        image_form = ImageForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            if request.FILES.get('image', None) is None:
                product.image = product.image  # Use previous image if none uploaded
                product.save()
            if image_form.is_valid():
                for file in request.FILES.getlist('file'):
                    Images.objects.create(post=product, file=file)
            messages.success(request, 'Updated product successfully.')
            return redirect('dashboard:updateproduct', slug= self.kwargs.get("slug"))
            
        else:
            # If ProductForm is not valid, pass the form to the template with errors
            messages.error(request, 'error updating product....')
            context = {'product_form': product_form, 'image_form': image_form}
            return redirect('dashboard:updateproduct', slug= self.kwargs.get("slug"))

            # return redirect('dashboard:products', slug=product.slug)
 

class CreateFormsView(LoginRequiredMixin, AdminRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        category_form = CategoryForm()
        subcategory_form = SubCategoryForm()
        color_form = ColorForm()
        size_form = SizeForm()
        coupon_form =CouponForm()
        context = {
            'category_form': category_form,
            'subcategory_form': subcategory_form,
            'color_form': color_form,
            'size_form': size_form,
            "coupon_form":coupon_form
        }
        return render(request, 'dashboard/create_forms.html', context)
    
    def post(self, request, *args, **kwargs):
        category_form = CategoryForm(request.POST)
        subcategory_form = SubCategoryForm(request.POST)
        color_form = ColorForm(request.POST)
        size_form = SizeForm(request.POST)
        coupon_form =CouponForm(request.POST)
        if subcategory_form.is_valid():
            category = subcategory_form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('dashboard:utils_dash')
        elif category_form.is_valid() :
            subcategory = category_form.save()
            messages.success(request, 'Subcategory created successfully.')
            return redirect('dashboard:utils_dash')
        elif color_form.is_valid():
            color = color_form.save()
            messages.success(request, 'Color created successfully.')
            return redirect('dashboard:utils_dash')
        elif size_form.is_valid():
            size = size_form.save()
            messages.success(request, 'Size created successfully.')
            return redirect('dashboard:utils_dash')
        elif coupon_form.is_valid():
            coupon = coupon_form.save()
            messages.success(request, 'Coupon created successfully.')
            return redirect('dashboard:utils_dash')
        else:
            context = {
                'category_form': category_form,
                'subcategory_form': subcategory_form,
                'color_form': color_form,
                'size_form': size_form,
                "coupon_form":coupon_form
            }
            return render(request, 'dashboard/create_forms.html', context)


class ListModelsView(LoginRequiredMixin, AdminRequiredMixin,ListView):
    model = Category
    template_name = 'dashboard/list_models.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = sub_Category.objects.all()
        context['colors'] = colors.objects.all()
        context['sizes'] = size.objects.all()
        context['coupons'] = Coupon.objects.all()
        return context
    

class OrderListView(ListView):
    model = Order
    ordering = ['-ordered_date']
    template_name = 'dashboard/orders.html'
    def get_queryset(self):
        return super().get_queryset().exclude(payment=None)

class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'dashboard/order_detail.html', {'order': order})


@csrf_exempt
def delete_model(request, model, id):
    print(model, "here")
    if request.method == 'POST':
        # Determine which model to delete based on the value of the `model` parameter.
        if model == 'category':
            model_class = Category
        elif model == 'subcategory':
            model_class = sub_Category
        elif model == 'color':
            model_class = colors
        elif model == 'size':
            model_class = size
        elif model == 'order':
            model_class = Order
        elif model == 'coupons':
            model_class = Coupon
        elif model == 'image':
            model_class = Images
        elif model == 'product': 
            model_class = Products
        else:
            return JsonResponse({'message': 'Invalid model.'}, status=400)
          
        # Attempt to delete the model instance with the given ID.
       
        model_class.objects.get(id=id).delete()
        return JsonResponse({'message': f'{model} deleted successfully.'}, status=200)
    
        return JsonResponse({'message': f'Error deleting {model}.'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid method.'}, status=400)
    
@csrf_exempt
def update_status(request, status, id):
    try:
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
        messages.success(request, 'message: Succesfully updated order status')
        return redirect('dashboard:order_list')
    except:
        messages.error(request, 'message: Error Uodating.')
        return redirect('dashboard:order_list')
   

@csrf_exempt
def update_status_in(request, status, id):
    try:
        order = Order.objects.get(id=id)
        order.status = status
        order.save()
        messages.success(request, 'message: Succesfully updated order status')
        return redirect('dashboard:ord_details', pk=id)
    except:
        messages.error(request, 'message: Error Uodating.')
        return redirect('dashboard:ord_details', pk=id)
   
