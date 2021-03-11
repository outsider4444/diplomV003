from django.urls import path, include

from . import views

urlpatterns = [
    # Форма удаления
    # path("goods_list/<int:pk>/delete/", views.GoodsDeleteView.as_view(), name="goods_delete"),

    # Форма обновления
    # path("goods_list/<int:pk>/update/", views.GoodsUpdateView.as_view(), name="goods_update"),
    # path("workers_list/<int:slug>/update/", views.WorkerUpdate.as_view(), name="workers_update"),

    # Форма создания
    # path("goods_list/goods_create/", views.GoodsNew, name="goods_create"),
    # path("workers_list/workers_create/", views.WorkerNew, name="workers_create"),
    # path("customer_create/", views.CustomerCreateView, name="customer_create"),


    # Фильтры
    # path("goods_list/goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    # path('goods_list/goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    # path("goods_list/<int:pk>/", views.GoodsDetailView, name="goods_detail"),
    # path('workers_list/<int:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),
    path('<int:pk>/', views.CustomerDetailView, name="customer_detail"),

    # Список
    # path("goods_list/", views.GoodsView.as_view(), name="goods_list"),
    # path("workers_list/", views.WorkerView.as_view(), name="workers_list"),
    path("", views.CustomerView.as_view(), name="customer_list"),

    # Авторизация
    path("accounts/", include("allauth.urls")),


    # Главная страница
    # path("", views.MainView.as_view(), name="main")
]
