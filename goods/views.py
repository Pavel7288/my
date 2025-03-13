from django.shortcuts import render


def catalog(request):
    context = {
        'title': 'Goods',
    }
    return render(request, 'main/catalog.html', context)


def product(request):
    context = {
        'title': 'Description',
    }
    return render(request, 'main/description.html', context)


def make_order(request):
    context = {
        'title': 'Orders',
    }
    return render(request, 'main/basket.html', context)
