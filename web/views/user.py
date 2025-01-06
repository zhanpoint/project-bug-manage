import random
from Bug_manage import settings
from utils.aliyun import Sample
from django.shortcuts import render, HttpResponse
from test.myforms import RegisterModelForm


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = RegisterModelForm()

    return render(request, 'web/register.html', {'form': form})
