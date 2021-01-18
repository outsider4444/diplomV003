from django.contrib import admin
from .models import UnitsMeasurement, Workers, WorkTime, Goods, Customers, Smesi, Suppliers, Remote

# Register your models here.

admin.site.register(UnitsMeasurement)
admin.site.register(Workers)
admin.site.register(WorkTime)
admin.site.register(Goods)
admin.site.register(Customers)
admin.site.register(Smesi)
admin.site.register(Suppliers)
admin.site.register(Remote)
