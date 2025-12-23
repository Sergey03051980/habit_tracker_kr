from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Habit, HabitCompletion

class HabitSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name', read_only=True)
    
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Все валидаторы из ТЗ"""
        
        # 1. Нельзя одновременно linked_habit и reward
        if data.get('linked_habit') and data.get('reward'):
            raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")
        
        # 2. Время выполнения <= 120 секунд
        if data.get('duration') and data['duration'] > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")
        
        # 3. linked_habit должен быть is_pleasant=True
        linked_habit = data.get('linked_habit')
        if linked_habit and not linked_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")
        
        # 4. У приятной привычки не может быть reward или linked_habit
        if data.get('is_pleasant'):
            if data.get('reward'):
                raise ValidationError("У приятной привычки не может быть вознаграждения.")
            if data.get('linked_habit'):
                raise ValidationError("У приятной привычки не может быть связанной привычки.")
        
        # 5. Периодичность 1-7 дней
        if data.get('period') and (data['period'] < 1 or data['period'] > 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
        
        return data
    
    def validate_duration(self, value):
        if value > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")
        return value
    
    def validate_period(self, value):
        if value < 1 or value > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
        return value

class HabitCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCompletion
        fields = '__all__'
        read_only_fields = ['completed_at', 'created_at']
