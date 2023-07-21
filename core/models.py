from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils.html import escape
from colorfield.fields import ColorField
from django.utils.html import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

STATUS_CHOICES = (
    ('DS', 'Dispatched'),
    ('IT', 'In transit'),
    ('DL', 'Delivered'),
    ('PR', 'Processing'),
    ('CL', 'Cancelled'),
)


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device
        return str(name)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class sub_Category(models.Model):
    category = models.ForeignKey(Category, related_name="sub_cat",
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " for " + self.category.name

    def get_absolute_url(self):
        return reverse("core:category_prod", kwargs={
            'slug': self.name,
            "cate": self.category.name
        })


class colors(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class size(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.symbol


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    category = models.ForeignKey(sub_Category,
                                 on_delete=models.CASCADE)
    colors = models.ManyToManyField(colors, blank=True)
    size = models.ManyToManyField(size, blank=False)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-first-to-cart", kwargs={
            'slug': self.slug
        })

    def get_first_add_to_cart_url(self):
        return reverse("core:add-first-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name, allow_unicode=True)

        super(Products, self).save(*args, **kwargs)


class Images(models.Model):
    post = models.ForeignKey(
        Products, related_name="picture", on_delete=models.CASCADE,)
    file = models.FileField(upload_to='', null=True, blank=True)

    def file_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % (self.file.url))


class Variants(models.Model):
    product = models.ForeignKey(
        Products, related_name="Variant_product", on_delete=models.CASCADE,)
    color = models.ForeignKey(
        colors, related_name="Variant_color", on_delete=models.CASCADE,)
    size = models.ForeignKey(
        size, related_name="Variant_size", on_delete=models.CASCADE,)

    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}, color {self.color.name}, size {self.size.name}"


class OrderItem(models.Model):
    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Variants, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.product.name} variant color {self.item.color.name } size {self.item.size.name }"

    def get_total_item_price(self):
        if self.item.stock < self.quantity:
            return 0
        return self.quantity * self.item.product.price

    def get_total_item_price2(self):
        # print(self.quantity, self.item.product.price)
        return self.quantity * self.item.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.product.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):

        return self.get_total_item_price()


class LocationPrice(models.Model):
    state = models.CharField(blank=False, max_length=1000)
    price = models.FloatField()

    def __str__(self):
        return self.state


class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)
    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(
        LocationPrice, on_delete=models.SET_NULL, null=True, blank=True)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    phone_number = models.CharField(blank=True, max_length=15)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=3, default='PR')

    '''
    1. Products added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.device

    def view_details(self):
        url = reverse('dashboard:ord_details', args=[self.pk])
        return mark_safe('<a target="_blank" href="%s">View Details</a>' % (url))

    view_details.short_description = 'Order Details'  # Set the column header name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        if self.location:
            total += self.location.price

        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_total2(self):
        total = 0
        for order_item in self.items.all():
            # print("hereeeeeee", order_item.get_total_item_price2())
            total += order_item.get_total_item_price2()

        if self.location:
            total += self.location.price

        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_qty(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity

        return total

    def get_total_without(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

        return total


class Address(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE)
    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.street_address + " ," + str(self.country.name) + " , zip code: " + self.zip

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    trx_ref = models.CharField(max_length=50, unique=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.SET_NULL, blank=True, null=True)

    user = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    status = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "payed ₦"+str(self.amount)+" trx_ref: "+self.trx_ref


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
        userprofile = Customer.objects.create()


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
