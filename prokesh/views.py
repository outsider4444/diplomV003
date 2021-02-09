from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from .models import Workers, Smesi, Goods, Suppliers, Customers, Remote


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


class RemoteSmesiGoods:
    """Коды смесей и изделий"""

    def get_remotesmesi(self):
        return Remote.objects.values("code_smesi").distinct()

    def get_remotegoods(self):
        return Remote.objects.values("code_goods").distinct()


# основная информация
class WorkerView(WorkerCategory, ListView):
    """Список сотрудников"""
    model = Workers
    queryset = Workers.objects.filter(fired=False)
    template_name = "workers/worker_list.html"
    paginate_by = 1


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
    paginate_by = 1


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
    paginate_by = 1


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
    paginate_by = 1


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
    paginate_by = 1


class CustomersDetailView(DetailView, CustomersDate):
    """Полная информация о заказчиках"""
    model = Customers
    slug_field = "url"
    template_name = "customers/customers_detail.html"


class RemoteView(ListView, RemoteSmesiGoods):
    """Список списанного"""
    model = Remote
    queryset = Remote.objects.all()
    template_name = "remote/remote_list.html"
    paginate_by = 1


class RemoteDetailView(DetailView, RemoteSmesiGoods):
    """Полная информация о списанном"""
    model = Remote
    slug_field = "url"
    template_name = "remote/remote_detail.html"


# Отдел фильтров
class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    template_name = "workers/worker_list.html"

    def get_queryset(self):
        queryset = Workers.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))
        ).distinct().values("name", "category", "url", "image")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"workers": queryset}, safe=False)


