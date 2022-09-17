from django.urls import path


from . import views

app_name = 'data'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload, name='upload'),
    path('doc_table', views.doc_table, name='doc_table'),
    path('doc<int:pk>/summary', views.summary_view, name='summary'),
    path('doc<int:pk>/questions', views.questions_view, name='questions'),
]
