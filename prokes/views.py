from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from datetime import date, timedelta
import locale
import pandas

from .forms import *
from .filters import ReportRemoteGoodsFilter, ReportUsedMaterialFilter

from .models import *


# Текущий месяц и его даты
def days_cur_month(strdate):
    locale.setlocale(locale.LC_ALL, "")
    m = datetime.now().month
    y = datetime.now().year
    ndays = (date(y, m + 1, 1) - date(y, m, 1)).days
    d1 = date(y, m, 1)
    d2 = date(y, m, ndays)
    delta = d2 - d1

    return [(d1 + timedelta(days=i)).strftime(strdate) for i in range(delta.days + 1)]


# текущая неделя
def week_now(strdate):
    locale.setlocale(locale.LC_ALL, "")
    now = datetime.now()
    now_day_1 = now - timedelta(days=now.weekday())
    dates = {}
    for n_week in range(1):
        dates[n_week] = [(now_day_1 + timedelta(days=d + n_week * 7)).strftime(strdate) for d in range(7)]
        return dates[n_week]


def calendar(s_date, e_date, strdate):
    locale.setlocale(locale.LC_ALL, "")
    start_date = datetime(s_date[0], s_date[1], s_date[2])
    end_date = datetime(e_date[0], e_date[1], e_date[2])

    res = pandas.date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime(strdate).tolist()
    return res


# Главная страница
def main(request):
    """Главное меню"""
    return render(request, "main/main.html")


# Список отчетов
def ReportList(request):
    """Список отчетов"""
    return render(request, "reports/reports_list.html")


# Выводы для фильтров
class WorkerCategory:
    """Должности сотрудников"""

    def get_category(self):
        return Workers.objects.filter(fired=False).values("category").distinct()


# Сотрудники
class WorkerListView(WorkerCategory, ListView):
    """Список сотрудников"""
    model = Workers
    queryset = Workers.objects.filter(fired=False)
    template_name = "workers/worker_list.html"
    paginate_by = 15


def WorkerNew(request):
    """Создание нового сотрудника"""
    worker_list = Workers.objects.all()
    form = WorkersForm()
    error = ""
    if request.method == "POST":
        form = WorkersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('workers_list'))
        else:
            print(form['code'].value())
            for worker in worker_list:
                if int(form['code'].value()) == worker.code:
                    error = "Сотрудник с таким кодом уже существует"
                    break
                else:
                    error = "Форма неверно заполнена"
    return render(request, "workers/workers_form/worker_new.html", {"form": form, "error": error})


class WorkerDetailView(DetailView, WorkerCategory):
    """Полная информация о сотруднике"""
    model = Workers
    slug_field = "code"
    template_name = 'workers/worker_detail.html'


class WorkerUpdateView(UpdateView):
    """Редактирование информации о сотруднике"""
    model = Workers
    template_name = "workers/workers_form/worker_new.html"
    success_url = "/worker_list"
    slug_field = "code"
    form_class = WorkersForm


class WorkerDeleteView(DeleteView):
    """Удаление сотрудника"""
    model = Workers
    # Изменить на список изделий
    slug_field = 'code'
    success_url = "/worker_list"
    template_name = "workers/workers_form/worker_delete.html"


# Заказчики
class CustomerListView(ListView):
    """Список заказчиков"""
    model = Customer
    queryset = Customer.objects.all()
    template_name = "customer/customer_list.html"
    paginate_by = 1


def CustomerNew(request):
    """Создание нового заказчика"""
    form = CustomerForm()
    error = ""
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
        else:
            error = "Форма неверно заполнена"
    return render(request, "customer/customer_form/customer_new.html", {"form": form, "error": error})


