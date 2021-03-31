from django.urls import path, include

from . import views

urlpatterns = [
    # Форма удаления
    path("goods_list/<int:pk>/delete/", views.GoodsDeleteView.as_view(), name="goods_delete"),
    path("material_list/<int:pk>/delete/", views.MaterialDeleteView.as_view(), name="material_delete"),
    path("worker_list/<int:slug>/delete/", views.WorkerDeleteView.as_view(), name="worker_delete"),
    path("customer_list/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name="customer_delete"),
    path("supplier_list/<int:pk>/delete/", views.SupplierDeleteView.as_view(), name="supplier_delete"),

    # Форма обновления
    path("goods_list/<int:pk>/update/", views.GoodsUpdateView.as_view(), name="goods_update"),
    path("workers_list/<int:slug>/update/", views.WorkerUpdateView.as_view(), name="workers_update"),
    path("customer_list/<int:pk>/update/", views.CustomerUpdateView.as_view(), name="customer_update"),
    path("material_list/<int:pk>/update/", views.MaterialUpdateView.as_view(), name="material_update"),
    path("supplier_list/<int:pk>/update/", views.SupplierUpdateView.as_view(), name="supplier_update"),


    # Форма создания
    path("goods_list/goods_create/", views.GoodsNew, name="goods_create"),
    path("worker_list/workers_create/", views.WorkerNew, name="workers_create"),
    path("customer_list/customer_create/", views.CustomerNew, name="customer_create"),
    path("material_list/material_create/", views.MaterialNew, name="material_create"),
    path("supplier_list/supplier_create/", views.SupplierNew, name="supplier_create"),



    # Обновить форму изделия
    path("goods_list/<int:pk>/update_goods_form/", views.GoodsFormUpdateView.as_view(), name="update_goods_form"),
    # Добавить форму изделия
    path("goods_list/<int:pk>/create_goods_form/", views.GoodsFormNew, name="create_goods_form"),

    # Фильтры
    # path("goods_list/goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    # path('goods_list/goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    path("goods_list/<int:pk>/", views.GoodsDetailView, name="goods_detail"),
    path('worker_list/<int:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),
    path('customer_list/<int:pk>/', views.CustomerDetailView, name="customer_detail"),
    path('material_list/<int:pk>/', views.MaterialDetailView, name="material_detail"),
    path('supplier_list/<int:pk>/', views.SuppliersDetailView, name="supplier_detail"),


    # Список
    path("goods_list/", views.GoodsListView.as_view(), name="goods_list"),
    path("worker_list/", views.WorkerListView.as_view(), name="workers_list"),
    path("customer_list/", views.CustomerListView.as_view(), name="customer_list"),
    path("material_list/", views.MaterialListView.as_view(), name="material_list"),
    path("supplier_list/", views.SuppliersListView.as_view(), name="supplier_list"),

    # Авторизация
    path("accounts/", include("allauth.urls")),

    # Главная страница
    path("", views.main, name="main")
]
