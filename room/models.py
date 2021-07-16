from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING

# Create your models here.
# 房间类型
class RoomType(models.Model):
    type_name = models.CharField(max_length = 15)

    def __str__(self) -> str:
        return self.type_name # 管理员界面显示分类名称

# 设置每个房间
class Room(models.Model):
    on_off = models.BooleanField(default = False) # 是否启用预约
    room_user = models.ForeignKey(User, on_delete = DO_NOTHING) # 用户
    user_id = models.CharField(max_length = 15) # 用户学号
    user_passwd = models.CharField(max_length = 15) # 用户密码
    room_name = models.CharField(max_length = 15) # 房间号
    room_type = models.ForeignKey(RoomType, on_delete = models.DO_NOTHING) # 房间类型外键
    start_time = models.TimeField() # 开始时间
    end_time = models.TimeField() # 结束时间
    members = models.TextField(default = 'None') # 研修室成员