def CustomerDetailView(request, pk):
    """Полная информация о заказчиках"""
    OrderFormSet = inlineformset_factory(Customer, CheckoutGoods, fields=("code_goods", "values"), extra=10)
    customer = Customer.objects.get(id=pk)
    goods = CheckoutGoods.objects.filter(customer_name=pk)
    formset = OrderFormSet(queryset=CheckoutGoods.objects.none(), instance=customer)
    date = CheckoutGoods.objects.order_by().values('date').order_by("date").distinct()
    error = ""
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            # перенаправление на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            error = formset.errors
    context = {"customer": customer, "formset": formset,
               "error": error, "date": date, "goods": goods}
    return render(request, "customer/customer_detail.html", context)


class CustomerUpdateView(UpdateView):
    """Редактирование информации о заказчике"""
    model = Customer
    template_name = "customer/customer_form/customer_new.html"
    success_url = "/customer_list"
    form_class = CustomerForm


class CustomerDeleteView(DeleteView):
    """Удаление заказчика"""
    model = Customer
    # Изменить на список изделий
    success_url = '/customer_list'
    template_name = "customer/customer_form/customer_delete.html"


# Изделия
class GoodsListView(ListView):
    """Список изделий"""
    model = Goods
    queryset = Goods.objects.all()
    template_name = "goods/goods_list.html"
    paginate_by = 5


def GoodsDetailView(request, pk):
    """Полная информация об изделии"""
    error = ""
    goods = Goods.objects.get(id=pk)
    calendar = GoodsCalendar.objects.filter(goods_code=pk)
    form = CalendarForm()
    goods_form = GoodsDefaultForm.objects.filter(goods_code=pk)
    if request.method == "POST":
        form = CalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('goods_list'))
        else:
            error = "Форма неверно заполнена"
    context = {"calendar": calendar, "goods": goods, "form": form, "error": error,
               "goods_form": goods_form, }
    return render(request, "goods/goods_detail.html", context)


class GoodsUpdateView(UpdateView):
    """Редактирование информации о детали"""
    model = Goods
    template_name = "goods/goods_form/goods_new.html"
    success_url = "/goods_list"
    form_class = GoodsForm


def GoodsNew(request):
    """Создание нового изделия"""
    form = GoodsForm()
    goods_list = Goods.objects.all()
    error = ""

    if request.method == "POST":
        form = GoodsForm(request.POST, request.FILES)
        # проверка на присутсвие изделия в бд
        if goods_list.__len__() != 0:
            for goods in goods_list:
                if form['code'].value() == goods.code:
                    error = "Такое изделие уже существует!"
                    break
                else:
                    if form.is_valid():
                        form.save()
                        return redirect(reverse('goods_list'))
                    else:
                        error = "Форма неверно заполнена"
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('goods_list'))
            else:
                error = "Форма неверно заполнена"
    return render(request, "goods/goods_form/goods_new.html", {"form": form, "error": error, "goods_list": goods_list,})


class GoodsDeleteView(DeleteView):
    """Удаление изделия"""
    model = Goods
    # Изменить на список изделий
    success_url = "/goods_list"
    template_name = "goods/goods_form/goods_delete.html"


class GoodsFormUpdateView(UpdateView):
    """Обновление информации о форме изделия"""
    model = GoodsDefaultForm
    template_name = 'goods/goods_form/def_form/goods_def_form_update.html'
    success_url = "/goods_list"
    form_class = FormsGoodsForm
    slug_field = 'pk'


class GoodsFormDeleteView(DeleteView):
    """Удаление изделия"""
    model = GoodsDefaultForm
    # Изменить на список изделий
    success_url = "/goods_list"
    template_name = "goods/goods_form/goods_delete.html"
    slug_field = 'pk'


def GoodsFormNew(request, pk):
    """Создание новой формы изделия"""
    goods = Goods.objects.get(id=pk)
    form = FormsGoodsForm()
    error = ""
    if request.method == "POST":
        form = FormsGoodsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('goods_list'))
        else:
            error = "Форма неверно заполнена"
    return render(request, 'goods/goods_form/def_form/goods_def_form_new.html', {"form": form,
                                                                                 "error": error, "goods": goods})


