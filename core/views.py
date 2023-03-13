import os
from dotenv import load_dotenv
import math
import random
import string
import requests
from functools import reduce
import operator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import ConnectionError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import logout
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Category, Customer, Products, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, size, sub_Category
from python_flutterwave import payment
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rave_python import Rave
from django.utils.decorators import method_decorator
import environ

from dotenv import load_dotenv
import os
 
load_dotenv()
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


public_key = settings.FLUTTER_TEST_PUBLIC_KEY
secret_key = settings.FLUTTER_TEST_SECRET_KEY
rave = Rave(public_key, secret_key, usingEnv=False)
payment.token = secret_key
auth_token = secret_key


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Products.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


 
class CheckoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, *args, **kwargs):
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            
            order = Order.objects.get(user=customer, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
                'categories': sub_Category.objects.all()[:8],
                'customer': customer
            }

            shipping_address_qs = Address.objects.filter(
                user=customer,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=customer,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "new/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order = Order.objects.get(user=customer, ordered=False)
            if form.is_valid():

                
                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
            

                if use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=customer,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=customer,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")
                        return redirect('core:checkout')

                payment_option = form.cleaned_data.get('payment_option')
                phone = form.cleaned_data.get('phone_number')
                order.phone_number = phone
                order.save()
                if payment_option == 'F':
                    order = Order.objects.get(
                        user=customer, ordered=False)
                    for item in order.items.all():
                        if item.item.stock < item.quantity:
                            item.delete()
                    amount = int(order.get_total())
                    name = form.cleaned_data.get('full_name')
                    email = email = form.cleaned_data.get('email') if self.request.user else (self.request.user.email if form.cleaned_data.get('email')  else 'johndoe@gmail.com')
                    customer.name = name
                    customer.email = email
                    customer.save()
                    return redirect(str(process_flutter_payment(
                        name, email, amount, phone, order)))
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
            print("hello")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class CheckoutView1(View):
    def get(self, *args, **kwargs):
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order = Order.objects.get(user=customer, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=customer,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=customer,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order = Order.objects.get(user=customer, ordered=False)
            if form.is_valid():

                # use_default_shipping = form.cleaned_data.get(
                #     'use_default_shipping')
                # if use_default_shipping:
                #     print("Using the defualt shipping address")
                #     address_qs = Address.objects.filter(
                #         user=self.request.user,
                #         address_type='S',
                #         default=True
                #     )
                #     if address_qs.exists():
                #         shipping_address = address_qs[0]
                #         order.shipping_address = shipping_address
                #         order.save()
                #     else:
                #         messages.info(
                #             self.request, "No default shipping address available")
                #         return redirect('core:checkout')
                # else:
                #     print("User is entering a new shipping address")
                #     shipping_address1 = form.cleaned_data.get(
                #         'shipping_address')
                #     shipping_address2 = form.cleaned_data.get(
                #         'shipping_address2')
                #     shipping_country = form.cleaned_data.get(
                #         'shipping_country')
                #     shipping_zip = form.cleaned_data.get('shipping_zip')

                #     if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                #         shipping_address = Address(
                #             user=self.request.user,
                #             street_address=shipping_address1,
                #             apartment_address=shipping_address2,
                #             country=shipping_country,
                #             zip=shipping_zip,
                #             address_type='S'
                #         )
                #         shipping_address.save()

                #         order.shipping_address = shipping_address
                #         order.save()

                #         set_default_shipping = form.cleaned_data.get(
                #             'set_default_shipping')
                #         if set_default_shipping:
                #             shipping_address.default = True
                #             shipping_address.save()

                #     else:
                #         messages.info(
                #             self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                # same_billing_address = form.cleaned_data.get(
                #     'same_billing_address')

                # if same_billing_address:
                #     billing_address = shipping_address
                #     billing_address.pk = None
                #     billing_address.save()
                #     billing_address.address_type = 'B'
                #     billing_address.save()
                #     order.billing_address = billing_address
                #     order.save()

                if use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=customer,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=customer,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')
                payment_option = form.cleaned_data.get('payment_option')
                print(payment_option)

                if payment_option == 'F':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")






@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status = request.GET.get('status', None)
    tx_ref = request.GET.get('tx_ref', None)
    current_url = request.build_absolute_uri()
    
    if status == "cancelled":
        messages.info(request, "AN error occured, payment not successful!")
        return redirect("core:home")
    try:
        val = rave.Card.verify(tx_ref)
    except ConnectionError as e:    # This is the correct syntax
        redirect(str(current_url))

    print(current_url)
    try:
        customer = request.user.customer	
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order = Order.objects.get(user=customer, ordered=False)

    if status != "successful":
        messages.info(request, "AN error occured, payment not successful!")
        return redirect("/")

    if not val["transactionComplete"]:
        messages.info(
            request, f"AN error occured, not verified your transaction ref: {tx_ref}!")
        return redirect("/")
    print(status)
    print(tx_ref)

    try:
        # create the payment
        payment = Payment()
        payment.trx_ref = tx_ref
        payment.status = status
        payment.user = customer
        payment.amount = order.get_total()
        payment.save()
    except IntegrityError as e:
        print(e, 'hereee')
        if 'UNIQUE constraint' in str(e):
            messages.info(
                request, f"Payment for transaction {tx_ref} already exist!")
            return redirect("/")

    # assign the payment to the order
    for item in order.items.all():
        item.item.stock -= item.quantity
        item.item.sold += item.quantity
        item.item.save()

    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()

    order.ordered = True
    order.payment = payment
    order.ref_code = request.GET.get('tx_ref', None)
    order.save()

    messages.success(request, "Your order was successful!")
    return redirect("/")


class HomeView(ListView):
    model = Products
    paginate_by = 10
    template_name = "index.html"
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(HomeView, self).get_context_data(**kwargs)

        context['categories'] = sub_Category.objects.all()[:8]

        context['bestseller'] = Products.objects.filter().order_by('-sold')

        context['thisweek'] = Products.objects.filter().order_by('-id')[:6]

        context['explore'] = Products.objects.filter().order_by('-id')[:20]
        context['explore2'] = Products.objects.filter().order_by('-id')[8:8]
        # context['cate'] = Products.objects.filter().order_by('-id')[8:8]

        return context



def process_flutter_payment(name, email, amount, phone, order):

    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
        "tx_ref": ''+str(math.floor(1000000 + random.random()*9000000)),
        "amount": amount,
        "currency": "NGN",
        "redirect_url": "https://www.centiastore.com/callback",
        "payment_options": "card",
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": phone,
            "name": name
        },
        "customizations": {
            "title": "Centistore",
            "description": "Best store in town",
            "logo": "http://www.centiastore.com/static/assets/images/logo/cent.png"
        },
        "order_info": {
            "order_id": order.id,
            "items": [
                {"name": item.item.name, "quantity": item.quantity, "price": item.item.price} for item in order.items.all()
            ]
        }
    }
    url = ' https://api.flutterwave.com/v3/payments'
    print(url)
    response = requests.post(url, json=data, headers=hed)
    response = response.json()
    link = response['data']['link']
    return link



