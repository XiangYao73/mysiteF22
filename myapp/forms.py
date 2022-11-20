from django import forms
from .models import Order, Client, Product
from django.core.validators import MinValueValidator


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']

    # client = forms.ModelChoiceField(widget=forms.RadioSelect,queryset=Client.objects.all(),to_field_name="username",label='Client name')
    # product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('id'),to_field_name="name")
    # num_units = forms.IntegerField(label='Quantity')


class InterestForm(forms.Form):
    INT_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=INT_CHOICES)
    quantity = forms.IntegerField(initial=1, min_value=0)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)