from django import forms
from .models import BitcoinPayment, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sender_name',
            'sender_address',
            'recipient_name',
            'recipient_address'
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
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        # You can add custom validation logic here if needed
        return cleaned_data
    
class BitcoinPaymentForm(forms.ModelForm):
    class Meta:
        model = BitcoinPayment
        fields = ['payment_proof']
        widgets = {
            'payment_proof': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'rows': 3,
                'placeholder': 'Paste your transaction ID or describe your payment proof'
            })
        }