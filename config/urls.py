"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from nagoyameshi.views import TopView,RestaurantView,ReviewView,FavoriteView,ReservationView,MypageView,CheckoutView,SuccessView,PortalView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TopView.as_view(), name="top"),
    path('restaurant/<int:pk>', RestaurantView.as_view(), name="restaurant"),

    # review/1 の場合 Restaurantのidが1の店舗にレビューを送るという意味になる。
    path('review/<int:pk>', ReviewView.as_view(), name="review"),

    # FavoriteViewを呼び出す。
    path('favorite/<int:pk>', FavoriteView.as_view(), name="favorite"),

    # ReservationViewを呼び出す。
    path('reservation/<int:pk>', ReservationView.as_view(), name="reservation"),


    # MypageViewを呼び出す。
    path('mypage/', MypageView.as_view(), name="mypage"),

    path('accounts/', include('allauth.urls')),


    # CheckoutView,SuccessViewを呼び出す。
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("success/", SuccessView.as_view(), name="success"),
    path("portal/", PortalView.as_view(), name="portal"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.TopView.as_view(), name="top"),
    # path('crud/', views.ProductListView.as_view(), name="list"),
    # path('crud/new/', views.ProductCreateView.as_view(), name="new"),
    # path('crud/edit/<int:pk>', views.ProductUpdateView.as_view(), name="edit"),
    # path('crud/delete/<int:pk>', views.ProductDeleteView.as_view(), name="delete"),
    # path('login/', views.LoginView.as_view(), name="login"),
    # path('logout/', views.LogoutView.as_view(), name="logout"),
# ]

