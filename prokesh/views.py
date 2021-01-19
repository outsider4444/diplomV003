from django.shortcuts import render
from django.views.generic.base import View

from .models import Workers, Category


# Create your views here.


class WorkerView(View):
    """Список сотрудников"""

    def get(self, request):
        workers = Workers.objects.all()
        return render(request, "workers/worker_list.html", {"worker_list": workers})
