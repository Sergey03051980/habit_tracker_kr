import re

def find_dependencies():
    """Find all dependencies from Python files"""
    dependencies = set()
    
    # Базовые зависимости Django
    base_deps = [
        'Django',
        'djangorestframework',
        'django-cors-headers',
        'celery',
        'redis',
        'psycopg2-binary',
        'gunicorn',
        'python-dotenv'
    ]
    
    # Ищем в INSTALLED_APPS
    try:
        with open('habit_tracker/settings.py', 'r') as f:
            content = f.read()
            
        # Ищем импорты приложений
        app_pattern = r"'([a-zA-Z_][a-zA-Z0-9_]*)'"
        apps = re.findall(app_pattern, content)
        
        # Маппинг приложений на зависимости
        app_to_dep = {
            'django_celery_results': 'django-celery-results',
            'rest_framework_simplejwt': 'djangorestframework-simplejwt',
            'drf_yasg': 'drf-yasg',
            'django_filters': 'django-filter',
            'drf_spectacular': 'drf-spectacular',
            'django_extensions': 'django-extensions'
        }
        
        for app in apps:
            if app in app_to_dep:
                dependencies.add(app_to_dep[app])
                
    except FileNotFoundError:
        pass
    
    return list(base_deps) + list(dependencies)

if __name__ == '__main__':
    deps = find_dependencies()
    print('\n'.join([f'{dep}>=0.0.0' for dep in deps]))
