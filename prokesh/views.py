from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Workers, WorkTime, Smesi, Goods, Suppliers, Customers, Remote


# Create your views here.


class MainView(ListView):
    """Главное меню"""
    model = Customers
    template_name = "main/main.html"


class WorkerCategory:
    """Должности сотрудников"""
    def get_category(self):
        return Workers.objects.filter(fired=False).values("category").distinct()


class WorkerView(WorkerCategory, ListView):
    """Список сотрудников"""
    model = Workers
    queryset = Workers.objects.filter(fired=False)
    template_name = "workers/worker_list.html"


class WorkerDetailView(WorkerCategory, View):
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


class SuppliersView(ListView):
    """Список поставщиков"""
    model = Suppliers
    queryset = Suppliers.objects.all()
    template_name = "suppliers/suppliers_list.html"


class SuppliersDetailView(View):
    """Полная информация об изделии"""

    # model = Goods
    # slug_field = "url"
    def get(self, request, slug):
        suppliers = Suppliers.objects.get(url=slug)
        return render(request, "suppliers/suppliers_detail.html", {"suppliers": suppliers})


class CustomersView(ListView):
    """Список заказчиков"""
    model = Customers
    queryset = Customers.objects.all()
    template_name = "customers/customers_list.html"


class CustomersDetailView(View):
    """Полная информация о заказчиках"""

    # model = Goods
    # slug_field = "url"
    def get(self, request, slug):
        customers = Customers.objects.get(url=slug)
        return render(request, "customers/customers_detail.html", {"customers": customers})


class RemoteView(ListView):
    """Список списанного"""
    model = Remote
    queryset = Remote.objects.all()
    template_name = "remote/remote_list.html"


class RemoteDetailView(View):
    """Полная информация о списанном"""

    # model = Goods
    # slug_field = "url"
    def get(self, request, slug):
        remote = Remote.objects.get(url=slug)
        return render(request, "remote/remote_detail.html", {"remote": remote})


# Отдел фильтров
class FilterWorkerView(WorkerCategory, ListView):
    """Фильтр сотрудников"""
    template_name = "workers/worker_list.html"

    def get_queryset(self):
        queryset = Workers.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context


class JsonFilterWorkerView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Workers.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))
        ).values("name", "category", "url", "image")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"worker": queryset}, safe=False)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Workers.objects.filter(title__icontains=self.request.GET.get("q").capitalize())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
