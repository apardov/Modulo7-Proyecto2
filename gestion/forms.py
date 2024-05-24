from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import forms
from .models import CustomEmailUser, Pedido


# definicion de formularios para creacion de usuarios y modificacion de estos
# usando los predefinidos que Django provee
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomEmailUser
        fields = ('email', 'rut', 'nombre_completo')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomEmailUser
        fields = ('email', 'rut', 'nombre_completo')


class PedidoForm(forms.Form):
    class Meta:
        model = Pedido
        fields = '__all__'
