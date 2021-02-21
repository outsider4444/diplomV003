from django.urls import path, include

from . import views

urlpatterns = [
    # Форма удаления
    # path("goods_list/<int:pk>/delete/", views.GoodsDeleteView.as_view(), name="goods_delete"),

    # Форма обновления
    # path("goods_list/<int:pk>/update/", views.GoodsUpdateView.as_view(), name="goods_update"),
    path("<int:slug>/update/", views.WorkerUpdate.as_view(), name="workers_update"),

    # Форма создания
    # path("goods_list/goods_create/", views.GoodsNew, name="goods_create"),
    path("workers_create/", views.WorkerNew, name="workers_create"),

    # Фильтры
    # path("goods_list/goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    # path('goods_list/goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    # path("goods_list/<int:pk>/", views.GoodsDetailView, name="goods_detail"),
    path('<int:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),

    # Список
    # path("goods_list/", views.GoodsView.as_view(), name="goods_list"),
    path("", views.WorkerView.as_view(), name="workers_list"),

    # Авторизация
    path("accounts/", include("allauth.urls")),


    # Главная страница
    # path("", views.MainView.as_view(), name="main")
]
