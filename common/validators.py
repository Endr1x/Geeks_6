from datetime import date
from rest_framework.exceptions import ValidationError

def validate_user_age(request):
    if not request or not request.auth:
        return
    
    payload = getattr(request, 'auth', None)
    if hasattr(payload, 'payload'):
        payload = payload.payload

    birthdate_str = payload.get('birthdate') if payload else None

    if not birthdate_str or birthdate_str == 'None':
        raise ValidationError("Укажите дату рождения, чтобы создать продукт.")

    try:
        birthdate = date.fromisoformat(birthdate_str)
    except ValueError:
        raise ValidationError("Неверный формат даты рождения.")

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
