from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^home$', views.PolyrhythmList.as_view(), name='polyrhythm_list'),
    url(r'^create$', views.PolyrhythmForm.as_view(), name='polyrhythm_form'),

]
