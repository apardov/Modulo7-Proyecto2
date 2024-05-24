from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# import el manager que me permitira la creacion de usuarios y super usuarios
from .managers import CustomEmailUserManager


# Create your models here.
class CustomEmailUser(AbstractUser):
    # desabilito el campo username
    username = None
    # agrego el campos email como unico y sera el pricipal
    email = models.EmailField(_('correo electronico'), unique=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre_completo = models.CharField(max_length=255)

    # coloco email como identificador unico
    USERNAME_FIELD = 'email'
    # campos que se pueden definir como requerido pero como tengo el email solo
    # colocare ese
    REQUIRED_FIELDS = []

    # especifico que todos lo modelos provienen de mi manager CustomEmailUserManager
    objects = CustomEmailUserManager()

    # mostrar el nombre del campo email, como correo electronico con el metodo str
    # que pasa un queryset a string
    def __str__(self):
        return self.email


# Modelo de productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Otros atributos según tus necesidades (imagen, categoría, etc.)

    def __str__(self):
        return self.nombre


# Modelo de pedidos
class Pedido(models.Model):
    cliente = models.ForeignKey(CustomEmailUser, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    numero_pedido = models.CharField(max_length=20, unique=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "Pendiente"),
            ("preparacion", "En Preparación"),
            ("despacho", "En Despacho"),
            ("entregado", "Entregado"),
        ],
    )
    direccion_entrega = models.TextField()
    forma_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"Pedido #{self.numero_pedido}"


# Modelo de detalle de pedidos
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto} (Pedido #{self.pedido.numero_pedido})"
