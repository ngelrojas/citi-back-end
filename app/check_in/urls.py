# urls.py

from django.urls import path
from .views import JSONFileView

urlpatterns = [
    path('json-files/', JSONFileView.as_view({"get": "get"}), name='json_files'),
]