# def process_flutter_payment(name, email, amount, phone):

#     hed = {'Authorization': 'Bearer ' + auth_token}
#     data = {
#         "tx_ref": ''+str(math.floor(1000000 + random.random()*9000000)),
#         "amount": amount,
#         "currency": "NGN",
#         "redirect_url": "https://www.centiastore.com/callback",
#         "payment_options": "card",
#         "meta": {
#             "consumer_id": 23,
#             "consumer_mac": "92a3-912ba-1192a"
#         },
#         "customer": {
#             "email": email,
#             "phonenumber": phone,
#             "name": name
#         },
#         "customizations": {
#             "title": "Centistore",
#             "description": "Best store in town",
#             "logo": "http://www.centiastore.com/static/assets/images/logo/cent.png"
#         }
#     }
#     url = ' https://api.flutterwave.com/v3/payments'
#     print(url)
#     response = requests.post(url, json=data, headers=hed)
#     response = response.json()
#     link = response['data']['link']
#     return link


class HomeView2(ListView):
    model = Products
    paginate_by = 10
    template_name = "home.html"


class ShopView(ListView):
    model = Products
    paginate_by = 8
    context_object_name = 'product_list'
    template_name = "new/shop.html"
    ordering = ['-id']

    def get_queryset(self):
        print("prod-search")
        query = self.request.GET.get('prod-search')
        self.query = query

        if query:
            query_list = query.split()
            search_results = Products.objects.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(category__name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(category__category__name__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter()
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter()
        else:
            # messages.error(
            #     self.request, f"Sorry you did not enter any keyword")
            return Products.objects.filter().order_by('-id')

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ShopView, self).get_context_data(**kwargs)

        context['categories'] = sub_Category.objects.all()[:8]

        context['bestseller'] = Products.objects.filter().order_by('-sold')

        context['thisweek'] = Products.objects.filter().order_by('-id')[:6]

        context['query'] = self.query

        context['explore'] = Products.objects.filter().order_by('-id')[:8]
        context['explore2'] = Products.objects.filter().order_by('-id')[8:8]
        # context['cate'] = Products.objects.filter().order_by('-id')[8:8]

        return context


class SearchView(ListView):
    model = Products
    paginate_by = 8
    template_name = "new/search.html"
    context_object_name = 'product_list'
    ordering = ['-id']

    def get_queryset(self):
        print("prod-search")
        query = self.request.GET.get('prod-search')
        self.query = query

        if query:
            query_list = query.split()
            search_results = Products.objects.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(category__name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(category__category__name__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter()
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter()
        else:
            messages.error(
                self.request, f"Sorry you did not enter any keyword")
            return []

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ShopView, self).get_context_data(**kwargs)

        context['categories'] = sub_Category.objects.all()[:8]

        context['bestseller'] = Products.objects.filter().order_by('-sold')

        context['thisweek'] = Products.objects.filter().order_by('-id')[:6]

        context['explore'] = Products.objects.filter().order_by('-id')[:8]
        context['explore2'] = Products.objects.filter().order_by('-id')[8:8]
        # context['cate'] = Products.objects.filter().order_by('-id')[8:8]

        return context


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order = Order.objects.get(user=customer, ordered=False)
            context = {
                'object': order,
                'couponform': CouponForm(),
            }
            return render(self.request, 'new/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class OrderSummaryView2(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            try:
                customer = self.request.user.customer	
            except:
                device = self.request.COOKIES['device']
                customer, created = Customer.objects.get_or_create(device=device)
            order = Order.objects.get(user=customer, ordered=False)
            context = {
                'object': order,
                'couponform': CouponForm()
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Products
    template_name = "new/product_view.html"

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ItemDetailView, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        context['bestseller'] = Products.objects.filter().order_by('-sold')

        context['also_like'] = Products.objects.filter(
            category=context["object"].category).order_by('-id')[:6]

        return context


class ItemDetailView1(DetailView):
    model = Products
    template_name = "product.html"

@csrf_exempt
def add_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)

    if item.stock > 0:
        try:
            customer = request.user.customer	
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=customer,
            ordered=False
        )
        
        order_qs = Order.objects.filter(user=customer, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()

            order = Order.objects.create(
                user=customer, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "This item out of Stock.")
        return redirect("core:order-summary")


@csrf_exempt
def add_first_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    sizes = request.POST.get('size', False)
    print(sizes)
    val_size = None
    if sizes:
        val_size = get_object_or_404(size, name=sizes)
    else:
        return redirect("core:product", slug=slug)
    print(val_size)
    try:
        customer = request.user.customer	
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    
    current_url = request.META.get('HTTP_REFERER')

    orderI = OrderItem.objects.filter(
            item=item,
            user=customer,
            ordered=False
        )
    ordered_stock= 0
    for ord in orderI:
        ordered_stock += ord.quantity

    if item.stock - ordered_stock > 0:
       
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            size=val_size,
            user=customer,
            ordered=False
        )
        
        
        order_qs = Order.objects.filter(user=customer, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            checker = order.items.filter(item__slug=item.slug).exists()
            if sizes != "null":
                checker = order.items.filter(item__slug=item.slug, size__name=val_size.name).exists()
            # check if the order item is in the order
            if checker:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "This item was added to your cart.")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=customer, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "This item out of Stock.")
        return redirect("core:order-summary")


def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    try:
        customer = request.user.customer	
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order_qs = Order.objects.filter(
        user=customer,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=customer,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    try:
        customer = request.user.customer	
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order_qs = Order.objects.filter(
        user=customer,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=customer,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        if Coupon.objects.filter(code=code).exists():
            coupon = Coupon.objects.get(code=code)
            return coupon
        return False
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            # print("okayyyyyyyyyyyyyyyyyyy")
            current_url = self.request.META.get('HTTP_REFERER')
            print(current_url)
            try:
                try:
                    customer = self.request.user.customer	
                except:
                    device = self.request.COOKIES['device']
                    customer, created = Customer.objects.get_or_create(device=device)
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=customer, ordered=False)
                val_coupon = get_coupon(self.request, code)
                if(val_coupon):
                    order.coupon = get_coupon(self.request, code)
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                    return redirect(current_url)
                messages.info(self.request, "Invalid Coupoun code")
                return redirect(current_url)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


class CategoryArticlesListView(ListView):
    model = Products
    paginate_by = 6
    context_object_name = 'product_list'
    # template_name = 'blog/category/category_articles.html'
    template_name = 'new/category_view.html'

    def get_queryset(self):
        category = get_object_or_404(
            sub_Category, name=self.kwargs.get('slug'))
        return Products.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesListView,
                        self).get_context_data(**kwargs)
        context['categories'] = sub_Category.objects.all()[:8]

        context['bestseller'] = Products.objects.filter().order_by('-sold')

        context['thisweek'] = Products.objects.filter().order_by('-id')[:6]

        context['explore'] = Products.objects.filter().order_by('-id')[:8]
        context['explore2'] = Products.objects.filter().order_by('-id')[8:8]
        return context


def logout_request(request):

    logout(request)

    return redirect('core:home')
