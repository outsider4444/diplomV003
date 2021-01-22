from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Workers, Category, WorkTime, Smesi, Goods


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


class SmesiDetailView(View):
    """Полная информация о смеси"""
    # model = Smesi
    # slug_field = "url"

    def get(self, request, slug):
        smesi = Smesi.objects.get(url=slug)
        return render(request, "smesi/smesi_detail.html", {"smesi": smesi})


class GoodsView(ListView):
    """Список изделий"""
    model = Goods
    queryset = Goods.objects.all()
    template_name = "goods/goods_list.html"


class GoodsDetailView(View):
    """Полная информация об изделии"""
    # model = Goods
    # slug_field = "url"
    def get(self, request, slug):
        goods = Goods.objects.get(url=slug)
        return render(request, "goods/goods_detail.html", {"goods": goods})
