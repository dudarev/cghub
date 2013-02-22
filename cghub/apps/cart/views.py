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
from django.utils.http import urlquote

from cghub.apps.core.utils import (get_filters_string, is_celery_alive,
                                                    get_wsapi_settings)
from cghub.apps.cart.forms import SelectedFilesForm, AllFilesForm
from cghub.apps.cart.utils import (add_file_to_cart, remove_file_from_cart,
                    cache_results, get_or_create_cart, get_cart_stats)
from cghub.wsapi.api import request as api_request
from cghub.wsapi.api import multiple_request as api_multiple_request
from cghub.wsapi.api import Results


WSAPI_SETTINGS = get_wsapi_settings()


def cart_add_files(request):
    result = {'success': True, 'redirect': reverse('cart_page')}
    if not request.is_ajax():
        raise Http404
    filters = request.POST.get('filters')
    celery_alive = is_celery_alive()
    if filters:
        form = AllFilesForm(request.POST)
        if form.is_valid():
            attributes = form.cleaned_data['attributes']
            filters = form.cleaned_data['filters']
            filter_str = get_filters_string(filters)
            q = filters.get('q')
            if q:
                query = u"xml_text={0}".format(urlquote(q))
                query += filter_str
            else:
                query = filter_str[1:]  # remove front ampersand
            if 'xml_text' in query:
                queries_list = [query, query.replace('xml_text', 'analysis_id', 1)]
                results = api_multiple_request(queries_list=queries_list,
                                    settings=WSAPI_SETTINGS)
            else:
                results = api_request(query=query, settings=WSAPI_SETTINGS)
            results.add_custom_fields()
            if hasattr(results, 'Result'):
                for r in results.Result:
                    r_attrs = dict(
                        (attr, unicode(getattr(r, attr)))
                        for attr in attributes if hasattr(r, attr))
                    r_attrs['files_size'] = int(r.files_size)
                    r_attrs['analysis_id'] = unicode(r.analysis_id)
                    add_file_to_cart(request, r_attrs)
                    if celery_alive:
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
                if celery_alive:
                    cache_results(attributes[f])
        else:
            result = {'success': False}
    return HttpResponse(json.dumps(result), mimetype="application/json")


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
            return cart_add_files(request)
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
                return self.metadata(cart=cart, format=action.split('_')[1])
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
                result = Results.from_file(
                        os.path.join(settings.CART_CACHE_FOLDER, filename),
                        settings=WSAPI_SETTINGS)
            except IOError:
                result = api_request(
                    query='analysis_id={0}'.format(analysis_id),
                    get_attributes=get_attributes, settings=WSAPI_SETTINGS)
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
            csvwriter = self._write_manifest_csv(stringio=mfio, tree=tree, delimeter='\t')
            content_type = 'text/tsv'
            filename = 'manifest.tsv'
        mfio.seek(0)

        response = HttpResponse(basehttp.FileWrapper(mfio), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    def metadata(self, cart, format):
        mfio = StringIO()
        results = self.get_results(cart, get_attributes=True)

        if format == 'xml':
            mfio.write(results.tostring())
            content_type = 'text/xml'
            filename = 'metadata.xml'
        if format == 'tsv':
            parser = etree.XMLParser()
            tree = etree.XML(results.tostring(), parser)
            csvwriter = self._write_metadata_csv(stringio=mfio, tree=tree, delimeter='\t')
            content_type = 'text/tsv'
            filename = 'metadata.tsv'

        mfio.seek(0)
        response = HttpResponse(basehttp.FileWrapper(mfio), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response

    def _empty_results(self):
        from lxml import objectify
        from datetime import datetime
        results = Results(
                    objectify.fromstring('<ResultSet></ResultSet>'),
                    settings=WSAPI_SETTINGS)
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

    def _write_manifest_csv(self, stringio, tree, delimeter):
        csvwriter = csv.writer(stringio, delimiter=delimeter)
        # date
        csvwriter.writerow(tree.items()[0])
        csvwriter.writerow('')
        # Result
        result = tree.find("Result")
        csvwriter.writerow([result.keys()[0]]+
                           [r.tag for r in result.iterchildren()])
        for result in tree.iterfind("Result"):
            csvwriter.writerow([result.values()[0]]+
                               [r.text for r in result.iterchildren()])
        csvwriter.writerow('')
        # ResultSummary
        summary = tree.find("ResultSummary")
        if summary is not None:
            state_count = summary.find("state_count")
            csvwriter.writerow([s.tag for s in summary.iterchildren()
                                if s.tag != "summary_count"]+
                               [s.tag for s in state_count.iterchildren()])
            csvwriter.writerow([s.text for s in summary.iterchildren()
                                if s.tag != "summary_count"]+
                               [s.text for s in state_count.iterchildren()])
        return csvwriter

    def _write_metadata_csv(self, stringio, tree, delimeter):
        csvwriter = csv.writer(stringio, delimiter=delimeter)
        # date
        csvwriter.writerow(tree.items()[0])
        csvwriter.writerow('')

        # Result
        # complex tags not included in table of Result
        not_included_tags_set = set(['files', 'analysis_xml', 'experiment_xml', 'run_xml'])

        for result in tree.iterfind("Result"):
            csvwriter.writerow(["Result"])
            csvwriter.writerow(result.items()[0])
            # variant of a Result in table with 2 columns
            for r in result.iterchildren():
                if r.tag not in not_included_tags_set:
                    csvwriter.writerow([r.tag, r.text])

#           # variant of a Result in one row
#            csvwriter.writerow([result.keys()[0]]+
#                               [r.tag for r in result.iterchildren()
#                                if r.tag not in not_included_tags_set])
#            csvwriter.writerow([result.values()[0]]+
#                               [r.text for r in result.iterchildren()
#                                if r.tag not in not_included_tags_set])

            csvwriter.writerow('')
            # separate inner table for files in Result
            file = result.find('.//file')
            if file is not None:
                csvwriter.writerow([f.tag for f in file.iterchildren()]+[file.find('checksum').keys()[0]])
                for file in result.iterfind('.//file'):
                    csvwriter.writerow([f.text for f in file.iterchildren()]+[file.find('checksum').values()[0]])
                csvwriter.writerow('')
            # TODO here might be separate tables for 'analysis_xml', 'experiment_xml', 'run_xml' tags
            csvwriter.writerow('')

        # ResultSummary
        summary = tree.find("ResultSummary")
        if summary is not None:
            csvwriter.writerow(["ResultSummary"])
            state_count = summary.find("state_count")
            csvwriter.writerow([s.tag for s in summary.iterchildren()
                                if s.tag != "summary_count"]+
                               [s.tag for s in state_count.iterchildren()])
            csvwriter.writerow([s.text for s in summary.iterchildren()
                                if s.tag != "summary_count"]+
                               [s.text for s in state_count.iterchildren()])
        return csvwriter
