from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, CategoryViewSet
from orders.views import OrderViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')

from users.views import get_user_profile, register_user, upload_avatar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/profile/', get_user_profile, name='user_profile'),
    path('api/user/register/', register_user, name='user_register'),
    path('api/user/upload-avatar/', upload_avatar, name='upload_avatar'),
    path('api/dashboard/', include('dashboard.urls')),
]

# Important pour afficher les images en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)