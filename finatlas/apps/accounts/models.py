from django.contrib.auth.models import AbstractUser
from django.db import models

"""
campos que já vem da classe User:
username,
first_name,
last_name,
email,
password,
groups,
user_permissions,
is_staff,
is_active,
is_superuser,
last_login,
date_joined
"""


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        FINANCEIRO = "financeiro", "Financeiro"
        ASSESSOR = "assessor", "Assessor"

    email = models.EmailField("E-mail", unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ASSESSOR,
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username


class Assessor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="advisor_profile",
        verbose_name="Usuário",
    )

    codigo_assessor = models.CharField(
        "Código do Assessor",
        max_length=30,
        unique=True,
        db_index=True,
    )

    role = models.CharField(
        "Função",
        max_length=20,
        choices=CustomUser.Role.choices,
        default=CustomUser.Role.ASSESSOR,
    )

    is_active = models.BooleanField(
        "Ativo",
        default=True,
    )

    class Meta:
        verbose_name = "Perfil do Assessor"
        verbose_name_plural = "Perfis dos Assessores"
        

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.codigo_assessor})"

