from django.urls import path
from . import views

urlpatterns = [
    path('<int:room_pk>', views.room_detail, name = 'room_detail'),
    path('type/<int:type_id>', views.room_type_list, name = 'room_type_list'),
    path('person/', views.my_page, name = 'my_page'),
]