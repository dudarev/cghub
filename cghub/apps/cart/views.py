import logging

from urllib2 import URLError

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.utils import DatabaseError
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.base import TemplateView, View

from cghub.apps.core import browser_text_search
from cghub.apps.core.forms import AnalysisIDsForm
from cghub.apps.core.requests import (
        RequestMinimal, RequestDetailJSON, get_results_for_ids)
from cghub.apps.core.utils import (
        get_filters_dict, paginator_params, add_message,
        remove_message)

from .forms import SelectedItemsForm, AllItemsForm
from .utils import (
        Cart, manifest_xml_generator, metadata_xml_generator,
        summary_tsv_generator)


cart_logger = logging.getLogger('cart')


def cart_add_selected_files(request):
    form = SelectedItemsForm(request.POST)
    if form.is_valid():
        try:
            message_id = add_message(
                        request, 'info',
                        settings.ADDING_TO_CART_IN_PROGRESS_NOTIFICATION)
            try:
                with transaction.commit_on_success():
                    cart = Cart(request.session)
                    for result in form.cleaned_data['selected_items']:
                        cart.add(result)
                    cart.update_stats()
                remove_message(request=request, message_id=message_id)
            except DatabaseError:
                remove_message(request=request, message_id=message_id)
                return {
                    'action': 'message',
                    'title': settings.DATABASE_ERROR_NOTIFICATION_TITLE,
                    'content': settings.DATABASE_ERROR_NOTIFICATION}
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding to cart: %s' % unicode(e))
    else:
        cart_logger.error('SelectedItemsForm not valid: %s' % unicode(form.errors))


def cart_add_all_files(request):
    # 'Add all to cart' pressed
    form = AllItemsForm(request.POST)
    if form.is_valid():
        try:
            # calculate query
            raw_filters = form.cleaned_data['filters']
            filters = get_filters_dict(raw_filters)
            q = raw_filters.get('q')
            queries = []
            if q:
                # FIXME: temporary hack to work around GNOS not quoting Solr query
                # FIXME: this is temporary hack, need for multiple requests will be fixed at CGHub
                if browser_text_search.useAllMetadataIndex:
                    query = {'all_metadata': browser_text_search.ws_query(q)}
                    query.update(filters)
                    queries = [query]
                else:
                    query = {'xml_text': u"(%s)" % q}
                    query.update(filters)
                    queries = [query, {'analysis_id': q}]
            if not queries:
                queries = [filters]

            message_id = add_message(
                        request, 'info',
                        settings.ADDING_TO_CART_IN_PROGRESS_NOTIFICATION)
            try:
                with transaction.commit_on_success():
                    cart = Cart(request.session)
                    for query in queries:
                        api_request = RequestMinimal(query=query)
                        for result in api_request.call():
                            cart.add(result)
                        cart.update_stats()
                remove_message(request, message_id)
            except DatabaseError:
                remove_message(request, message_id)
                return {
                    'action': 'message',
                    'title': settings.DATABASE_ERROR_NOTIFICATION_TITLE,
                    'content': settings.DATABASE_ERROR_NOTIFICATION}
            return {'action': 'redirect', 'redirect': reverse('cart_page')}
        except Exception as e:
            cart_logger.error('Error while adding all files to cart: %s' % unicode(e))
    else:
        cart_logger.error('AllItemsForm not valid: %s' % unicode(form.errors))


def cart_add_files(request):
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    if filters:
        result = cart_add_all_files(request)
    else:
        result = cart_add_selected_files(request)
    result = result or {'action': 'error'}
    return HttpResponse(json.dumps(result), mimetype="application/json")


class CartView(TemplateView):
    """
    Lists files in cart
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request.session)
        sort_by = self.request.GET.get('sort_by')
        offset, limit = paginator_params(self.request)
        # will be saved to cookie in get method
        self.paginator_limit = limit
        return {
            'results': cart.page(offset=offset, limit=limit, sort_by=sort_by),
            'num_results': cart.all_count,
            'size': cart.size}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        if request.GET and response.status_code == 200:
            response.set_cookie(settings.PAGINATOR_LIMIT_COOKIE,
                    self.paginator_limit,
                    max_age=settings.COOKIE_MAX_AGE,
                    path=reverse('home_page'))
        return response


class CartAddRemoveItemsView(View):
    """
    Handles files added to cart
    """

    http_method_names = ['post']

    def post(self, request, action):
        if 'add' == action:
            return cart_add_files(request)
        if 'remove' == action:
            form = AnalysisIDsForm(request.POST or None)
            if form.is_valid():
                try:
                    with transaction.commit_on_success():
                        cart = Cart(request.session)
                        for analysis_id in form.cleaned_data['ids']:
                            cart.remove(analysis_id)
                        cart.update_stats()
                except DatabaseError:
                    add_message(
                            request, 'error',
                            settings.DATABASE_ERROR_NOTIFICATION,
                            once=True)
        return HttpResponseRedirect(reverse('cart_page'))


class CartAddItem(View):

    http_method_names = ['post']

    def post(self, request, analysis_id):
        api_request = RequestDetailJSON(query={'analysis_id': analysis_id})
        try:
            result = api_request.call().next()
        except StopIteration:
            raise URLError('No results for analysis_id == %s' % analysis_id)
        try:
            with transaction.commit_on_success():
                cart = Cart(request.session)
                cart.add(result)
                cart.update_stats()
        except DatabaseError:
            add_message(
                    request, 'error',
                    settings.DATABASE_ERROR_NOTIFICATION,
                    once=True)
        return HttpResponseRedirect(reverse('cart_page'))


class CartClearView(View):
    """
    Handels clearing cart
    """
    def post(self, request):
        try:
            with transaction.commit_on_success():
                cart = Cart(request.session)
                cart.clear()
        except DatabaseError:
            add_message(
                    request, 'error', 
                    settings.DATABASE_ERROR_NOTIFICATION, once=True)
        return HttpResponseRedirect(reverse('cart_page'))


def manifest(request):
    if request.GET.get('gzip'):
        response = HttpResponse(
                manifest_xml_generator(request, compress=True),
                content_type='application/x-gzip')
        response['Content-Disposition'] = 'attachment; filename=manifest.xml.gz'
    else:
        response = HttpResponse(
                manifest_xml_generator(request),
                content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=manifest.xml'
    return response


def metadata(request):
    if request.GET.get('gzip'):
        response = HttpResponse(
                metadata_xml_generator(request, compress=True),
                content_type='application/x-gzip')
        response['Content-Disposition'] = 'attachment; filename=metadata.xml.gz'
    else:
        response = HttpResponse(
            metadata_xml_generator(request), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response


def summary(request):
    if request.GET.get('gzip'):
        response = HttpResponse(
                summary_tsv_generator(request, compress=True),
                content_type='application/x-gzip')
        response['Content-Disposition'] = 'attachment; filename=summary.tsv.gz'
    else:
        response = HttpResponse(
                summary_tsv_generator(request),
                content_type='text/tsv')
        response['Content-Disposition'] = 'attachment; filename=summary.tsv'
    return response


DOWNLOAD_VIEWS = {
    'manifest': manifest,
    'metadata': metadata,
    'summary': summary,
}


class CartDownloadFilesView(View):
    def post(self, request, action):
        if action:
            download = DOWNLOAD_VIEWS.get(action, DOWNLOAD_VIEWS['manifest'])
            return download(request)
        return HttpResponseRedirect(reverse('cart_page'))
