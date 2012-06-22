from lxml import etree
from django.conf import settings
import os
from cghub.cghub_api import api
from cghub.cghub_api.api import request as api_request

def get_or_create_cart(request):
    """ return cart and creates it if it does not exist """
    try:
        request.session["cart"]
    except KeyError:
        request.session["cart"] = []
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
    analysis_id = file_dict.get('analysis_id')
    filename_with_attributes = os.path.join(settings.API_RESULTS_CACHE_FOLDER,
        "{0}_with_attributes".format(analysis_id))
    filename_without_attributes = os.path.join(settings.API_RESULTS_CACHE_FOLDER,
        "{0}_without_attributes".format(analysis_id))
    result = api_request(query='analysis_id={0}'.format(analysis_id))
    with open(filename_with_attributes, 'w') as f:
        f.write(etree.tostring(result))
    with open(filename_without_attributes, 'w') as f:
        result.Result.remove(result.Result.find('sample_accession'))
        result.Result.remove(result.Result.find('legacy_sample_id'))
        result.Result.remove(result.Result.find('disease_abbr'))
        result.Result.remove(result.Result.find('tss_id'))
        result.Result.remove(result.Result.find('participant_id'))
        result.Result.remove(result.Result.find('sample_id'))
        result.Result.remove(result.Result.find('analyte_code'))
        result.Result.remove(result.Result.find('sample_type'))
        result.Result.remove(result.Result.find('library_strategy'))
        result.Result.remove(result.Result.find('platform'))
        result.Result.remove(result.Result.find('analysis_xml'))
        result.Result.remove(result.Result.find('run_xml'))
        result.Result.remove(result.Result.find('experiment_xml'))
        analysis_attribute_uri = etree.Element('analysis_attribute_uri')
        analysis_attribute_uri.text = api.CGHUB_SERVER + api.CGHUB_ANALYSIS_ATTRIBUTES_URI + '/' + analysis_id
        result.Result.append(analysis_attribute_uri)
        f.write(etree.tostring(result))
