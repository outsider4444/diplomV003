from django.urls import path, re_path

from . import views

urlpatterns = [
    path('smesi_list/<slug:slug>/', views.SmesiDetailView.as_view(), name="smesi_detail"),
    path('goods_list/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods_detail'),
    path('smesi_list/', views.SmesiView.as_view(), name='smesi_list'),
    path('goods_list/', views.GoodsView.as_view(), name='goods_list'),
    path('<slug:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),
    path("", views.WorkerView.as_view(), name='worker_list'),
]

