from django.contrib import admin
from .models import Goods, GoodsDefaultForm, GoodsCalendar, Workers

admin.site.register(Workers)


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = ("code",)
    fieldsets = (
        (None, {
            "fields": ("code",)
        }),
        (None, {
            "fields": ("image",)
        }),

        (None, {
            "fields": ("weight_clean",)
        }),
        (None, {
            "fields": (("norma_with_carpet", "consumption_smesi", "defect_limit"),)
        }),
        (None, {
            "fields": ("one_person_norma",)
        }),
    )


@admin.register(GoodsCalendar)
class GoodsCalendarAdmin(admin.ModelAdmin):
    list_display = ("code_goods", "month")
    search_fields = ("code_goods",)


admin.site.register(GoodsDefaultForm)
