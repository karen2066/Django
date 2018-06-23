from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from app.models import MainWheel, MainNav, MainMustBuy, MainShop,\
    MainShow, FoodType, Goods, CartModel, OrderModel, OrderGoodsModel
from django.core.urlresolvers import reverse

from utils.functions import get_order_random_id


def home(request):

    '''
    首页视图函数
    '''
    if request.method == 'GET':
        mainwheels = MainWheel.objects.all()
        mainnavs = MainNav.objects.all()
        mainbuys = MainMustBuy.objects.all()
        mainshops = MainShop.objects.all()
        mainshows = MainShow.objects.all()
        data = {
            'title': '首页',
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainbuys': mainbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,
        }
        return render(request, 'home/home.html', data)


def mine(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user_id=user.id)
        payed, wait_pay = 0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            if order.o_status == 1:
                payed += 1
        data = {
            'payed': payed,
            'wait_pay': wait_pay
        }
        return render(request, 'mine/mine.html', data)


def market(request):
    if request.method == 'GET':

        return HttpResponseRedirect(reverse('axf:market_params', args=('104749', '0', '0')))


def user_market(request, typeid, cid, sid):
    if request.method == 'GET':
        foodtypes = FoodType.objects.all()

        if cid == '0':
            goods = Goods.objects.filter(categoryid=typeid)
        else:
            goods = Goods.objects.filter(categoryid=typeid,
                                         childcid=cid)

        foodtypes_current = foodtypes.filter(typeid=typeid).first()

        if foodtypes_current:
            childtypes = foodtypes_current.childtypenames
            childtypenames = childtypes.split('#')
            child_list = []
            for childtypename in childtypenames:
                child_type_info = childtypename.split(':')
                child_list.append(child_type_info)

        if sid == '0':
            pass
        if sid == '1':
            goods = goods.order_by('productnum')
        if sid == '2':
            goods = goods.order_by('-price')
        if sid == '3':
            goods = goods.order_by('price')

        data = {
            'foodtypes': foodtypes,
            'goods': goods,
            'typeid': typeid,
            'child_list': child_list,
            'cid': cid,
        }
        return render(request, 'market/market.html', data)


def add_cart(request):
    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {'code': 200,
                'msg': '请求成功'}
        if user.id:
            user_carts = CartModel.objects.filter(user_id=user.id,
                                                  goods_id=goods_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CartModel.objects.create(user_id=user.id,
                                         goods_id=goods_id)
                data['c_num'] = 1

            return JsonResponse(data)
        data['code'] = 403
        data['msg'] = '请登录'
        return JsonResponse(data)


def sub_cart(request):
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        if user.id:
            user_carts = CartModel.objects.filter(user_id=user.id,
                                                  goods_id=goods_id).first()

            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                return JsonResponse(data)
            data['c_num'] = 0
            return JsonResponse(data)
        data['msg'] = '请登录'
        data['code'] = 403
        return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        user = request.user
        user_carts = CartModel.objects.filter(user_id=user.id)
        data = {
            'user_carts': user_carts
        }
        return render(request, 'cart/cart.html', data)


def change_select_status(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        cart = CartModel.objects.filter(id=cart_id).first()
        if cart.is_select :
            cart.is_select = 0
        else:
            cart.is_select = 1
        cart.save()

        data = {
            'code': 200,
            'msg': '请求成功',
            'is_select': cart.is_select
        }
        return JsonResponse(data)


def generate_order(request):
    if request.method == 'GET':
        user = request.user
        o_num = get_order_random_id()
        order = OrderModel.objects.create(user_id=user.id, o_num=o_num)
        user_carts = CartModel.objects.filter(user_id=user.id, is_select=True)
        for carts in user_carts:
            OrderGoodsModel.objects.create(goods=carts.goods, order=order, goods_num=carts.c_num)
        user_carts.delete()
        return render(request, 'order/order_info.html', {'order': order})


def change_order_status(request):

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        OrderModel.objects.filter(id=order_id).update(o_status=1)

        return JsonResponse({'code': 200, 'msg': '请求成功'})


def order_wait_pay(request):

    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user_id=user.id, o_status=0)

        return render(request, 'order/order_list_wait_pay.html', {'orders':orders})


def order_payed(request):
    if request.method == 'GET':
        user = request.user
        orders = OrderModel.objects.filter(user_id=user.id, o_status=1)

        return render(request, 'order/order_list_payed.html', {'orders': orders})


def wait_pay_to_payed(request):
    if request.method == 'GET':
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.filter(id=order_id).first()

        return render(request, 'order/order_info.html', {'order': order})




