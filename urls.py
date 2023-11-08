from django.urls import path
from .views import DataListView, AddDataView, EditDataView, DeleteDataView

urlpatterns = [
    path('', DataListView.as_view(), name='data_list'),
    path('add/', AddDataView.as_view(), name='add_data'),
    path('edit/<str:username>/', EditDataView.as_view(), name='edit_data'),
    path('delete/<str:username>/', DeleteDataView.as_view(), name='delete_data'),
]