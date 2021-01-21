from django.urls import path

from . import views

urlpatterns = [
    path('smesi_list/', views.SmesiView.as_view(), name='smesi_list'),
    path('<slug:slug>/', views.WorkerDetailView.as_view(), name="worker_detail"),
    path("", views.WorkerView.as_view(), name='worker_list'),

]

