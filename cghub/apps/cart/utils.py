import sys

from cghub.apps.cart.tasks import cache_results_task


def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    request.session["cart"] = request.session.get('cart', {})
    return request.session["cart"]


def add_file_to_cart(request, file_dict):
    """ adds file file_dict to cart """
    cart = get_or_create_cart(request)
    analysis_id = file_dict.get('analysis_id')
    if analysis_id not in cart:
        cart[analysis_id] = file_dict
    request.session.modified = True


def remove_file_from_cart(request, analysis_id):
    """ removes file with legacy_sample_id from cart """
    cart = get_or_create_cart(request)
    if analysis_id in cart:
        del cart[analysis_id]
    request.session.modified = True


def get_cart_stats(request):
    cart = get_or_create_cart(request)
    stats = {'count': len(cart), 'size': 0}
    for analysis_id, f in cart.iteritems():
        if 'files_size' in f and isinstance(f['files_size'], (int, long)):
            stats['size'] += f['files_size']
    return stats


def clear_cart(request):
    request.session.get('cart').clear()
    request.session.modified = True


def cache_results(file_dict):
    """
    To check celery status use cghub.apps.core.utils.py:is_celery_alive
    """
    try:
        cache_results_task.delay(file_dict)
    except:
        cache_results_task(file_dict)
