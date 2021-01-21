from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Workers, Category, WorkTime, Smesi


# Create your views here.


class WorkerView(ListView):
    """Список сотрудников"""
    model = Workers
    queryset = Workers.objects.filter(fired=False)
    template_name = "workers/worker_list.html"


class WorkerDetailView(View):
    """Полная информация о сотруднике"""

    def get(self, request, slug):
        worker = Workers.objects.get(url=slug)
        worker_time = WorkTime.objects.get(worker_name_id=worker.id)
        return render(request, "workers/worker_detail.html", {"worker": worker, "worker_time": worker_time})


class SmesiView(ListView):
    """Список смесей"""
    model = Smesi
    queryset = Smesi.objects.all()
    template_name = 'smesi/smesi_list.html'


class SmesiDetailView(DetailView):
    """Полная информация о смеси"""

