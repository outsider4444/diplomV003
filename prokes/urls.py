from django.urls import path, include

from . import views

urlpatterns = [
    # Форма удаления
    path("<int:pk>/delete/", views.GoodsDeleteView.as_view(), name="goods_delete"),

    # Форма обновления
    path("<int:pk>/update/", views.GoodsUpdateView.as_view(), name="goods_update"),

    # Форма создания
    path("goods_create/", views.GoodsNew, name="goods_create"),

    # Фильтры
    path("goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    path('goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    path("<int:pk>/", views.GoodsDetailView, name="goods_detail"),
    # path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),

    # Список
    path("", views.GoodsView.as_view(), name="goods_list"),
    # path('goods_list/', views.GoodsView.as_view(), name='goods_list'),

    # Авторизация
    path("accounts/", include("allauth.urls")),


    # Главная страница
    # path("", views.MainView.as_view(), name="main")
]
