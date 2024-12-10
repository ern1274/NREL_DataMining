from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("geocode", views.geocode_view, name="geocode_view"),
    path("reset_points", views.reset_region_and_points, name="reset_region_and_points"),
    path("preverify_export", views.preverify_export, name="preverify_export"),
    path("export", views.export_view, name="export_view"),
    path("attribute_filter", views.attribute_filter_view, name="attribute_filter_view")

]