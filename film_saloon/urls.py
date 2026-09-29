from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse,HttpResponse
from django.urls import path,include

def manifest(request):
    return JsonResponse({
        "name":"FILM SALOON","short_name":"FILM SALOON","start_url":"/","scope":"/",
        "display":"standalone","background_color":"#000000","theme_color":"#000000",
        "description":"Movies, Reviews, More.",
        "icons":[
            {"src":"/static/icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any maskable"},
            {"src":"/static/icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}
        ]
    })
def service_worker(request):
    p=settings.STATICFILES_DIRS[0]/"service-worker.js"
    return HttpResponse(p.read_text(encoding="utf-8"),content_type="application/javascript")
urlpatterns=[
    path("admin/",admin.site.urls),
    path("manifest.json",manifest,name="manifest"),
    path("service-worker.js",service_worker,name="service_worker"),
    path("",include("movies.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
