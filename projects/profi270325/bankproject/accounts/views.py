from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, CatalogItem, Order
from .forms import UserRegistrationForm
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



@login_required(login_url='login')
def reviews(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Review.objects.create(user=request.user, text=text)
            messages.success(request, 'Спасибо! Ваш отзыв сохранён.')
            return redirect('reviews')
        else:
            messages.error(request, 'Введите текст перед отправкой.')
    return render(request, 'reviews.html')



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse('home')





@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/accounts/login/')
def catalog(request):
    items = CatalogItem.objects.all()
    return render(request, 'catalog.html', {'items': items})

@login_required(login_url='/accounts/login/')
def contacts(request):
    return render(request, 'contacts.html')


@login_required(login_url='/accounts/login/')
def order_item(request, item_id):
    item = get_object_or_404(CatalogItem, id=item_id)

    if request.method == 'POST':
        fio = request.POST.get('fio', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        payment_type = request.POST.get('payment_type', '')

        if not fio or not phone or not email or not address or not payment_type:
            messages.error(request, "Заполните все поля формы.")
        else:
            Order.objects.create(
                user=request.user,
                item=item,
                fio=fio,
                phone=phone,
                email=email,
                address=address,
                payment_type=payment_type
            )
            messages.success(request, f"Заказ на {item.name} оформлен!")
            return redirect('catalog')
    return render(request, 'order_form.html', {'item': item})
