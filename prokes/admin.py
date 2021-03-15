from django.contrib import admin
from .models import *

admin.site.register(Workers)
admin.site.register(Materials)
admin.site.register(Goods)
admin.site.register(GoodsDefaultForm)


@admin.register(GoodsCalendar)
class GoodsCalendarAdmin(admin.ModelAdmin):
    list_display = ("goods_code", "month")
    search_fields = ("goods_code",)


admin.site.register(Customer)
admin.site.register(CheckoutGoods)
admin.site.register(Suppliers)
admin.site.register(DeliveriesMaterials)

admin.site.register(Nariad)
admin.site.register(OTK)
admin.site.register(GoodsStorage)
admin.site.register(MaterialStorage)
