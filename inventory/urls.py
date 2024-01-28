from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("revenues", views.revenues, name="revenues"),
    path("vehicles", views.vehicles, name="vehicles"),
    path("sell/<str:vtype>", views.sell_view, name="sell"),
    path("add/<str:vtype>", views.add_view, name="add"),
    

    # API Routes
    path("api/sell", views.sell, name="sale"),
    path("api/add", views.add, name="create"),
    path("api/chartdata/<str:chart>", views.data_charts, name="chartdata")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)