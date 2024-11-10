from django import forms
from .models import BitcoinPayment, Product, PricingPlan

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sender_name',
            'sender_address',
            'recipient_name',
            'recipient_address',
            'pricing_plan'
        ]
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sender name'
            }),
            'sender_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete sender address'
            }),
            'recipient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipient name'
            }),
            'recipient_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete recipient address'
            }),
            'pricing_plan': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pricing_plan'].queryset = PricingPlan.objects.all()
        self.fields['pricing_plan'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation logic here if needed
        return cleaned_data

class BitcoinPaymentForm(forms.ModelForm):
    class Meta:
        model = BitcoinPayment
        fields = ['payment_proof']
        widgets = {
            'payment_proof': forms.FileInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'accept': 'image/*'
            })
        }