from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("geocode", views.geocode_view, name="geocode_view"),
    path("reset_points", views.reset_region_and_points, name="reset_region_and_points"),
    path("export", views.export_view, name="export_view"),
    path("attribute_filter", views.attribute_filter_view, name="attribute_filter_view"),
    path("reset_filter_attributes", views.reset_filter_attributes, name="reset_filter_attributes"),
    path("delete_filter_attribute", views.delete_filter_attribute, name="delete_filter_attribute"),
    path("sorted_results", views.sorted_results_view, name="sorted_results_view")

]