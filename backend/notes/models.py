from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Color must be a valid hex code (e.g. #FF5733).",
)


class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, validators=[hex_color_validator])
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories", db_index=True
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_category_per_user"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Note(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes",
        db_index=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notes", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title or "(untitled)"
