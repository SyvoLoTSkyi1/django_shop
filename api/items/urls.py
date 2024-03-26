from rest_framework.routers import DefaultRouter

from api.items.views import ItemsViewSet, CategoriesViewSet

router = DefaultRouter()
router.register(r'items', ItemsViewSet, basename='items')
router.register(r'categories', CategoriesViewSet, basename='categories')
urlpatterns = router.urls