# Фильтры для изделий
class FilterGoodsView(ListView):
    """Фильтр изделий"""
    template_name = "goods/goods_list.html"

    def get_queryset(self):
        queryset = ""
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


# Поиск изделий
class SearchGoods(ListView):
    """Поиск изделий"""
    template_name = "goods/goods_list.html"

    def get_queryset(self):
        return Goods.objects.filter(code__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


# Материалы
class MaterialListView(ListView):
    """Список материалов"""
    model = Materials
    queryset = Materials.objects.all()
    template_name = "materials/material_list.html"
    # paginate_by = 5


def MaterialNew(request):
    """Создание нового материала"""
    form = MaterialNewForm()
    materials_list = Materials.objects.all()
    error = ""

    if request.method == "POST":
        form = MaterialNewForm(request.POST, request.FILES)
        # проверка на присутсвие изделия в бд
        if materials_list.__len__() != 0:
            for material in materials_list:
                if form['code'].value() == material.code:
                    error = "Такой материал уже существует!"
                    break
                else:
                    if form.is_valid():
                        form.save()
                        return redirect(reverse('material_list'))
                    else:
                        error = "Форма неверно заполнена"
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('material_list'))
            else:
                error = "Форма неверно заполнена"
    return render(request, "materials/materials_form/materials_new.html", {"form": form, "error": error})


def MaterialDetailView(request, pk):
    """Просмотр подробности о материале"""
    material = Materials.objects.get(id=pk)
    context = {"material": material}
    return render(request, "materials/material_detail.html", context)


class MaterialUpdateView(UpdateView):
    """Обновление информации о материале"""
    model = Materials
    template_name = 'materials/materials_form/materials_new.html'
    form_class = MaterialNewForm
    slug_field = 'pk'
    success_url = '/material_list'


class MaterialDeleteView(DeleteView):
    """Удаление материала"""
    model = Materials
    # Изменить на список смесей
    success_url = '/material_list'
    template_name = "materials/materials_form/materials_delete.html"


# Поставщики
class SuppliersListView(ListView):
    """Список поставщиков"""
    model = Suppliers
    queryset = Suppliers.objects.all()
    template_name = "suppliers/suppliers_list.html"
    # paginate_by = 5


def SupplierNew(request):
    """Создание нового заказчика"""
    form = SupplierNewForm()
    error = ""
    if request.method == "POST":
        form = SupplierNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("supplier_list"))
        else:
            error = "Форма неверно заполнена"
    return render(request, "suppliers/supplier_form/supplier_new.html", {"form": form, "error": error})


def SuppliersDetailView(request, pk):
    """Просмотр подробности о поставщике"""
    OrderFormSet = inlineformset_factory(Suppliers, DeliveriesMaterials, fields=("code_material", "values"), extra=10)
    supplier = Suppliers.objects.get(id=pk)
    materials = DeliveriesMaterials.objects.filter(supplier_name=pk)
    formset = OrderFormSet(queryset=DeliveriesMaterials.objects.none(), instance=supplier)
    date = DeliveriesMaterials.objects.order_by().values('date').order_by("date").distinct()
    error = ""
    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=supplier)
        if formset.is_valid():
            formset.save()
            # перенаправление на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            error = formset.errors
    context = {"supplier": supplier, "formset": formset,
               "error": error, "date": date, "materials": materials}
    return render(request, "suppliers/suppliers_detail.html", context)


class SupplierUpdateView(UpdateView):
    """Редактирование информации о поставщике"""
    model = Suppliers
    template_name = "suppliers/supplier_form/supplier_new.html"
    success_url = "/supplier_list"
    form_class = SupplierNewForm


class SupplierDeleteView(DeleteView):
    """Удаление поставщика"""
    model = Suppliers
    # Изменить на список изделий
    success_url = "/supplier_list"
    template_name = "suppliers/supplier_form/supplier_delete.html"


