from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)  # stable order, required for correct pagination

    def __str__(self) -> str:
        return self.name
