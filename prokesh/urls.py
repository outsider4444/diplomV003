from django.urls import path

from . import views

urlpatterns = [
    path("", views.WorkerView.as_view())
]

