import sys

from cghub.apps.cart.tasks import cache_results_task
from cghub.apps.core.utils import get_wsapi_settings


WSAPI_SETTINGS = get_wsapi_settings()


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
    if 'cart' in request.session:
        request.session['cart'].clear()
        request.session.modified = True


def cache_results(file_dict):
    """
    To check celery status use cghub.apps.core.utils.py:is_celery_alive
    """
    try:
        cache_results_task.delay(file_dict)
    except:
        cache_results_task(file_dict)


def save_metadata_full(analysis_id, modification_time):
    """
    Save file to {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisFull.xml
    and cutted version saves to
    {CACHE_ROOT}/{analysis_id}/{modification_time}/analysisShort.xml
    """
    path = settings.CART_CACHE_DIR
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, analysis_id)
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, modification_time)
    if not os.path.isdir(path):
        os.makedirs(path)
    path_full = os.path.join(path, 'analysisFull.xml')
    path_short = os.path.join(path, 'analysisShort.xml')
    if not (os.path.exists(path_full) and os.path.exists(path_short)):
        result = api_request(
                query='analysis_id={0}'.format(analysis_id),
                settings=WSAPI_SETTINGS)
        with open(path_full, 'w') as f:
            f.write(result.tostring())
        with open(path_short, 'w') as f:
            result.remove_attributes()
            f.write(result.tostring())
