

def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    try:
        request.session["cart"]
    except KeyError:
        request.session["cart"] = []
    return request.session["cart"]

def add_file_to_cart(request, f):
    """ adds file f to cart """
    cart = get_or_create_cart(request)
    if f not in cart:
        cart.append(f)
    request.session.modified = True

def remove_file_from_cart(request, f):
    """ removes file f from cart """
    cart = get_or_create_cart(request)
    if f in cart:
        cart.remove(f)
    request.session.modified = True

def get_cart_stats(request):
    cart = get_or_create_cart(request)
    return {'count': len(cart)}
