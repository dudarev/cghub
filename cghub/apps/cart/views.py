import os
from StringIO import StringIO
from operator import itemgetter
from lxml import etree
import csv

from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.core.servers import basehttp
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import simplejson as json

from cghub.apps.core.utils import get_filters_string
from cghub.apps.core.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                    cache_results, get_or_create_cart, get_cart_stats)
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import Results


class CartView(TemplateView):
    """
    Lists files in cart
    """
    template_name = 'cart/cart.html'

    def get_context_data(self, **kwargs):
        sort_by = self.request.GET.get('sort_by')
        cart = get_or_create_cart(self.request).values()
        if sort_by:
            item = sort_by[1:] if sort_by[0] == '-' else sort_by
            cart = sorted(cart, key=itemgetter(item), reverse=sort_by[0] == '-')
        stats = get_cart_stats(self.request)
        offset = self.request.GET.get('offset')
        offset = offset and offset.isdigit() and int(offset) or 0
        limit = self.request.GET.get('limit')
        limit = limit and limit.isdigit() and int(limit) or settings.DEFAULT_PAGINATOR_LIMIT
        return {
            'results': cart[offset:offset + limit],
            'stats': stats,
            'num_results': stats['count']}


class CartAddRemoveFilesView(View):
    """
    Handles files added to cart
    """
    def post(self, request, action):
        if 'add' == action:
            result = {'success': True, 'redirect': reverse('cart_page')}
            if not request.is_ajax():
                raise Http404
            filters = request.POST.get('filters')
            if filters:
                form = AllFilesForm(request.POST)
                if form.is_valid():
                    attributes = form.cleaned_data['attributes']
                    filters = form.cleaned_data['filters']
                    query = get_filters_string(filters)[1:]
                    results = api_request(query=query)
                    results.add_custom_fields()
                    if hasattr(results, 'Result'):
                        for r in results.Result:
                            r_attrs = dict(
                                (attr, unicode(getattr(r, attr)))
                                for attr in attributes if hasattr(r, attr))
                            r_attrs['files_size'] = int(r.files_size)
                            r_attrs['analysis_id'] = unicode(r.analysis_id)
                            add_file_to_cart(request, r_attrs)
                            cache_results(r_attrs)
                else:
                    result = {'success': False}
            else:
                form = SelectedFilesForm(request.POST)
                if form.is_valid():
                    attributes = form.cleaned_data['attributes']
                    selected_files = request.POST.getlist('selected_files')
                    for f in selected_files:
                        add_file_to_cart(request, attributes[f])
                        cache_results(attributes[f])
                else:
                    result = {'success': False}
            return HttpResponse(
                json.dumps(result),
                mimetype="application/json")
        if 'remove' == action:
            for f in request.POST.getlist('selected_files'):
                # remove file from cart by sample id
                remove_file_from_cart(request, f)
            params = request.META.get('HTTP_REFERER', '')
            url = reverse('cart_page')
            if params.find('/?') != -1:
                url += params[params.find('/?') + 1:len(params)]
            return HttpResponseRedirect(url)

    def get(self, request, action):
        raise Http404


class CartDownloadFilesView(View):
    def post(self, request, action):
        cart = request.session.get('cart')
        if cart and action:
            if action.startswith('manifest'):
                return self.manifest(cart=cart, format=action.split('_')[1])
            if action.startswith('metadata'):
                return self.metadata(cart=cart)
        return HttpResponseRedirect(reverse('cart_page'))

    @staticmethod
    def get_results(cart, get_attributes=False, live_only=False):
        results = None
        results_counter = 1
        for analysis_id in cart:
            if live_only and cart[analysis_id].get('state') != 'live':
                continue
            filename = "{0}_with{1}_attributes".format(
                analysis_id,
                '' if get_attributes else 'out')
            try:
                result = Results.from_file(os.path.join(settings.CART_CACHE_FOLDER, filename))
            except IOError:
                result = api_request(
                    query='analysis_id={0}'.format(analysis_id),
                    get_attributes=get_attributes)
            if results is None:
                results = result
                results.Query.clear()
                results.Hits.clear()
            else:
                result.Result.set('id', u'{0}'.format(results_counter))
                # '+ 1' because the first two elements (0th and 1st) are Query and Hits
                results.insert(results_counter + 1, result.Result)
            results_counter += 1

        return results

    def manifest(self, cart, format):
        results = self.get_results(cart, live_only=True)
        if not results:
            results= self._empty_results()

        mfio = StringIO()
        if format == 'xml':
            mfio.write(results.tostring())
            content_type = 'text/xml'
            filename = 'manifest.xml'
        if format == 'tsv':
            parser = etree.XMLParser()
            tree = etree.XML(results.tostring(), parser)
            csvwriter = self._write_csv(stringio=mfio, tree=tree, delimeter='\t')
            content_type = 'text/tsv'
            filename = 'manifest.tsv'
        mfio.seek(0)

        response = HttpResponse(basehttp.FileWrapper(mfio), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    def metadata(self, cart):
        mfio = StringIO()
        results = self.get_results(cart, get_attributes=True)
        mfio.write(results.tostring())
        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename=metadata.xml'
        return response

    def _empty_results(self):
        from lxml import objectify
        from datetime import datetime
        results = Results(objectify.fromstring('<ResultSet></ResultSet>'))
        results.set('date', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        results.insert(0, objectify.fromstring('<Query></Query>'))
        results.insert(1, objectify.fromstring('<Hits></Hits>'))
        results.insert(2, objectify.fromstring(
            '<ResultSummary>'
            '<downloadable_file_count>0</downloadable_file_count>'
            '<downloadable_file_size units="GB">0</downloadable_file_size>'
            '<state_count>'
            '<live>0</live>'
            '</state_count>'
            '</ResultSummary>'))
        return results

    def _write_csv(self, stringio, tree, delimeter):
        csvwriter = csv.writer(stringio, delimiter=delimeter)
        # date
        csvwriter.writerow(tree.items()[0])
        csvwriter.writerow('')
        # Result
        if tree.getchildren()[2].tag == 'Result':
            res = tree.getchildren()[2]
            csvwriter.writerow([res.keys()[0]]+[c.tag for c in res.getchildren()])
        for res in tree.getchildren()[2:]:
            if res.tag == 'Result':
                csvwriter.writerow([res.values()[0]]+[c.text for c in res.getchildren()])
        csvwriter.writerow('')
        # ResultSummary
        if tree.getchildren()[-1].tag == 'ResultSummary':
            summary = tree.getchildren()[-1]
            csvwriter.writerow([s.tag for s in summary.getchildren()[:-1]]+[summary.getchildren()[-1].getchildren()[0].tag])
            csvwriter.writerow([s.text for s in summary.getchildren()[:-1]]+[summary.getchildren()[-1].getchildren()[0].text])
        return csvwriter
