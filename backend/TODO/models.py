from django.db import models
from TODO.services.ids import generate_id


class User(models.Model):
    telegram_id = models.CharField(max_length=20, unique=True, primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Category(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_id, editable=False, max_length=32
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_category"
            )
        ]

        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_id, editable=False, max_length=32
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_id, editable=False, max_length=32
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="TODO")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    due_time = models.TimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
