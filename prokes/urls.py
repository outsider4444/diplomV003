from django.urls import path, include

from . import views

urlpatterns = [
    # Обновление информации
    path("<slug:slug>/update/", views.GoodsUpdateView.as_view(), name="goods_update"),

    # Форма создания
    path("goods_new/", views.GoodsNew, name="goods_new"),

    # Фильтры
    path("goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    path('goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    path("<slug:slug>/", views.GoodsDetailView, name="goods_detail"),
    # path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),


    # Список
    path("", views.GoodsView.as_view(), name="goods_list"),
    # path('goods_list/', views.GoodsView.as_view(), name='goods_list'),

    # Авторизация
    path("accounts/", include("allauth.urls")),


    # Главная страница
    # path("", views.MainView.as_view(), name="main")
]
