from django.contrib import admin
from .models import Room, RoomType

# Register your models here.
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'on_off','room_user', 'user_id', 'user_passwd', 'room_name', 'room_type', 'start_time', 'end_time', 'members')
