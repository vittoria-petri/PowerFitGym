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

    class EnumCarico(models.TextChoices):
        C10 = "C10", _("10 kg")
        C20 = "C20", _("20 kg")
        C30 = "C30", _("30 kg")

    ExID = models.IntegerField(default=0)
    category = models.CharField(max_length=2, choices=EnumCategory.choices, default=EnumCategory.Arm)
    name = models.CharField(max_length=255)
    description = models.TextField()
    ripetizioni = models.IntegerField(default=0)
    carico = models.TextField(choices=EnumCarico.choices, default=EnumCarico.C10)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})


class Scheda(models.Model):
    NomeScheda = models.CharField(max_length=255)

    def __str__(self):
        return self.NomeScheda

class SchedaAssign(models.Model):
    Esercizio = models.ForeignKey(Esercizi, on_delete=models.CASCADE)
    Scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)

    def __str__(self):
        return self.Scheda.NomeScheda + " : " + self.Esercizio.name

class UserAssign(models.Model):
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)    # scheda assegnata

    def __str__(self):
        return self.User.username + " : " + self.Scheda.NomeScheda
