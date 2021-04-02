from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from requests import request

from .forms import *

from .models import *


# Главная страница
def main(request):
    """Главное меню"""
    return render(request, "main/main.html")


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
    paginate_by = 5


def WorkerNew(request):
    """Создание нового сотрудника"""
    form = WorkersForm()
    error = ""
    if request.method == "POST":
        form = WorkersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("workers_list")
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
    success_url = "/"
    slug_field = "code"
    form_class = WorkersForm


class WorkerDeleteView(DeleteView):
    """Удаление сотрудника"""
    model = Workers
    # Изменить на список изделий
    slug_field = 'code'
    success_url = "/"
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
            return redirect("workers_list")
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
    success_url = "/"
    form_class = CustomerForm


class CustomerDeleteView(DeleteView):
    """Удаление заказчика"""
    model = Customer
    # Изменить на список изделий
    success_url = "/"
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
        else:
            error = "Форма неверно заполнена"
    context = {"calendar": calendar, "goods": goods, "form": form, "error": error,
               "goods_form": goods_form, }
    return render(request, "goods/goods_detail.html", context)


class GoodsUpdateView(UpdateView):
    """Редактирование информации о детали"""
    model = Goods
    template_name = "goods/goods_form/goods_new.html"
    success_url = "goods_list"
    form_class = GoodsForm


def GoodsNew(request):
    """Создание нового изделия"""
    form = GoodsForm()
    error = ""
    if request.method == "POST":
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("goods_list")
        else:
            error = "Форма неверно заполнена"
    return render(request, "goods/goods_form/goods_new.html", {"form": form, "error": error})


class GoodsDeleteView(DeleteView):
    """Удаление изделия"""
    model = Goods
    # Изменить на список изделий
    success_url = "/"
    template_name = "goods/goods_form/goods_delete.html"


class GoodsFormUpdateView(UpdateView):
    """Обновление информации о форме изделия"""
    model = GoodsDefaultForm
    template_name = 'goods/goods_form/def_form/goods_def_form_update.html'
    form_class = FormsGoodsForm
    slug_field = 'pk'


class GoodsFormDeleteView(DeleteView):
    """Удаление изделия"""
    model = GoodsDefaultForm
    # Изменить на список изделий
    success_url = "/"
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
            return redirect("goods_list")
        else:
            error = "Форма неверно заполнена"
    return render(request, 'goods/goods_form/def_form/goods_def_form_new.html', {"form": form,
                                                                        "error": error, "goods": goods})


