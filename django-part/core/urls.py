from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users import views as users_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', users_view.BlacklistTokenUpdateView.as_view(), name='logout'),
    path('register/', users_view.UserCreate.as_view(), name="register"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
