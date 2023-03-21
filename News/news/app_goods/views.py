from _csv import reader
from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from app_goods.models import Item
from app_goods.forms import UploadPriceForm
from django.urls import reverse


def items_list(request):
    items = Item.objects.all()
    return render(request, 'app_goods/items_list.html', {'items_list': items})

def update_prices(request):
    if request.method == 'POST':
        upload_file_form = UploadPriceForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            price_file = upload_file_form.cleaned_data['file'].read()
            price_str = price_file.decode('utf-8').split('\n')
            csv_reader = reader(price_str, delimiter=':', quotechar='"')
            for row in csv_reader:
                Item.objects.filter(code=row[0]).update(price=Decimal(row[1]))
            return HttpResponseRedirect(reverse('items_list'))
    else:
        upload_file_form = UploadPriceForm()

    context = {
        'form': upload_file_form
    }
    return render(request, 'app_goods/upload_file.html', context=context)