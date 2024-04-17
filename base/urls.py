from django.urls import path
from .views import  upload_marks
from .mark_views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('upload/', upload_marks, name='upload_marks'),
]