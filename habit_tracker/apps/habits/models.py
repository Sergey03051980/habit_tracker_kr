from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from habit_tracker.apps.users.models import User


class Habit(models.Model):
    """Модель привычки."""

    class Periodicity(models.TextChoices):
        DAILY = "daily", _("Ежедневно")
        WEEKLY = "weekly", _("Еженедельно")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name=_("Пользователь"),
    )
    name = models.CharField(_("Название"), max_length=255)
    place = models.CharField(
        _("Место"),
        max_length=255,
        blank=True,
        help_text=_("Место выполнения"),
    )
    time = models.TimeField(
        _("Время"),
        blank=True,
        null=True,
        help_text=_("Время выполнения"),
    )
    action = models.CharField(
        _("Действие"),
        max_length=500,
        blank=True,
        help_text=_("Действие привычки"),
    )
    description = models.TextField(_("Описание"), blank=True)
    period = models.CharField(
        _("Периодичность"),
        max_length=20,
        choices=Periodicity.choices,
        default=Periodicity.DAILY,
    )
    execution_time = models.TimeField(
        _("Время выполнения"),
        blank=True,
        null=True,
        help_text=_("Время выполнения"),
    )
    duration = models.PositiveIntegerField(
        _("Длительность (секунды)"),
        default=120,
        help_text=_("Максимум 120 секунд"),
    )
    is_public = models.BooleanField(_("Публичная"), default=False)
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлена"), auto_now=True)
    reward = models.CharField(
        _("Вознаграждение"),
        max_length=255,
        blank=True,
        help_text=_("Чем себя наградить"),
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Связанная привычка"),
        help_text=_("Приятная привычка"),
    )
    is_pleasant = models.BooleanField(
        _("Приятная привычка"),
        default=False,
        help_text=_("Является ли приятной"),
    )

    class Meta:
        verbose_name = _("Привычка")
        verbose_name_plural = _("Привычки")
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(duration__lte=120),
                name="duration_max_120_seconds",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    def clean(self):
        """Валидация модели."""
        super().clean()

        # 1. Время выполнения не более 120 секунд
        if self.duration > 120:
            raise ValidationError(
                {"duration": _("Время выполнения не может превышать 120 секунд.")}
            )

        # 2. Нельзя одновременно указать и вознаграждение, и связанную привычку
        if self.reward and self.linked_habit:
            raise ValidationError(
                _("Нельзя одновременно указывать и вознаграждение, и связанную привычку.")
            )

        # 3. Связанная привычка должна быть приятной
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError(
                _("Связанная привычка должна быть приятной.")
            )

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant:
            if self.reward:
                raise ValidationError(
                    _("Приятная привычка не может иметь вознаграждения.")
                )
            if self.linked_habit:
                raise ValidationError(
                    _("Приятная привычка не может быть связана с другой привычкой.")
                )

        # 5. Признак приятной привычки должен быть True для связанных привычек
        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError(
                _("Связанная привычка должна быть приятной.")
            )


class HabitCompletion(models.Model):
    """Модель для отметки выполнения привычки."""

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="completions",
        verbose_name=_("Привычка"),
    )
    completed_at = models.DateTimeField(_("Время выполнения"), auto_now_add=True)
    created_at = models.DateTimeField(_("Создано"), auto_now_add=True)

    class Meta:
        verbose_name = _("Выполнение привычки")
        verbose_name_plural = _("Выполнения привычек")
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.habit.name} - {self.completed_at.strftime('%Y-%m-%d %H:%M')}"
