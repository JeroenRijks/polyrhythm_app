from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^home/$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^create/$', views.PolyrhythmEdit.as_view(), name='polyrhythm_edit'),
    url(r'^create/(?P<poly_id>[0-9]+)$', views.PolyrhythmEdit.as_view(), name='polyrhythm_edit'),
    url(r'^display/(?P<poly_id>[0-9]+)$', views.PolyrhythmDisplay.as_view(), name='polyrhythm_display'),

]
