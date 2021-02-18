from django.contrib import admin
from .models import Goods, GoodsForm, GoodsCalendar


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("code",)
    search_fields = ("code",)
    fieldsets = (
        (None, {
            "fields": ("code", "url")
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
        # (None, {
        #     "fields": (("one_person_norma", "two_person_norma"),)
        # }),

        # (None, {
        #     "fields": (("min_temperature", "max_temperature"),)
        # }),
        # (None, {
        #     "fields": (("min_malt", "max_malt"),)
        # }),
        # (None, {
        #     "fields": (("min_pressure", "max_pressure"),)
        # }),
        # (None, {
        #     "fields": (("min_strength", "max_strength"),)
        # }),
        # (None, {
        #     "fields": ("measurement",)
        # }),
    )


@admin.register(GoodsCalendar)
class GoodsCalendarAdmin(admin.ModelAdmin):
    list_display = ("code_goods", "month")
    search_fields = ("code_goods",)


admin.site.register(GoodsForm)
