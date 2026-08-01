from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, custom_404_view
from portfolio.views import submit_testimonial_view

# Custom 404 handler
handler404 = custom_404_view

urlpatterns = [
    path('', home_view, name='home'),
    path('submit-feedback/', submit_testimonial_view, name='submit-testimonial'),
    path('hawa/', admin.site.urls),
    path('api/', include('portfolio.urls')),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


