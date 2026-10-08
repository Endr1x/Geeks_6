
class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('id_token')
        try:
            import requests as req
            response = req.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
            idinfo = response.json()

            if 'error' in idinfo or not idinfo.get('email'):
                raise ValidationError("Недействительный Google токен.")
            
            attrs['idinfo'] = idinfo
            return attrs
        except Exception as e:
            raise ValidationError(f"Ошибка авторизации через Google: {str(e)}")
