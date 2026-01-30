from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import ShortURL
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from .forms import ShortURLForm, CustomShortURLForm, UserRegistrationForm
import qrcode


# Create your views here.


def register(request):
    if request.method == 'POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,'Account created successfully!!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, usernaminite=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
        

@login_required
def dashboard_view(request):
    urls = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html',{'urls' : urls})


@login_required
def create_url(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            url_obj = form.save(commit=False)
            url_obj.user = request.user
            url_obj.short_key = ShortURL.generate_short_key()
            url_obj.save()
            messages.success(request, 'Short URL created successfully!')
            return redirect('dashboard')
    else:
        form = ShortURLForm()
    return render(request, 'create_url.html', {'form': form})

@login_required
def create_custom_url(request):
    if request.method == 'POST':
        form = CustomShortURLForm(request.POST)
        if form.is_valid():
            custom_key = form.cleaned_data['short_key']
            if ShortURL.objects.filter(short_key=custom_key).exists():
                messages.error(request, 'This custom key is already taken. Please choose another.')
            else:
                url_obj = form.save(commit=False)
                url_obj.user = request.user
                url_obj.custom_key = True
                url_obj.save()
                messages.success(request, 'Custom short URL created successfully!')
                return redirect('dashboard')
    else:
        form = CustomShortURLForm()
    return render(request, 'create_custom_url.html', {'form': form})

@login_required
def edit_url(request, pk):
    url_obj = get_object_or_404(ShortURL, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShortURLForm(request.POST, instance=url_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Short URL updated successfully!')
            return redirect('dashboard')
    else:
        form = ShortURLForm(instance=url_obj)
    return render(request, 'edit_url.html', {'form': form})

@login_required
def delete_url(request, pk):
    url_obj = get_object_or_404(ShortURL, pk=pk, user=request.user)
    if request.method == 'POST':
        url_obj.delete()
        messages.success(request, 'Short URL deleted successfully!')
        return redirect('dashboard')
    return render(request, 'delete_url.html', {'url': url_obj})

def redirect_url(request, short_key):
    try:
        url_obj = ShortURL.objects.get(short_key=short_key)
        if url_obj.is_expired():
            messages.error(request, 'This short URL has expired.')
            return redirect('login')  # Or a custom expired page
        url_obj.click_count += 1
        url_obj.save()
        return HttpResponseRedirect(url_obj.original_url)
    except ShortURL.DoesNotExist:
        raise Http404("Short URL not found.")

@login_required
def generate_qr(request, pk):
    url_obj = get_object_or_404(ShortURL, pk=pk, user=request.user)
    short_url = request.build_absolute_uri(reverse('redirect_url', args=[url_obj.short_key]))
    qr = qrcode.QRCode()
    qr.add_data(short_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    response = HttpResponse(content_type='image/png')
    img.save(response, 'PNG')
    return response