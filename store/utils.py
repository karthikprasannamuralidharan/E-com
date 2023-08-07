import json
from .models import *


# created a function which can be used in views.py file and it will reduce the overlapping of copy paste

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #empty cart for non-logged
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']


    return {'cartItems':cartItems, 'order':order, 'items':items}


