from django.contrib import admin

from .models import Category, Task, User, Tag


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username")
    search_fields = ("telegram_id", "username")
    ordering = ("telegram_id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    list_filter = ("user",)
    search_fields = ("name", "user__telegram_id")
    ordering = ("user", "name")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category", "due_date", "is_completed", "display_tags")
    list_filter = ("is_completed", "category", "due_date", "tags")
    search_fields = ("title", "user__telegram_id", "category__name", "tags__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    filter_horizontal = ("tags",)  # удобный виджет для выбора тегов

    def display_tags(self, obj):
        """Отображение тегов в колонке через запятую"""
        return ", ".join(tag.name for tag in obj.tags.all())

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
