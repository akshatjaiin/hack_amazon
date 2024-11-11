from django.urls import path
from django.conf.urls import handler404, handler403, handler400
from . import views

# Point all errors to the generic custom_error view
handler404 = 'amaze.views.custom_error'
handler403 = 'amaze.views.custom_error'
handler400 = 'amaze.views.custom_error'

# Other URL patterns here
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
]
