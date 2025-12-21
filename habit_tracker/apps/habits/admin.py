from django.contrib import admin
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "period",
        "duration",
        "is_public",
        "created_at",
    ]
    list_filter = ["period", "is_public", "created_at"]
    search_fields = ["name", "description", "action"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("user", "name", "description", "action")
        }),
        ("Детали выполнения", {
            "fields": ("place", "time", "period", "duration")
        }),
        ("Дополнительно", {
            "fields": ("is_public", "created_at", "updated_at")
        }),
        ("Вознаграждения", {
            "fields": ("reward", "linked_habit", "is_pleasant"),
            "classes": ("collapse",),
        }),
    )


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ["habit", "completed_at", "created_at"]
    list_filter = ["completed_at", "created_at"]
    readonly_fields = ["completed_at", "created_at"]
