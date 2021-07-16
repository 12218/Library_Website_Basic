from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, RoomType
from django.core.paginator import Paginator
from django.db.models import Count # 导入计数方法
from django.conf import settings
from django.contrib import auth

# Create your views here.
# 分页函数
def divid_room_pages(request, all_rooms):
    paginator = Paginator(all_rooms, settings.EACH_PAGE_ROOM_NUM) # 分页，每10条分一页

    page_num = request.GET.get('page', 1) # request.GET得到get请求中的内容; 此处查看get请求中有没有page这个属性，没有则为1
    page_of_rooms = paginator.get_page(page_num) # 获取分页后的房间分类
    current_page_num = page_of_rooms.number # 获取当前页码
    # 获取当前页码及前后2页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
        list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上页码之间的省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 保留首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    room_types = RoomType.objects.annotate(room_count = Count('type_name'))

    context = {}
    context['rooms'] = page_of_rooms
    context['room_types'] = room_types
    context['page_range'] = page_range

    return context

# 所有房间预约信息
def room_list(request):
    # context = {}
    # context['rooms'] = Room.objects.all() # 获取全部房间信息
    # context['room_types'] = RoomType.objects.all() # 获取全部分类
    all_rooms = Room.objects.all() # 获取全部房间信息
    context = divid_room_pages(request, all_rooms)
    return render(request, 'room_list.html', context)

# 房间预约详情
def room_detail(request, room_pk):
    context = {}
    context['room_detail'] = get_object_or_404(Room, id = room_pk)
    context['room_types'] = RoomType.objects.all() # 获取全部分类
    context['room_type_1'] = RoomType.objects.all()[0]
    context['room_type_2'] = RoomType.objects.all()[1]
    context['user'] = request.user # 登录验证
    return render(request, 'room_detail.html', context)

# 某房间分类列表
def room_type_list(request, type_id):
    room_type = get_object_or_404(RoomType, pk = type_id)
    all_rooms = Room.objects.filter(room_type = room_type)
    # context = {}
    # context['room_types'] = RoomType.objects.all() # 获取全部分类
    # type_list = Room.objects.filter(room_type = room_type)
    # context['room_type'] = room_type
    # context['rooms'] = type_list
    context = divid_room_pages(request, all_rooms)
    context['room_type'] = room_type
    return render(request, 'room_type_list.html', context)

# 用户所有预约页面
def my_page(request):
    if request.user.username != '': # 如果登录成功
        all_rooms = Room.objects.filter(room_user = request.user) # 获取全部房间信息
        context = divid_room_pages(request, all_rooms)
        context['username'] = request.user.username
        context['user'] = request.user # 登录验证
    else:
        all_rooms = Room.objects.filter(room_user = 8) # 获取全部房间信息
        context = divid_room_pages(request, all_rooms)
        context['username'] = ''
        context['user'] = request.user # 登录验证
    return render(request, 'personal_page.html', context)

# 登录函数
def login(request):
    username = request.POST.get('username', '') # 从request中取出username字段，如果没有则设为空字符串
    password = request.POST.get('password', '')

    user = auth.authenticate(request, username = username, password = password) # 获取登录信息
    if user is not None:
        auth.login(request, user)
        return redirect('/') # 重定向到首页
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确', 'title': '登录错误'}) # 跳转错误页面

# 提交信息
def submit_info(request):
    roomid = request.POST.get('roomid')
    if request.POST.get('on_off', 'False') == 'False':
        on_off = False
    else:
        on_off = True
    user_id = request.POST.get('user_id', '')
    user_passwd = request.POST.get('user_passwd', '')
    room_name = request.POST.get('room_name', '')
    room_type = request.POST.get('room_type', '')
    start_time = request.POST.get('start_time', '')
    end_time = request.POST.get('end_time', '')
    members = request.POST.get('members', 'None')

    try:
        room = get_object_or_404(Room, id = roomid)
        room.on_off = on_off
        room.user_id = user_id
        room.user_passwd = user_passwd
        room.room_name = room_name
        type_obj = RoomType.objects.filter(type_name = room_type)[0] # 筛选出房间类型对象
        room.room_type = type_obj
        room.start_time = start_time
        room.end_time = end_time
        room.members = members
        room.save()

        return redirect('/room/' + roomid) # 重定向到详情界面

    except:
        # return redirect('/room/' + roomid) # 重定向到详情界面
        return render(request, 'error.html', {'message': '用户名或密码不正确', 'title': '登录错误'}) # 跳转错误页面