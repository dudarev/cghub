from cghub.apps.cart.tasks import cache_results_task

def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    request.session["cart"] = request.session.get('cart', {})
    return request.session["cart"]


def add_file_to_cart(request, file_dict):
    """ adds file file_dict to cart """
    cart = get_or_create_cart(request)
    if file_dict not in cart:
        cart.append(file_dict)
    request.session.modified = True


def remove_file_from_cart(request, legacy_sample_id):
    """ removes file with legacy_sample_id from cart """
    cart = get_or_create_cart(request)
    for i, file_dict in enumerate(cart):
        if file_dict['legacy_sample_id'] == legacy_sample_id:
            del(cart[i])
            break
    request.session.modified = True


def get_cart_stats(request):
    cart = get_or_create_cart(request)
    stats = {'count': len(cart), 'size': 0}
    for f in cart:
        if 'filesize' in f and int == type(f['filesize']):
            stats['size'] += int(f['filesize'] / 1024.0 / 1024.0)
    return stats


def cache_results(file_dict):
    cache_results_task.delay(file_dict)
