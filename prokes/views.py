from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View, CreateView
from django.shortcuts import render, redirect
from requests import request

from .forms import GoodsForm, CalendarForm

from .models import Goods, GoodsCalendar, UnitsMeasurement


class GoodsView(ListView):
    """Список изделий"""
    model = Goods
    queryset = Goods.objects.all()
    template_name = "goods/goods_list.html"
    paginate_by = 5


def GoodsDetailView(request, slug):
    """Полная информация об изделии"""
    # model = Goods
    # slug_field = "url"
    # template_name = "goods/goods_detail.html"
    error = ""
    goods = Goods.objects.get(url=slug)
    calendar = GoodsCalendar.objects.filter(code_goods=goods.code).order_by("month")
    month = GoodsCalendar.objects.all()
    if request.method == "POST":
        form = CalendarForm(request.POST)
        form.code_goods = goods.code
        if form.is_valid():
            form.save()
            return redirect("goods_list")
        else:
            error = "Форма неверно заполнена"
    form = CalendarForm()
    return render(request, "goods/goods_detail.html", {"calendar": calendar, "goods": goods,
                                                       "form": form, "error": error})


def GoodsNew(request):
    """Создание нового изделия"""
    error = ""
    if request.method == "POST":
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("goods_list")
        else:
            error = "Форма неверно заполнена"
    form = GoodsForm()
    return render(request, "goods/goods_new.html", {"form": form, "error": error})
    # def get(self, request):
    #     goods = Goods.objects.all()
    #     measurement = UnitsMeasurement.objects.all()
    #     return render(request, "goods/goods_new.html", {"measurement": measurement, "goods": goods})


class AddGoods(View):
    """Добавить издилие в список изделий"""
    pass


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

class SearchGoods(ListView):
    """Поиск изделий"""
    template_name = "goods/goods_list.html"

    def get_queryset(self):
        return Goods.objects.filter(code__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
