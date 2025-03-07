from django.shortcuts import render



def index(request):
    context = {
        'title': 'my project',
        'main_page': 'welcome',
    }
    return render(request, 'main/index.html', context)
