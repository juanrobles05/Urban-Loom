from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, ProfileForm, UserForm, ShippingAddressForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import ShippingAddress
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from core.utils.lang import load_translation
import json


def register_user(request):
    # Cargar traducciones según el idioma activo
    lang = getattr(request, 'LANGUAGE_CODE', 'es')
    t = load_translation(lang)
    
    success_message = None
    error_message = None
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            success_message = t.get('AUTH_REGISTER_SUCCESS', 'Account created successfully! You can now sign in.')
            print(success_message)
            form = UserRegistrationForm()  # Limpiar el formulario
        else:
            if not form.errors:
                error_message = t.get('AUTH_REGISTER_ERROR', 'There was a problem creating your account. Please try again.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {
        'form': form,
        'success_message': success_message,
        'error_message': error_message,
    })

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    # Cargar traducciones según el idioma activo
    lang = getattr(request, 'LANGUAGE_CODE', 'es')
    t = load_translation(lang)
    
    user = request.user

    # Obtener o crear el perfil del usuario
    try:
        profile = user.profile
    except:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, t.get('PROFILE_UPDATE_SUCCESS', '¡Perfil actualizado exitosamente!'))
            return redirect('profile')
        else:
            messages.error(request, t.get('PROFILE_UPDATE_ERROR', 'Por favor corrige los errores en el formulario.'))
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.userprofile  # o Profile si tu modelo se llama así

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def add_shipping_address(request):
    print(f"add_shipping_address called with method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"POST data: {request.POST}")

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            print(f"Address saved successfully: {address}")

            # Check if it's an AJAX request by looking at Accept header
            if 'application/json' in request.headers.get('Accept', ''):
                print("Returning JSON response")
                return JsonResponse({'success': True, 'message': 'Dirección agregada exitosamente'})

            return redirect('profile')
        else:
            if 'application/json' in request.headers.get('Accept', ''):
                print("Returning JSON error response")
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ShippingAddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})

@login_required
def list_shipping_addresses(request):
    addresses = request.user.shipping_addresses.all()
    return render(request, 'accounts/list_addresses.html', {'addresses': addresses})

@login_required
def edit_shipping_address(request, address_id):
    try:
        address = ShippingAddress.objects.get(id=address_id, user=request.user)
    except ShippingAddress.DoesNotExist:
        if 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': False, 'message': 'Dirección no encontrada'})
        return redirect('profile')

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()

            # Check if it's an AJAX request
            if 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({'success': True, 'message': 'Dirección actualizada exitosamente'})

            return redirect('profile')
        else:
            if 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'accounts/edit_address.html', {'form': form})

@login_required
def delete_shipping_address(request, address_id):
    try:
        address = ShippingAddress.objects.get(id=address_id, user=request.user)
    except ShippingAddress.DoesNotExist:
        if 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': False, 'message': 'Dirección no encontrada'})
        return redirect('profile')

    if request.method == 'POST':
        address.delete()

        # Check if it's an AJAX request
        if 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': True, 'message': 'Dirección eliminada exitosamente'})

        return redirect('profile')

    return render(request, 'accounts/delete_address.html', {'address': address})