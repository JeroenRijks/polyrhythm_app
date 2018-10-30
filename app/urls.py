from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^home/$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^rhythms/$', views.RhythmsEdit.as_view(), name='rhythms_edit'),
    url(r'^rhythms/(?P<poly_id>[0-9]+)$', views.RhythmsEdit.as_view(), name='rhythms_edit'),
    url(r'^beats/$', views.BeatsEdit.as_view(), name='beats_edit'),
    url(r'^beats/(?P<poly_id>[0-9]+)$', views.BeatsEdit.as_view(), name='beats_edit'),
    url(r'^display/(?P<poly_id>[0-9]+)$', views.PolyrhythmDisplay.as_view(), name='polyrhythm_display'),

]

