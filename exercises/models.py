from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from accounts.models import CustomUser


class Esercizi(models.Model):
    class EnumCategory(models.TextChoices):
        Arm = "AR", _("Arm")
        Abdomen = "AB", _("Abdomen")
        Leg = "L", _("Leg")

    ExID = models.IntegerField(default=0, unique=True, db_index=True)
    category = models.CharField(max_length=2, choices=EnumCategory.choices, default=EnumCategory.Arm)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    ripetizioni = models.IntegerField(default=1)
    carico = models.IntegerField(default=0)
    isDefault = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})


class Scheda(models.Model):
    NomeScheda = models.CharField(max_length=255)
    isDefault = models.BooleanField(default=True)

    def __str__(self):
        return self.NomeScheda

class SchedaAssign(models.Model):
    Esercizio = models.ForeignKey(Esercizi, on_delete=models.CASCADE)
    Scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)
    Username = models.TextField(max_length=256, default="Pippo")
    IsDone = models.BooleanField(default=False)

    def __str__(self):
        return self.Scheda.NomeScheda + " : " + self.Esercizio.name

class UserAssign(models.Model):
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)    # scheda assegnata

    def __str__(self):
        return self.User.username + " : " + self.Scheda.NomeScheda

class ExUserAssign(models.Model):
    ExRef = models.ForeignKey(Esercizi, on_delete=models.CASCADE)
    UserRef = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    IsDone = models.BooleanField(default=False)