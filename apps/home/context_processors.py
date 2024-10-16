from .models import CartItem

def cart_items_counter(request):
    cart_items_count = 0
    if request.session.session_key:
        cart_items_count = CartItem.objects.filter(session_key=request.session.session_key).count()
    return {'cart_items_count': cart_items_count}