# Склад изделий
class StorageGoodsListView(ListView):
    """Список изделий на складе"""
    model = GoodsStorage
    queryset = GoodsStorage.objects.all()
    template_name = "storage_goods/storage_goods_list.html"
    # paginate_by = 5


def StorageGoodsNew(request):
    """Создание нового изделия на склад"""
    form = GoodsStorageNewForm()
    error = ""
    if request.method == "POST":
        form = GoodsStorageNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("storage_goods_list"))
        else:
            error = "Форма неверно заполнена"
    return render(request, "storage_goods/goods_form/goods_new.html", {"form": form, "error": error})


def StorageGoodsDetailView(request, pk):
    """Просмотр подробности об изделии на складе"""
    goods = GoodsStorage.objects.get(id=pk)
    error = ""
    context = {"goods": goods, "error": error}
    return render(request, "storage_goods/storage_goods_detail.html", context)


class StorageGoodsUpdateView(UpdateView):
    """Редактирование информации об изделии на складе"""
    model = GoodsStorage
    template_name = "storage_goods/goods_form/goods_new.html"
    success_url = "/storage_goods_list"
    form_class = GoodsStorageNewForm


class StorageGoodsDeleteView(DeleteView):
    """Удаление изделия со склада"""
    model = GoodsStorage
    # Изменить на список изделий
    success_url = "/storage_goods_list"
    template_name = "storage_goods/goods_form/goods_delete.html"


# Склад материалов
class StorageMaterialsListView(ListView):
    """Список материалов на складе"""
    model = MaterialStorage
    queryset = MaterialStorage.objects.all()
    template_name = "storage_materials/storage_materials_list.html"
    # paginate_by = 5


def StorageMaterialsNew(request):
    """Создание нового материала на склад"""
    form = MaterialsStorageNewForm()
    error = ""
    if request.method == "POST":
        form = MaterialsStorageNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("storage_material_list"))
        else:
            error = "Форма неверно заполнена"
    return render(request, "storage_materials/materials_form/material_new.html", {"form": form, "error": error})


def StorageMaterialsDetailView(request, pk):
    """Просмотр подробности о материале на складе"""
    material = MaterialStorage.objects.get(id=pk)
    error = ""
    context = {"material": material, "error": error}
    return render(request, "storage_materials/storage_materials_detail.html", context)


class StorageMaterialsUpdateView(UpdateView):
    """Редактирование информации о материале на складе"""
    model = MaterialStorage
    template_name = "storage_materials/materials_form/material_new.html"
    success_url = "/"
    form_class = MaterialsStorageNewForm


class StorageMaterialsDeleteView(DeleteView):
    """Удаление материала со склада"""
    model = GoodsStorage
    # Изменить на список изделий
    success_url = "/"
    template_name = "storage_materials/materials_form/material_delete.html"


# Наряды
class NariadListView(ListView):
    """Список изделий на складе"""
    model = Nariad
    queryset = Nariad.objects.all()
    template_name = "nariad/nariad_list.html"
    # paginate_by = 5


def NariadNew(request):
    """Создание нового изделия на склад"""
    nariad_list = Nariad.objects.all()
    form = NariadNewForm()
    error = ""
    if request.method == "POST":
        form = NariadNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("nariad_list"))
        else:
            for nariad in nariad_list:
                if int(form['code'].value()) == nariad.code:
                    error = "Наряд с таким кодом уже существует"
                    break
                else:
                    error = "Форма неверно заполнена"
    return render(request, "nariad/nariad_form/nariad_new.html", {"form": form, "error": error})


def NariadDetailView(request, slug):
    """Просмотр подробности о наряде"""
    nariad = Nariad.objects.get(code=slug)
    error = ""
    context = {"nariad": nariad, "error": error}
    return render(request, "nariad/nariad_detail.html", context)


