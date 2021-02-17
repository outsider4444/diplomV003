from django.urls import path, include

from . import views

urlpatterns = [
    # Отправка нового в БД
    path("<int:pk>/", views.AddGoods.as_view(), name="add_goods"),

    # Форма создания
    path("goods_new/", views.GoodsNew.as_view(), name="goods_new"),

    # Фильтры
    path("goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),


    # Поиск
    path('goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    path("<slug:slug>/", views.GoodsDetailView.as_view(), name="goods_detail"),
    # path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),


    # Список
    path("", views.GoodsView.as_view(), name="goods_list"),
    # path('goods_list/', views.GoodsView.as_view(), name='goods_list'),


    # Авторизация
    path("accounts/", include("allauth.urls")),


    # Главная страница
    # path("", views.MainView.as_view(), name="main")
]
