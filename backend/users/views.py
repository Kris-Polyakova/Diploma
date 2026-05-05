from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AdminUserUpdateSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"[{__name__}] INFO {user.username} зарегистрирован успешно.")
            return Response({
                "message": "Пользователь успешно зарегистрирован",
                "username": user.username
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        print(f"[{__name__}] INFO Пользователь {self.user.username} успешно вошёл в систему.")
        return data


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                print(f"INFO Пользователь {request.user.username} вышел из системы (refresh токен заблокирован)")
            else:
                print(f"WARNING Logout без refresh токена от пользователя {request.user.username}")

            return Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(f"ERROR Ошибка при logout: {e}")
            return Response({"error": "Неверный refresh токен"}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all().values('id', 'username', 'full_name', 'email', 'is_admin', 'date_joined')
        print(f"INFO Админ {request.user.username} запросил список всех пользователей")
        return Response({"users": list(users)})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
        })


class AdminUserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(f"INFO Админ {request.user.username} отредактировал пользователя {user.username}")
            return Response({"message": "Пользователь обновлён", "user": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user.is_superuser and not request.user.is_superuser:
            return Response({"error": "Нельзя удалить главного суперпользователя"}, status=status.HTTP_403_FORBIDDEN)

        username = user.username
        user.delete()
        print(f"INFO Админ {request.user.username} удалил пользователя {username}")
        return Response({"message": f"Пользователь {username} успешно удалён"}, status=status.HTTP_204_NO_CONTENT)