class NariadUpdateView(UpdateView):
    """Редактирование информации о наряде"""
    model = Nariad
    template_name = "nariad/nariad_form/nariad_new.html"
    success_url = "/"
    slug_field = 'code'
    form_class = NariadNewForm


class NariadDeleteView(DeleteView):
    """Удаление наряда"""
    model = Nariad
    # Изменить на список изделий
    success_url = "/"
    slug_field = 'code'
    template_name = "nariad/nariad_form/nariad_delete.html"


# ОТК
class OTKListView(ListView):
    """Список ОТК"""
    model = OTK
    queryset = OTK.objects.all()
    template_name = "otk/otk_list.html"
    # paginate_by = 5


def OTKDetailView(request, pk):
    """Просмотр подробности об ОТК"""
    otk = OTK.objects.get(id=pk)
    error = ""
    context = {"otk": otk, "error": error}
    return render(request, "otk/otk_detail.html", context)


def OTKNew(request):
    """Создание нового ОТК"""
    form = OTKNewForm()
    otk_list = OTK.objects.all()
    form_nariad = NariadNewForm()
    nariad_list = Nariad.objects.all()
    error = ""
    if request.method == "POST":
        for otk in otk_list:
            if form['nariad_code'] == otk.nariad_code:
                error = "ОТК с данным кодом уже существует!"
                break
            else:
                form = OTKNewForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect(reverse("otk_list"))
                else:
                    error = "Форма неверно заполнена"
    return render(request, "otk/otk_form/otk_new.html", {"form": form, "error": error, "form_nariad": form_nariad,
                                                         "nariad_list": nariad_list})


def OTKUpdateView(request, pk):
    """Редактирование информации о наряде"""
    otk = OTK.objects.get(id=pk)
    nariad = Nariad.objects.get(code=otk.nariad_code.code)
    form = OTKNewForm(instance=otk)
    form_nariad = NariadNewForm(instance=nariad)
    nariad_list = Nariad.objects.all()
    error = ""
    if request.method == "POST":
        form = OTKNewForm(request.POST, instance=otk)
        if form.is_valid():
            form.save()
            return redirect(reverse("otk_list"))
        else:
            error = "Форма неверно заполнена"
    return render(request, "otk/otk_form/otk_update.html", {"form": form, "error": error, "form_nariad": form_nariad,
                                                            "nariad_list": nariad_list})


class OTKDeleteView(DeleteView):
    """Удаление ОТК"""
    model = OTK
    # Изменить на список изделий
    success_url = "/"
    template_name = "otk/otk_form/otk_delete.html"


