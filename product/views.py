
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GoogleLoginSerializer

class GoogleLoginView(generics.GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idinfo = serializer.validated_data['idinfo']
        
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        user, created = User.objects.get_or_create(email=email, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'is_active': True,
            'registration_source': 'google'
        })

        if not created:
            user.first_name = first_name or user.first_name
            user.last_name = last_name or user.last_name
            user.is_active = True
            if user.registration_source == 'local':
                user.registration_source = 'google'
        
        user.last_login = timezone.now()
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Успешная авторизация через Google'
        }, status=status.HTTP_200_OK)
