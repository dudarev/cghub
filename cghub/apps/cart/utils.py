import sys
import socket
import traceback

from django.core.mail import mail_admins

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


def cache_results(file_dict):

    try:
        if 'test' in sys.argv:
            from celery import Celery
            from django.conf import settings
            Celery(broker=settings.BROKER_URL).connection().connect()
        cache_results_task.delay(file_dict)
    except socket.error, v:
        subject = '[ucsc-cghub] ERROR: Message broker not working'
        message = traceback.format_exc()
        mail_admins(subject, message, fail_silently=True)
        # cache_results_task(file_dict)
    
