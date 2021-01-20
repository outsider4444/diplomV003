from django.urls import path

from . import views

urlpatterns = [
    path("", views.WorkerView.as_view(), name='worker'),
    path("<slug:slug>/", views.WorkerDetailView.as_view(), name="worker_detail")
]

