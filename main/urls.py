from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import main.views

app_name = "main"
urlpatterns = [
    path('', main.views.index, name='main_page'),
    path('about/', main.views.about, name='about_us'),
    path('opo/', main.views.something, name='button'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