# Фильтры для изделий
# class FilterGoodsView(ListView):
#     """Фильтр изделий"""
#     template_name = "goods/nariad_list.html"
#
#     def get_queryset(self):
#         queryset = ""
#         temp = self.request.GET.get("temp")
#         malt = self.request.GET.get("malt")
#         pres = self.request.GET.get("pres")
#         strength = self.request.GET.get("strength")
#         if temp == "" and malt == "" and pres == "" and strength == "":
#             queryset = Goods.objects.all()
#         elif temp != "" and malt != "" and pres != "" and strength != "":
#             queryset = Goods.objects.filter(
#                 Q(min_temperature__lte=int(temp)) &
#                 Q(min_malt__lte=int(malt)) &
#                 Q(min_pressure__lte=int(pres)) &
#                 Q(min_strength__lte=int(strength))
#             ).distinct()
#         elif temp != "" and malt != "" and pres != "":
#             queryset = Goods.objects.filter(
#                 Q(min_temperature__lte=int(temp)) &
#                 Q(min_malt__lte=int(malt)) &
#                 Q(min_pressure__lte=int(pres))
#             ).distinct()
#         elif temp != "" and malt != "" and strength != "":
#             queryset = Goods.objects.filter(
#                 Q(min_temperature__lte=int(temp)) &
#                 Q(min_malt__lte=int(malt)) &
#                 Q(min_strength__lte=int(strength))
#             ).distinct()
#         elif temp != "" and pres != "" and strength != "":
#             queryset = Goods.objects.filter(
#                 Q(min_temperature__lte=int(temp)) &
#                 Q(min_pressure__lte=int(pres)) &
#                 Q(min_strength__lte=int(strength))
#             ).distinct()
#         elif malt != "" and pres != "" and strength != "":
#             queryset = Goods.objects.filter(
#                 Q(min_malt__lte=int(malt)) &
#                 Q(min_pressure__lte=int(pres)) &
#                 Q(min_strength__lte=int(strength))
#             ).distinct()
#         elif temp != "":
#             queryset = Goods.objects.filter(
#                 Q(min_temperature__lte=int(temp))
#             ).distinct()
#         elif malt != "":
#             queryset = Goods.objects.filter(
#                 Q(min_malt__lte=int(malt))
#             ).distinct()
#         elif pres != "":
#             queryset = Goods.objects.filter(
#                 Q(min_pressure__lte=int(pres))
#             ).distinct()
#         elif strength != "":
#             queryset = Goods.objects.filter(
#                 Q(min_strength__lte=int(strength))
#             ).distinct()
#         return queryset
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["temp"] = ''.join([f"temp={x}&" for x in self.request.GET.getlist("temp")])
#         context["malt"] = ''.join([f"malt={x}&" for x in self.request.GET.getlist("malt")])
#         context["pres"] = ''.join([f"pres={x}&" for x in self.request.GET.getlist("pres")])
#         context["strength"] = ''.join([f"strength={x}&" for x in self.request.GET.getlist("strength")])
#         return context
#
#
# # Отдел поиска
# class SearchGoods(ListView):
#     """Поиск изделий"""
#     template_name = "goods/nariad_list.html"
#
#     def get_queryset(self):
#         return Goods.objects.filter(code__icontains=self.request.GET.get("q"))
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["q"] = f'q={self.request.GET.get("q")}&'
#         return context

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
    error = ""
    if request.method == "POST":
        form = MaterialNewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("material_list")
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
    success_url = '/'


class MaterialDeleteView(DeleteView):
    """Удаление материала"""
    model = Materials
    # Изменить на список смесей
    success_url = '/'
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
            return redirect("supplier_list")
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
    success_url = "/"
    form_class = SupplierNewForm


class SupplierDeleteView(DeleteView):
    """Удаление поставщика"""
    model = Suppliers
    # Изменить на список изделий
    success_url = "/"
    template_name = "suppliers/supplier_form/supplier_delete.html"


# Склад изделия
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
            return redirect("storage_goods_list")
        else:
            error = "Форма неверно заполнена"
    return render(request, "storage_goods/goods_form/goods_new.html", {"form": form, "error": error})


class StorageGoodsUpdateView(UpdateView):
    """Редактирование информации об изделии на складе"""
    model = GoodsStorage
    template_name = "storage_goods/goods_form/goods_new.html"
    success_url = "/"
    form_class = GoodsStorageNewForm


class StorageGoodsDeleteView(DeleteView):
    """Удаление изделия со склада"""
    model = GoodsStorage
    # Изменить на список изделий
    success_url = "/"
    template_name = "storage_goods/goods_form/goods_delete.html"


def StorageGoodsDetailView(request, pk):
    """Просмотр подробности об изделии на складе"""
    goods = GoodsStorage.objects.get(id=pk)
    error = ""
    context = {"goods": goods, "error": error}
    return render(request, "storage_goods/storage_goods_detail.html", context)


# Наряды
class NariadListView(ListView):
    """Список изделий на складе"""
    model = Nariad
    queryset = Nariad.objects.all()
    template_name = "nariad/nariad_list.html"
    # paginate_by = 5


def NariadNew(request):
    """Создание нового изделия на склад"""
    form = NariadNewForm()
    error = ""
    if request.method == "POST":
        form = NariadNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nariad_list")
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
    form_nariad = NariadNewForm()
    nariad_list = Nariad.objects.all()
    error = ""
    if request.method == "POST":
        form = OTKNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("otk_list")
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
            return redirect("otk_list")
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