# Отчет о выпущенных изделиях
def ReportReleasedGoodsMonth(request):
    """Отчет о выпущенных изделиях за месяц"""
    summa_released_goods = 0
    # получение всех дат текущего месяца
    delta_date = days_cur_month(strdate='%d %B %Yг.')
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
              'Декабрь']
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year
    # дни
    date_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28, 29, 30, 31]
    get_date = months[datetime.today().month - 1]

    while date_days.__len__() != days_cur_month(strdate='%d %B %Yг.').__len__():
        del date_days[-1]

    nariad = Nariad.objects.filter(
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for nar in nariad:
        summa_released_goods += nar.goods_value

    report_released_goods_filter = ReportUsedMaterialFilter(request.GET, queryset=nariad)

    context = {"date": delta_date, "date_days": date_days, "months": months, "nariad": nariad,
               "summa_released_goods": summa_released_goods, "get_date": get_date,
               "report_released_goods_filter": report_released_goods_filter}
    return render(request, 'reports/goods_reports/released_goods/released_goods_report_month.html', context)


# Отчет о расходе материала
def ReportUsedMaterialMonth(request):
    """Отчет о расходе смеси за месяц"""
    summa_used_material = 0
    # получение всех дат текущего месяца
    delta_date = days_cur_month(strdate='%d %B %Yг.')
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
              'Декабрь']
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year
    # дни
    date_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28, 29, 30, 31]
    get_date = months[datetime.today().month - 1]

    while date_days.__len__() != days_cur_month(strdate='%d %B %Yг.').__len__():
        del date_days[-1]

    nariad = Nariad.objects.filter(
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for nar in nariad:
        summa_used_material += nar.used_materials

    report_used_material_filter = ReportUsedMaterialFilter(request.GET, queryset=nariad)

    context = {"date": delta_date, "date_days": date_days, "months": months, "nariad": nariad,
               "summa_used_material": summa_used_material, "get_date": get_date,
               "report_used_material_filter": report_used_material_filter}
    return render(request, 'reports/goods_reports/used_materials/used_materials_report_month.html', context)


def ReportUsedMaterialWeek(request):
    """Отчет о расходе смеси за неделю"""
    summa_used_material = 0
    # неделя
    week_now_days = week_now("%d %B %a")
    # дни
    date_days = week_now("%d")
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year

    nariad = Nariad.objects.filter(
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for days in date_days:
        for nariad_days in nariad:
            if int(days) == nariad_days.date.day:
                summa_used_material += nariad_days.remote_value

    report_used_material_filter = ReportUsedMaterialFilter(request.GET, queryset=nariad)

    context = {"nariad": nariad, "week_now_days": week_now_days, "date_days": date_days,
               "summa_used_material": summa_used_material, "report_used_material_filter": report_used_material_filter}
    return render(request, 'reports/goods_reports/used_materials/used_materials_report_week.html', context)


def ReportUsedMaterialToday(request):
    """Отчет о списанных изделиях за день"""
    summa_used_material = 0
    # день
    date_day = datetime.today().day
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year

    # надпись в шапку
    delta_date = datetime.today().date()

    nariad = Nariad.objects.filter(
        Q(date__day=date_day) &
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for nar in nariad:
        summa_used_material += nar.remote_value

    report_used_material_filter = ReportUsedMaterialFilter(request.GET, queryset=nariad)

    context = {"nariad": nariad, "summa_used_material": summa_used_material, "date_day": date_day,
               "delta_date": delta_date, "report_used_material_filter": report_used_material_filter}
    return render(request, 'reports/goods_reports/used_materials/used_materials_report_today.html', context)


def ReportUsedMaterialCalendar(request):
    """Отчет по календарю"""
    summa_used_material = 0

    # дата начала
    start_date = request.GET.get('start_date')
    start_date = start_date.split("-")
    start_date[0] = int(start_date[0])
    start_date[1] = int(start_date[1])
    start_date[2] = int(start_date[2])
    # дата окончания
    end_date = request.GET.get('end_date')
    end_date = end_date.split("-")
    end_date[0] = int(end_date[0])
    end_date[1] = int(end_date[1])
    end_date[2] = int(end_date[2])

    # дни для вывода
    delta_days = calendar(s_date=start_date, e_date=end_date, strdate='%Y-%m-%d')
    # календарь
    delta_date = calendar(s_date=start_date, e_date=end_date, strdate='%d %B %Yг.')

    nariad = Nariad.objects.all()
    report_used_material_filter = ReportUsedMaterialFilter(request.GET, queryset=nariad)
    nariad = report_used_material_filter.qs

    for nari in nariad:
        summa_used_material += nari.used_materials

    context = {"report_used_material_filter": report_used_material_filter, "nariad": nariad,
               "delta_days": delta_days, "delta_date": delta_date,
               "summa_used_material": summa_used_material}
    return render(request, 'reports/goods_reports/used_materials/used_materials_report_calendar.html', context)


# Отчет о списанных изделиях
def ReportRemoteGoodsMonth(request):
    """Отчет о списанных изделиях за месяц"""
    summa_remote_goods = 0
    # получение всех дат текущего месяца
    delta_date = days_cur_month(strdate='%d %B %Yг.')
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь',
              'Декабрь']
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year
    # дни
    date_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                 28, 29, 30, 31]
    get_date = months[datetime.today().month - 1]

    while date_days.__len__() != days_cur_month(strdate='%d %B %Yг.').__len__():
        del date_days[-1]

    otk = OTK.objects.filter(
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for otks in otk:
        summa_remote_goods += otks.remote_value

    report_remote_goods_filter = ReportRemoteGoodsFilter(request.GET, queryset=otk)

    context = {"date": delta_date, "date_days": date_days, "months": months, "otk": otk,
               "summa_remote_goods": summa_remote_goods, "get_date": get_date,
               "report_remote_goods_filter": report_remote_goods_filter}
    return render(request, 'reports/goods_reports/remote_goods/remote_goods_report_month.html', context)


def ReportRemoteGoodsWeek(request):
    """Отчет о списанных изделиях за неделю"""
    summa_remote_goods = 0
    # неделя
    week_now_days = week_now("%d %B %a")
    # дни
    date_days = week_now("%d")
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year

    otk = OTK.objects.filter(
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for days in date_days:
        for goods_days in otk:
            if int(days) == goods_days.date.day:
                summa_remote_goods += goods_days.remote_value

    report_remote_goods_filter = ReportRemoteGoodsFilter(request.GET, queryset=otk)

    context = {"otk": otk, "week_now_days": week_now_days, "date_days": date_days,
               "summa_remote_goods": summa_remote_goods, "report_remote_goods_filter": report_remote_goods_filter}
    return render(request, 'reports/goods_reports/remote_goods/remote_goods_report_week.html', context)


def ReportRemoteGoodsToday(request):
    """Отчет о списанных изделиях за день"""
    summa_remote_goods = 0
    # день
    date_day = datetime.today().day
    # месяц
    date_month = datetime.today().month
    # год
    date_year = datetime.today().year

    # надпись в шапку
    delta_date = datetime.today().date()

    otk = OTK.objects.filter(
        Q(date__day=date_day) &
        Q(date__month=date_month) &
        Q(date__year=date_year)
    ).order_by('date').distinct()

    for otks in otk:
        summa_remote_goods += otks.remote_value

    report_remote_goods_filter = ReportRemoteGoodsFilter(request.GET, queryset=otk)

    context = {"otk": otk, "summa_remote_goods": summa_remote_goods, "date_day": date_day, "delta_date": delta_date,
               "report_remote_goods_filter": report_remote_goods_filter}
    return render(request, 'reports/goods_reports/remote_goods/remote_goods_report_today.html', context)


def ReportRemoteGoodsCalendar(request):
    """Отчет по календарю"""
    summa_remote_goods = 0

    # дата начала
    start_date = request.GET.get('start_date')
    start_date = start_date.split("-")
    start_date[0] = int(start_date[0])
    start_date[1] = int(start_date[1])
    start_date[2] = int(start_date[2])
    # дата окончания
    end_date = request.GET.get('end_date')
    end_date = end_date.split("-")
    end_date[0] = int(end_date[0])
    end_date[1] = int(end_date[1])
    end_date[2] = int(end_date[2])

    # дни для вывода
    delta_days = calendar(s_date=start_date, e_date=end_date, strdate='%Y-%m-%d')
    # календарь
    delta_date = calendar(s_date=start_date, e_date=end_date, strdate='%d %B %Yг.')

    otk = OTK.objects.all()
    otkfilter = ReportRemoteGoodsFilter(request.GET, queryset=otk)
    otk = otkfilter.qs

    for otks in otk:
        summa_remote_goods += otks.remote_value

    context = {"otkfilter": otkfilter, "otk": otk, "delta_days": delta_days, "delta_date": delta_date,
               "summa_remote_goods": summa_remote_goods}
    return render(request, 'reports/goods_reports/remote_goods/remote_goods_report_calendar.html', context)