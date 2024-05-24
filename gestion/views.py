from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm
from .models import Pedido


# Create your views here.
def home(request):
    return render(request, template_name='gestion/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # genero una copia del formulario, ya que es inmutable por eso utilizo copy()
        form.data = form.data.copy()
        # accedo a los campos password 1 y 2 y les asigno una temporal para poder pasar la validacion
        # del form.is_valid()
        form.data['password1'] = settings.PASSWORD_TEMPORAL
        form.data['password2'] = settings.PASSWORD_TEMPORAL
        if form.is_valid():
            print('estoy aca')
            user = form.save(commit=False)
            temp_password = get_random_string(8)
            user.set_password(temp_password)
            user.save()
            send_mail(
                'Tu contraseña Temporal - Te Lo vendo',
                f'Hola {user.email}, aqui está tu contraseña temporal: {temp_password}\n Por favor cambia esta contraseña tras iniciar sesión por primera vez',
                'no-contestar@mailtrap.io',
                [user.email],
                fail_silently=False
            )
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'gestion/register.html', {'form': form})


class EmailLoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('authenticated')
    template_name = 'gestion/login.html'


class EmailLogoutView(LogoutView):
    template_name = 'gestion/logout.html'
    next_page = 'logout'


@login_required(login_url='login')
def authenticated(request):
    pedidos_view = Pedido.objects.all()
    print(pedidos_view)
    if pedidos_view.exists():
        return render(request, 'gestion/authenticated.html', context={'pedidos': pedidos_view})
    else:
        message = "No hay elementos que mostrar"
        return render(request, 'gestion/authenticated.html', context={'message': message})
