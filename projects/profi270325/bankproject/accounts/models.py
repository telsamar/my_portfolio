from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField("ФИО", max_length=255, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    consent = models.BooleanField("Согласие на обработку персональных данных", default=False)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CatalogItem(models.Model):
    name = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAY_CHOICES = [
        ('cash', 'наличными'),
        ('card', 'картой'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, verbose_name="Товар")
    
    fio = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    address = models.CharField("Адрес доставки", max_length=255)
    
    payment_type = models.CharField("Способ оплаты", max_length=10, choices=PAY_CHOICES)
    created_at = models.DateTimeField("Дата заказа", auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.pk} от {self.user.username}"
