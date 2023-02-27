from django import forms

from core.models import Images, Products, Category, sub_Category, colors, size, Coupon



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code',"amount")
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = sub_Category
        fields = ('category', 'name')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ColorForm(forms.ModelForm):
    class Meta:
        model = colors
        fields = ('name', 'color')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }

class SizeForm(forms.ModelForm):
    class Meta:
        model = size
        fields = ('name', 'symbol')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('name', 'price', 'discount_price', 'category', 'colors', 'size', 'description', 'stock', 'image')


class updProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('name', 'price', 'discount_price', 'category', 'colors', 'size', 'description', 'stock', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

 
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True, 'accept':"image/*", "onchange":"useFileReader(this.files)"})
        }  