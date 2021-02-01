from django.urls import path

from . import views

urlpatterns = [

    # Фильтры
    path("suppliers_list/suppliers_filter/", views.FilterSupplierView.as_view(), name="suppliers_filter"),
    path("worker_list/worker_filter/", views.FilterWorkerView.as_view(), name="worker_filter"),


    # Поиск
    path('worker_list/worker_search/', views.SearchWorker.as_view(), name='worker_search'),

    # Подробности
    path('smesi_list/<slug:slug>/', views.SmesiDetailView.as_view(), name="smesi_detail"),
    path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),
    path('suppliers_list/<slug:slug>/', views.SuppliersDetailView.as_view(), name='suppliers_detail'),
    path('customers_list/<slug:slug>/', views.CustomersDetailView.as_view(), name='customers_detail'),
    path('remote_list/<slug:slug>/', views.RemoteDetailView.as_view(), name='remote_detail'),
    path('worker_list/<slug:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),

    # Список
    path('smesi_list/', views.SmesiView.as_view(), name='smesi_list'),
    path('goods_list/', views.GoodsView.as_view(), name='goods_list'),
    path('suppliers_list/', views.SuppliersView.as_view(), name='suppliers_list'),
    path('customers_list/', views.CustomersView.as_view(), name='customers_list'),
    path('remote_list/', views.RemoteView.as_view(), name='remote_list'),
    path("worker_list/", views.WorkerView.as_view(), name='worker_list'),

    # Главная страница
    path("", views.MainView.as_view(), name="main")
]
