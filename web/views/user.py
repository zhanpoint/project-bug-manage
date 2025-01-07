from django.shortcuts import render
from web.forms.register import RegisterModelForm


def register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = RegisterModelForm()

    return render(request, 'web/register.html', {'form': form})
