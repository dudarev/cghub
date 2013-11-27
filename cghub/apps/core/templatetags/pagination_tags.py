from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from ..utils import paginator_params


register = template.Library()


class Paginator(object):

    def __init__(self, context):
        self.context = context
        self.num_results = context['num_results']
        self.offset, self.limit = paginator_params(context['request'])
        self.is_paginated = self.limit < self.num_results
        pages_count, partial_page = divmod(self.num_results, self.limit)
        self.pages_count = pages_count + (partial_page and 1 or 0)
        self.current_page = self.offset / self.limit + 1
        self.url_template = '{path}?{getvars}&offset={offset}&limit={limit}'
        # number of buttons to show prev and after current page
        self.paginator_buttons = getattr(settings, 'PAGINATOR_BUTTONS', 2)

    def get_path(self):
        request = self.context['request']
        # patch for the home page
        if request.path == reverse('home_page'):
            return reverse('search_page')
        return request.path

    def get_vars(self):
        request = self.context['request']
        get_copy = request.GET.copy()
        offset_limit = paginator_params(request)

        if 'limit' in get_copy:
            del get_copy['limit']
        if 'offset' in get_copy:
            del get_copy['offset']
        if len(get_copy.keys()) > 0:
            getvars = '{0}'.format(get_copy.urlencode())
        else:
            getvars = ''
        return getvars

    def _get_url(self, path, getvars, limit, offset):
        url = self.url_template.format(
                path=path, getvars=getvars,
                limit=limit, offset=offset)
        if '?&' in url:
            url = url.replace('?&', '?')
        return url

    def prev_button(self):
        return {
            'is_active': self.current_page > 1,
            'url': self._get_url(
                    path=self.get_path(), getvars=self.get_vars(),
                    limit=self.limit, offset=(self.offset - self.limit)),
        }

    def next_button(self):
        return {
            'is_active': self.current_page < self.pages_count,
            'url': self._get_url(
                    path=self.get_path(), getvars=self.get_vars(),
                    limit=self.limit, offset=(self.offset + self.limit)),
        }

    def buttons(self):
        p = []
        numbers = []
        # first page
        p.append({
            'is_active': True,
            'is_current': self.current_page == 1,
            'url': self._get_url(
                    path=self.get_path(), getvars=self.get_vars(),
                    limit=self.limit, offset=0),
            'n': 1,
        })
        numbers.append(1)
        # space
        if self.current_page > self.paginator_buttons + 2:
            p.append({
                'is_active': False,
                'is_current': False,
                'n': '...',
            })
        # prev nad next n pages
        for i in range(
                self.current_page - self.paginator_buttons,
                self.current_page + self.paginator_buttons + 1):
            if i < 1:
                continue
            if i > self.pages_count:
                continue
            if i in numbers:
                continue
            p.append({
                'is_active': True,
                'is_current': self.current_page == i,
                'url': self._get_url(
                        path=self.get_path(), getvars=self.get_vars(),
                        limit=self.limit, offset=(self.limit * (i - 1))),
                'n': i,
            })
            numbers.append(i)
        # space
        if self.current_page + self.paginator_buttons + 1 < self.pages_count:
            p.append({
                'is_active': False,
                'is_current': False,
                'n': '...',
            })
        # last page
        if self.pages_count not in numbers:
            p.append({
                'is_active': True,
                'is_current': self.current_page == self.pages_count,
                'url': self._get_url(
                        path=self.get_path(), getvars=self.get_vars(),
                        limit=self.limit, offset=(
                                self.limit * (self.pages_count - 1))),
                'n': self.pages_count,
            })
        return p


@register.inclusion_tag('pagination.html', takes_context=True)
def pagination(context):
    context['paginator'] = Paginator(context)
    return context


@register.simple_tag
def items_per_page(request, *limits):
    """
    Output is something like this:
    Items per page: 10 | 25 | 50 | 100
    """
    links = ''
    for limit in limits:
        # Checking for correct data have been passed
        if not str(limit).isdigit():
            raise Exception("Limits can be numbers or it's string representation")
        get = request.GET.copy()
        offset, old_limit = paginator_params(request)

        if old_limit == limit:
            link = '%d' % limit
        else:
            get['limit'] = str(limit)
            get['offset'] = str(int(offset / limit) * limit)
            path = request.path + '?' + get.urlencode()
            link = ('<a href="{link}"><span class="hidden">view </span>'
                    '{limit}<span class="hidden"> items per page</span></a>'.format(
                            link=path.replace('&', '&amp;'), limit=limit))
        links += '&nbsp;' + link + '&nbsp;|'

    return '<div class="items-per-page-label">Items per page:{0}</div>'.format(
        links[:-1])
