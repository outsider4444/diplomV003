from django.urls import path, include

from . import views

urlpatterns = [

    # Фильтры
    path("worker_list/json-filter/", views.JsonFilterMoviesView.as_view(), name="json_filter"),
    path("smesi_list/smesi_filter/", views.FilterSmesiView.as_view(), name="smesi_filter"),
    path("suppliers_list/suppliers_filter/", views.FilterSupplierView.as_view(), name="suppliers_filter"),
    path("worker_list/worker_filter/", views.FilterWorkerView.as_view(), name="worker_filter"),
    path("customers_list/customers_filter/", views.FilterCustomersView.as_view(), name="customers_filter"),
    path("goods_list/goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),
    path("remote_list/remote_filter/", views.FilterRemoteView.as_view(), name="remote_filter"),

    # Поиск
    path('worker_list/worker_search/', views.SearchWorker.as_view(), name='worker_search'),
    path('suppliers_list/suppliers_search/', views.SearchSuppliers.as_view(), name='suppliers_search'),
    path('smesi_list/smesi_search/', views.SearchSmesi.as_view(), name='smesi_search'),
    path('customers_list/customers_search/', views.SearchCustomers.as_view(), name='customers_search'),
    path('remote_list/remote_search/', views.SearchRemote.as_view(), name='remote_search'),


    # Подробности
    path('worker_list/<slug:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),
    path('smesi_list/<slug:slug>/', views.SmesiDetailView.as_view(), name="smesi_detail"),
    path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),
    path('suppliers_list/<slug:slug>/', views.SuppliersDetailView.as_view(), name='suppliers_detail'),
    path('customers_list/<slug:slug>/', views.CustomersDetailView.as_view(), name='customers_detail'),
    path('remote_list/<slug:slug>/', views.RemoteDetailView.as_view(), name='remote_detail'),


    # Список
    path('smesi_list/', views.SmesiView.as_view(), name='smesi_list'),
    path('goods_list/', views.GoodsView.as_view(), name='goods_list'),
    path('suppliers_list/', views.SuppliersView.as_view(), name='suppliers_list'),
    path('customers_list/', views.CustomersView.as_view(), name='customers_list'),
    path('remote_list/', views.RemoteView.as_view(), name='remote_list'),
    path("worker_list/", views.WorkerView.as_view(), name='worker_list'),
    # path("calendar/", views.CalendarView.as_view(), name='calendar'),



    # Авторизация
    path("accounts/", include("allauth.urls")),

    # Главная страница
    path("", views.MainView.as_view(), name="main")
]
