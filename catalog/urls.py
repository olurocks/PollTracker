from .views import *
from django.urls import path

# myproject/urls.py

urlpatterns = [
    # ...
    path('polling_unit/<int:polling_unit_uniqueid>/',polling_unit_result, name='polling_unit_result'),
    path('lga-result/', lga_result, name='lga_result'),
    path('add_polling_unit_result/', add_polling_unit_result,name='add_polling_unit_result'),
    path('view_poll_result/', view_poll_result, name='view_poll_result'),
    path('',home,name='home')


]
