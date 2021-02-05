from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Workers, Smesi, Goods, Suppliers, Customers, Remote


# Create your views here.


class MainView(ListView):
    """Главное меню"""
    model = Customers
    template_name = "main/main.html"


# Выводы для фильтров
class WorkerCategory:
    """Должности сотрудников"""

    def get_category(self):
        return Workers.objects.filter(fired=False).values("category").distinct()


class SupplierDate:
    """Даты поставки поставщиков"""

    def get_supdate(self):
        return Suppliers.objects.values("date").distinct()


class CustomersDate:
    """Даты поставки поставщиков"""

    def get_cusdate(self):
        return Customers.objects.values("date").distinct()


class SmesiWorkerDate:
    """Даты изготовления смесей и сотрудники"""

    def get_smesiyears(self):
        return Smesi.objects.values("date").distinct()

    def get_smesiworker(self):
        return Smesi.objects.all()


# основная информация
class WorkerView(WorkerCategory, ListView):
    """Список сотрудников"""
    model = Workers
    queryset = Workers.objects.filter(fired=False)
    template_name = "workers/worker_list.html"


class WorkerDetailView(DetailView, WorkerCategory):
    """Полная информация о сотруднике"""
    model = Workers
    slug_field = "url"
    template_name = 'workers/worker_detail.html'


class SmesiView(SmesiWorkerDate, ListView):
    """Список смесей"""
    model = Smesi
    queryset = Smesi.objects.all()
    template_name = 'smesi/smesi_list.html'


class SmesiDetailView(SmesiWorkerDate, DetailView):
    """Полная информация о смеси"""
    model = Smesi
    slug_field = "url"
    template_name = 'smesi/smesi_detail.html'


class GoodsView(ListView):
    """Список изделий"""
    model = Goods
    queryset = Goods.objects.all()
    template_name = "goods/goods_list.html"


class GoodsDetailView(DetailView):
    """Полная информация об изделии"""
    model = Goods
    slug_field = "url"
    template_name = "goods/goods_detail.html"


class SuppliersView(SupplierDate, ListView):
    """Список поставщиков"""
    model = Suppliers
    queryset = Suppliers.objects.all()
    template_name = "suppliers/suppliers_list.html"


class SuppliersDetailView(SupplierDate, DetailView):
    """Полная информация об изделии"""
    model = Suppliers
    slug_field = "url"
    template_name = "suppliers/suppliers_detail.html"


class CustomersView(ListView, CustomersDate):
    """Список заказчиков"""
    model = Customers
    queryset = Customers.objects.all()
    template_name = "customers/customers_list.html"


class CustomersDetailView(DetailView, CustomersDate):
    """Полная информация о заказчиках"""
    model = Customers
    slug_field = "url"
    template_name = "customers/customers_detail.html"


class RemoteView(ListView):
    """Список списанного"""
    model = Remote
    queryset = Remote.objects.all()
    template_name = "remote/remote_list.html"


class RemoteDetailView(DetailView):
    """Полная информация о списанном"""
    model = Remote
    slug_field = "url"
    template_name = "remote/remote_detail.html"


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


class FilterSupplierView(SupplierDate, ListView):
    """Фильтр поставщиков"""
    template_name = "suppliers/suppliers_list.html"

    def get_queryset(self):
        queryset = Suppliers.objects.filter(
            Q(date__in=self.request.GET.getlist("date"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        return context


class FilterSmesiView(SmesiWorkerDate, ListView):
    """Фильтр смесей"""
    template_name = "smesi/smesi_list.html"

    def get_queryset(self):
        queryset = Smesi.objects.filter(
            Q(date__in=self.request.GET.getlist("date")) |
            Q(worker_name__name__in=self.request.GET.getlist("worker_name"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        context["worker_name"] = ''.join([f"worker_name={x}&" for x in self.request.GET.getlist("worker_name")])
        return context


class FilterCustomersView(CustomersDate, ListView):
    """Фильтр заказчиков"""
    template_name = "customers/customers_list.html"

    def get_queryset(self):
        queryset = Customers.objects.filter(
            Q(date__in=self.request.GET.getlist("date"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        return context

# Отдел поиска

class SearchWorker(ListView):
    """Поиск сотрудников"""
    template_name = "workers/worker_list.html"

    def get_queryset(self):
        return Workers.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class SearchSuppliers(ListView):
    """Поиск поставщиков"""
    template_name = "suppliers/suppliers_list.html"

    def get_queryset(self):
        return Suppliers.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
