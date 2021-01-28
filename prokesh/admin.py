from django.contrib import admin
from .models import UnitsMeasurement, Workers, WorkTime, Goods, Customers, Smesi, Suppliers, Remote


# Register your models here.


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "email", "fired")
    list_display_links = ("name",)
    search_fields = ("name", "category")
    list_editable = ("fired",)


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ("worker_name", "standard_time", "date_vacation")
    search_fields = ("worker_name",)


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("code", "cleaning_period", "number_nest")
    search_fields = ("code",)
    fieldsets = (
        (None, {
            "fields": ("code", "url")
        }),
        (None, {
            "fields": (("cleaning_period", "number_nest"),)
        }),
        (None, {
            "fields": (("percent_mass", "weight_clean"),)
        }),
        (None, {
            "fields": (("norma_with_carpet", "consumption_smesi", "defect_limit"),)
        }),
        (None, {
            "fields": (("one_person_norma", "two_person_norma"),)
        }),

        (None, {
            "fields": (("min_temperature", "max_temperature"),)
        }),
        (None, {
            "fields": (("min_malt", "max_malt"),)
        }),
        (None, {
            "fields": (("min_pressure", "max_pressure"),)
        }),
        (None, {
            "fields": (("min_strength", "max_strength"),)
        }),
    )


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "email")
    search_fields = ("name",)


@admin.register(Smesi)
class SmesiAdmin(admin.ModelAdmin):
    list_display = ("code", "value", "date")
    search_fields = ("code",)


@admin.register(Remote)
class RemoteAdmin(admin.ModelAdmin):
    list_display = ("id", "delete_date", "name", "value")
    list_display_links = ("delete_date",)
    search_fields = ("delete_date",)


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "email")
    search_fields = ("name",)


admin.site.register(UnitsMeasurement)