class FilterWorkerView(WorkerCategory, ListView):
    """Фильтр сотрудников"""
    template_name = "workers/worker_list.html"

    def get_queryset(self):
        category = self.request.GET.getlist("category")
        if not category:
            queryset = Workers.objects.all()
        else:
            queryset = Workers.objects.filter(
                Q(category__in=category)
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
        date = self.request.GET.getlist("date")
        if not date:
            queryset = Suppliers.objects.all()
        else:
            queryset = Suppliers.objects.filter(
                Q(date__in=date)
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
        date = self.request.GET.getlist("date")
        worker_name = self.request.GET.getlist("worker_name")
        if date == [] and worker_name == []:
            queryset = Smesi.objects.all()
        elif date:
            queryset = Smesi.objects.filter(
                Q(date__in=date)
            ).distinct()
        elif worker_name:
            queryset = Smesi.objects.filter(
                Q(worker_name__name__in=worker_name)
            ).distinct()
        else:
            queryset = Smesi.objects.filter(
                Q(date__in=date) &
                Q(worker_name__name__in=worker_name)
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        context["worker_name"] = ''.join([f"worker_name={x}&" for x in self.request.GET.getlist("worker_name")])
        return context


class FilterRemoteView(RemoteSmesiGoods, ListView):
    """Фильтр списанного"""
    template_name = "remote/remote_list.html"

    def get_queryset(self):
        delete_date = self.request.GET.getlist("date")
        code_goods = self.request.GET.getlist("code_goods")
        code_smesi = self.request.GET.getlist("code_smesi")
        if delete_date == [] and code_goods == [] and code_smesi == []:
            queryset = Remote.objects.all()
        elif delete_date != [] and code_goods != [] and code_smesi != []:
            queryset = Remote.objects.filter(
                Q(delete_date__in=delete_date) |
                Q(code_smesi__in=code_smesi) &
                Q(code_goods__in=code_goods)
            ).distinct()
        elif code_smesi != []:
            queryset = Remote.objects.filter(
                Q(delete_date__in=delete_date) |
                Q(code_smesi__in=code_smesi)
            ).distinct()
        elif code_goods != []:
            queryset = Remote.objects.filter(
                Q(delete_date__in=delete_date) |
                Q(code_goods__in=code_goods)
            ).distinct()
        else:
            queryset = Remote.objects.filter(
                Q(delete_date__in=delete_date)
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        context["code_goods"] = ''.join([f"code_goods={x}&" for x in self.request.GET.getlist("code_goods")])
        context["code_smesi"] = ''.join([f"code_smesi={x}&" for x in self.request.GET.getlist("code_smesi")])
        return context


class FilterCustomersView(CustomersDate, ListView):
    """Фильтр заказчиков"""
    template_name = "customers/customers_list.html"

    def get_queryset(self):
        date = self.request.GET.getlist("date")
        if not date:
            queryset = Customers.objects.all()
        else:
            queryset = Customers.objects.filter(
                Q(date__in=date)
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["date"] = ''.join([f"date={x}&" for x in self.request.GET.getlist("date")])
        return context


class FilterGoodsView(ListView):
    """Фильтр изделий"""
    template_name = "goods/goods_list.html"

    def get_queryset(self):
        temp = self.request.GET.get("temp")
        malt = self.request.GET.get("malt")
        pres = self.request.GET.get("pres")
        strength = self.request.GET.get("strength")
        if temp == "" and malt == "" and pres == "" and strength == "":
            queryset = Goods.objects.all()
        elif temp != "" and malt != "" and pres != "" and strength != "":
            queryset = Goods.objects.filter(
                Q(min_temperature__lte=int(temp)) &
                Q(min_malt__lte=int(malt)) &
                Q(min_pressure__lte=int(pres)) &
                Q(min_strength__lte=int(strength))
            ).distinct()
        elif temp != "" and malt != "" and pres != "":
            queryset = Goods.objects.filter(
                Q(min_temperature__lte=int(temp)) &
                Q(min_malt__lte=int(malt)) &
                Q(min_pressure__lte=int(pres))
            ).distinct()
        elif temp != "" and malt != "" and strength != "":
            queryset = Goods.objects.filter(
                Q(min_temperature__lte=int(temp)) &
                Q(min_malt__lte=int(malt)) &
                Q(min_strength__lte=int(strength))
            ).distinct()
        elif temp != "" and pres != "" and strength != "":
            queryset = Goods.objects.filter(
                Q(min_temperature__lte=int(temp)) &
                Q(min_pressure__lte=int(pres)) &
                Q(min_strength__lte=int(strength))
            ).distinct()
        elif malt != "" and pres != "" and strength != "":
            queryset = Goods.objects.filter(
                Q(min_malt__lte=int(malt)) &
                Q(min_pressure__lte=int(pres)) &
                Q(min_strength__lte=int(strength))
            ).distinct()
        elif temp != "":
            queryset = Goods.objects.filter(
                Q(min_temperature__lte=int(temp))
            ).distinct()
        elif malt != "":
            queryset = Goods.objects.filter(
                Q(min_malt__lte=int(malt))
            ).distinct()
        elif pres != "":
            queryset = Goods.objects.filter(
                Q(min_pressure__lte=int(pres))
            ).distinct()
        elif strength != "":
            queryset = Goods.objects.filter(
                Q(min_strength__lte=int(strength))
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["temp"] = ''.join([f"temp={x}&" for x in self.request.GET.getlist("temp")])
        context["malt"] = ''.join([f"malt={x}&" for x in self.request.GET.getlist("malt")])
        context["pres"] = ''.join([f"pres={x}&" for x in self.request.GET.getlist("pres")])
        context["strength"] = ''.join([f"strength={x}&" for x in self.request.GET.getlist("strength")])
        return context


# Отдел поиска

class SearchWorker(ListView, WorkerCategory):
    """Поиск сотрудников"""
    template_name = "workers/worker_list.html"

    def get_queryset(self):
        return Workers.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class SearchSuppliers(ListView, SupplierDate):
    """Поиск поставщиков"""
    template_name = "suppliers/suppliers_list.html"

    def get_queryset(self):
        return Suppliers.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class SearchSmesi(ListView, SmesiWorkerDate):
    """Поиск смесей"""
    template_name = "smesi/smesi_list.html"

    def get_queryset(self):
        return Smesi.objects.filter(code__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context