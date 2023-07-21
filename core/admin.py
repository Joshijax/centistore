from django.contrib.admin import ModelAdmin
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Customer, LocationPrice, Products, OrderItem, Variants, size, Order, Payment, Coupon, Refund, Address, UserProfile, sub_Category, Category, colors, Images


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'state',
        'price'
    ]
    list_display_links = [
        'state',
        'price'
    ]
    # readonly_fields = ('shipping_address',
    #                 'billing_address', "items")
    list_filter = [
        'state',
        'price'
    ]
    search_fields = [
        'state',
        'price'
    ]


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.pk:
            selected_items = instance.items.all()
            self.fields['items'].queryset = selected_items


class OrderAdmin(admin.ModelAdmin):
    list_display = ['view_details', 'user', 'ordered', 'location', 'being_delivered',
                    'received', 'refund_requested', 'refund_granted', 'payment', 'coupon']
    list_display_links = ['user', 'payment', 'coupon']
    list_filter = ['ordered', 'being_delivered',
                   'received', 'refund_requested', 'refund_granted']
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted]
    readonly_fields = ('view_details',)
    form = OrderAdminForm

    # def view_details(self, obj):
    #     url = reverse('ord_details', args=[obj.pk])
    #     return format_html('<a href="{}">View Details</a>', url)

    # view_details.short_description = 'Order Details'  # Set the column header name


class variantInline(admin.StackedInline):
    model = Variants
    can_delete = False
    verbose_name_plural = 'Variant_product'
    fk_name = 'product'
    # readonly_fields = ('file_tag',)


class imagesInline(admin.StackedInline):
    model = Images
    can_delete = False
    verbose_name_plural = 'picture'
    fk_name = 'post'
    readonly_fields = ('file_tag',)


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class productAdmin(admin.ModelAdmin):
    # fields = ('image_tag', )
    inlines = [imagesInline, variantInline]
    search_fields = ['name', 'description']
    list_display = [
        'image_tag',
        'name',
        'stock'
    ]
    readonly_fields = ('image_tag',)


class productImageAdmin(admin.ModelAdmin):
    # fields = ('image_tag', )
    list_display = [
        'file_tag',
    ]
    readonly_fields = ('file_tag',)


admin.site.register(Products, productAdmin)
admin.site.register(sub_Category)
admin.site.register(Images, productImageAdmin)
admin.site.register(colors)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(size)
admin.site.register(Refund)
admin.site.register(Customer)
admin.site.register(Variants)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(LocationPrice, LocationAdmin)
