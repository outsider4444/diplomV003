from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # Форма удаления
    path("goods_list/<int:pk>/delete/", login_required(login_url='login')(views.GoodsDeleteView.as_view()), name="goods_delete"),
    path("material_list/<int:pk>/delete/", login_required(login_url='login')(views.MaterialDeleteView.as_view()), name="material_delete"),
    path("worker_list/<int:slug>/delete/", login_required(login_url='login')(views.WorkerDeleteView.as_view()), name="worker_delete"),
    path("customer_list/<int:pk>/delete/", login_required(login_url='login')(views.CustomerDeleteView.as_view()), name="customer_delete"),
    path("supplier_list/<int:pk>/delete/", login_required(login_url='login')(views.SupplierDeleteView.as_view()), name="supplier_delete"),
    path("nariad_list/<int:slug>/delete/", login_required(login_url='login')(views.NariadDeleteView.as_view()), name="nariad_delete"),
    path("otk_list/<int:pk>/delete/", login_required(login_url='login')(views.OTKDeleteView.as_view()), name="otk_delete"),
    # Склады
    path("storage_goods/<int:pk>/delete/", login_required(login_url='login')(views.StorageGoodsDeleteView.as_view()), name="storage_goods_delete"),
    path("storage_material/<int:pk>/delete/", login_required(login_url='login')(views.StorageMaterialsDeleteView.as_view()),
         name="storage_material_delete"),
    # Форма изделия
    path("goods_list/<int:pk>/goods_form_delete/", login_required(login_url='login')(views.GoodsFormDeleteView.as_view()), name="goods_form_delete"),


    # Форма обновления
    path("goods_list/<int:pk>/update/", login_required(login_url='login')(views.GoodsUpdateView.as_view()), name="goods_update"),
    path("worker_list/<int:slug>/update/", login_required(login_url='login')(views.WorkerUpdateView.as_view()), name="workers_update"),
    path("customer_list/<int:pk>/update/", login_required(login_url='login')(views.CustomerUpdateView.as_view()), name="customer_update"),
    path("material_list/<int:pk>/update/", login_required(login_url='login')(views.MaterialUpdateView.as_view()), name="material_update"),
    path("supplier_list/<int:pk>/update/", login_required(login_url='login')(views.SupplierUpdateView.as_view()), name="supplier_update"),
    path("nariad_list/<int:slug>/update/", login_required(login_url='login')(views.NariadUpdateView.as_view()), name="nariad_update"),
    path("otk_list/<int:pk>/update/", login_required(login_url='login')(views.OTKUpdateView), name="otk_update"),
    # Склады
    path("storage_goods/<int:pk>/update/", login_required(login_url='login')(views.StorageGoodsUpdateView.as_view()), name="storage_goods_update"),
    path("storage_material/<int:pk>/update/", login_required(login_url='login')(views.StorageMaterialsUpdateView.as_view()),
         name="storage_material_update"),


    # Форма создания
    path("goods_list/goods_create/", login_required(login_url='login')(views.GoodsNew), name="goods_create"),
    path("worker_list/workers_create/", login_required(login_url='login')(views.WorkerNew), name="workers_create"),
    path("customer_list/customer_create/", login_required(login_url='login')(views.CustomerNew), name="customer_create"),
    path("material_list/material_create/", login_required(login_url='login')(views.MaterialNew), name="material_create"),
    path("supplier_list/supplier_create/", login_required(login_url='login')(views.SupplierNew), name="supplier_create"),
    path("nariad_list/nariad_create/", login_required(login_url='login')(views.NariadNew), name="nariad_create"),
    path("otk_list/otk_create/", login_required(login_url='login')(views.OTKNew), name="otk_create"),
    # Склады
    path("storage_goods/storage_goods_create/", login_required(login_url='login')(views.StorageGoodsNew), name="goods_storage_create"),
    path("storage_material/storage_material_create/", login_required(login_url='login')(views.StorageMaterialsNew), name="storage_material_create"),



    # Обновить форму изделия
    path("goods_list/<int:pk>/update_goods_form/", login_required(login_url='login')(views.GoodsFormUpdateView.as_view()), name="update_goods_form"),
    # Добавить форму изделия
    path("goods_list/<int:pk>/create_goods_form/", login_required(login_url='login')(views.GoodsFormNew), name="create_goods_form"),

    # Фильтры
    path("goods_list/goods_filter/", views.FilterGoodsView.as_view(), name="goods_filter"),

    # Поиск
    path('goods_list/goods_search/', views.SearchGoods.as_view(), name='goods_search'),

    # Подробности
    path("goods_list/<int:pk>/", login_required(login_url='login')(views.GoodsDetailView), name="goods_detail"),
    path('worker_list/<int:slug>/', login_required(login_url='login')(views.WorkerDetailView.as_view()), name="worker_detail"),
    path('customer_list/<int:pk>/', login_required(login_url='login')(views.CustomerDetailView), name="customer_detail"),
    path('material_list/<int:pk>/', login_required(login_url='login')(views.MaterialDetailView), name="material_detail"),
    path('supplier_list/<int:pk>/', login_required(login_url='login')(views.SuppliersDetailView), name="supplier_detail"),
    path('nariad_list/<int:slug>/', login_required(login_url='login')(views.NariadDetailView), name="nariad_detail"),
    path('otk_list/<int:pk>/', login_required(login_url='login')(views.OTKDetailView), name="otk_detail"),
    # Склады
    path('storage_goods/<int:pk>/', login_required(login_url='login')(views.StorageGoodsDetailView), name="storage_goods_detail"),
    path('storage_material/<int:pk>/', login_required(login_url='login')(views.StorageMaterialsDetailView), name="storage_material_detail"),

    # Отчет о выпущенных изделиях_месяц_неделю_день_Календарь
    path("report_list/released_goods_report_month", login_required(login_url='login')(views.ReportReleasedGoodsMonth), name="released_goods_report_month"),
    path("report_list/released_goods_report_week", login_required(login_url='login')(views.ReportReleasedGoodsWeek), name="released_goods_report_week"),
    path("report_list/released_goods_report_today", login_required(login_url='login')(views.ReportReleasedGoodsToday), name="released_goods_report_today"),
    path("report_list/released_goods_report_calendar", login_required(login_url='login')(views.ReportReleasedGoodsCalendar),
         name="released_goods_report_calendar"),
    # Отчет о хороших изделиях_месяц_день_Календарь
    path("report_list/good_goods_report_month", login_required(login_url='login')(views.ReportGoodGoodsMonth), name="good_goods_report_month"),
    path("report_list/good_goods_report_week", login_required(login_url='login')(views.ReportGoodGoodsWeek), name="good_goods_report_week"),
    path("report_list/good_goods_report_today", login_required(login_url='login')(views.ReportGoodGoodsToday), name="good_goods_report_today"),
    path("report_list/good_goods_report_calendar", login_required(login_url='login')(views.ReportGoodGoodsCalendar),
         name="good_goods_report_calendar"),

    # Отчет удаленных изделий_месяц_неделю_день_Календарь
    path("report_list/remove_goods_report_month", login_required(login_url='login')(views.ReportRemoteGoodsMonth), name="remove_goods_report_month"),
    path("report_list/remove_goods_report_week", login_required(login_url='login')(views.ReportRemoteGoodsWeek), name="remove_goods_report_week"),
    path("report_list/remove_goods_report_today", login_required(login_url='login')(views.ReportRemoteGoodsToday), name="remove_goods_report_today"),
    path("report_list/remove_goods_report_calendar", login_required(login_url='login')(views.ReportRemoteGoodsCalendar),
         name="remove_goods_report_calendar"),
    # Отчет расхода материала_месяц_неделю_день_Календарь
    path("report_list/used_material_report_month", login_required(login_url='login')(views.ReportUsedMaterialMonth), name="used_material_report_month"),
    path("report_list/used_material_report_week", login_required(login_url='login')(views.ReportUsedMaterialWeek), name="used_material_report_week"),
    path("report_list/used_material_report_today", login_required(login_url='login')(views.ReportUsedMaterialToday), name="used_material_report_today"),
    path("report_list/used_material_report_calendar", login_required(login_url='login')(views.ReportUsedMaterialCalendar),
         name="used_material_report_calendar"),

    # Список
    path("goods_list/", login_required(login_url='login')(views.GoodsListView.as_view()), name="goods_list"),
    path("worker_list/", login_required(login_url='login')(views.WorkerListView.as_view()), name="workers_list"),
    path("customer_list/", login_required(login_url='login')(views.CustomerListView.as_view()), name="customer_list"),
    path("material_list/", login_required(login_url='login')(views.MaterialListView.as_view()), name="material_list"),
    path("supplier_list/", login_required(login_url='login')(views.SuppliersListView.as_view()), name="supplier_list"),
    path("nariad_list/", login_required(login_url='login')(views.NariadListView.as_view()), name="nariad_list"),
    path("otk_list/", login_required(login_url='login')(views.OTKListView.as_view()), name="otk_list"),
    # Склады
    path("storage_goods/", login_required(login_url='login')(views.StorageGoodsListView.as_view()), name="storage_goods_list"),
    path("storage_material/", login_required(login_url='login')(views.StorageMaterialsListView.as_view()), name="storage_material_list"),
    # Отчеты
    path("report_list/", login_required(login_url='login')(views.ReportList), name="report_list"),


    # Авторизация
    path("login/", views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),

    # Главная страница
    path("", login_required(login_url='login')(views.main), name="main")
]
