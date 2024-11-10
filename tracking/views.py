from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from .utils import generate_tracking_pdf
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Product, Notification
from .forms import ProductForm, BitcoinPaymentForm
from .models import Product, BitcoinPayment, BitcoinWallet

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        
        new_password = request.POST.get('new_password')
        if new_password:
            if new_password == request.POST.get('confirm_password'):
                user.set_password(new_password)
            else:
                messages.error(request, 'Passwords do not match')
                return render(request, 'tracking/profile.html')
        
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('tracking:profile')
    
    return render(request, 'tracking/profile.html')

def logout_view(request):
    logout(request)
    return redirect('tracking:home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tracking:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracking/auth/register.html', {'form': form})

@login_required
def dashboard(request):
    shipments = Product.objects.filter(user=request.user)
    in_transit_count = shipments.filter(current_status='in_transit').count()
    delivered_count = shipments.filter(current_status='delivered').count()
    
    # Get unread notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            product = Product.objects.get(tracking_number=tracking_number)
            return render(request, 'tracking/tracking_result.html', {'product': product})
        except Product.DoesNotExist:
            context = {
                'shipments': shipments,
                'in_transit_count': in_transit_count,
                'delivered_count': delivered_count,
                'notifications': notifications,
                'error': 'Invalid tracking number'
            }
            return render(request, 'tracking/dashboard.html', context)
    
    context = {
        'shipments': shipments,
        'in_transit_count': in_transit_count,
        'delivered_count': delivered_count,
        'notifications': notifications,
    }
    return render(request, 'tracking/dashboard.html', context)

@login_required
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)


def home(request):
    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number')
        try:
            product = Product.objects.get(tracking_number=tracking_number)
            return render(request, 'tracking/tracking_result.html', {'product': product})
        except Product.DoesNotExist:
            return render(request, 'tracking/home.html', {'error': 'Invalid tracking number'})
    return render(request, 'tracking/home.html')

def tracking_detail(request, tracking_number):
    try:
        product = Product.objects.get(tracking_number=tracking_number)
        return render(request, 'tracking/tracking_result.html', {'product': product})
    except Product.DoesNotExist:
        raise Http404("Tracking number not found")

def download_pdf(request, tracking_number):
    try:
        product = Product.objects.get(tracking_number=tracking_number)
        pdf = generate_tracking_pdf(product)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="tracking_{tracking_number}.pdf"'
        return response
    except Product.DoesNotExist:
        raise Http404("Tracking number not found")


@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        payment_form = BitcoinPaymentForm(request.POST)
        
        if product_form.is_valid() and payment_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            
            payment = payment_form.save(commit=False)
            payment.product = product
            payment.user = request.user
            payment.save()
            
            messages.success(request, f'Product created successfully. Tracking number: {product.tracking_number}. Payment proof submitted for review.')
            return redirect('tracking:dashboard')
    else:
        product_form = ProductForm()
        payment_form = BitcoinPaymentForm()
    
    bitcoin_wallet = BitcoinWallet.objects.filter(is_active=True).first()
    
    context = {
        'product_form': product_form,
        'payment_form': payment_form,
        'bitcoin_wallet': bitcoin_wallet.address if bitcoin_wallet else None
    }
    return render(request, 'tracking/add_product.html', context)
