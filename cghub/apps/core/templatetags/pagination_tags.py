from django import template
from django.conf import settings


register = template.Library()


class Paginator(object):
    def __init__(self, context):
        # context
        self.context = context

        # num_results
        self.num_results = self.context['num_results']
        request = context['request']

        # limit
        limit = request.GET.get('limit')
        if limit and limit.isdigit():
            self.limit = int(limit)
        else:
            self.limit = settings.DEFAULT_PAGINATOR_LIMIT

        # offset
        offset = request.GET.get('offset')
        if offset and offset.isdigit():
            self.offset = int(offset)
        else:
            self.offset = 0

        # is_paginated
        self.is_paginated = self.limit or self.offset

        # pages count
        pages_count, partial_page = divmod(self.num_results,
            self.limit or self.num_results)
        self.pages_count = pages_count + (partial_page and 1 or 0)

        # url tempalte
        self.url_template = '{path}?{getvars}&offset={offset}&limit={limit}'

    def get_path(self):
        request = self.context['request']
        # patch for the home page were all paginator 
        # links should refer to search page
        if request.path == u'/':
            return u'/search/'
        return request.path

    def get_vars(self):
        request = self.context['request']
        get_copy = request.GET.copy()
        if 'limit' in get_copy:
            del get_copy['limit']
        if 'offset' in get_copy:
            del get_copy['offset']

        if len(get_copy.keys()) > 0:
            getvars = '{0}'.format(get_copy.urlencode())
        else:
            getvars = ''
        # patch for the home page where sort_by=-last_modified 
        # is enabled and should remain
        # on other paginated pages
        if request.path == u'/':
            getvars += '&sort_by=-last_modified'
        return getvars

    def current_page(self):
        return {
            'url': self._get_url(path=self.get_path(), getvars=self.get_vars(),
                                 limit=self.limit, offset=self.offset),
            'page_number': self.offset / self.limit,
            }

    def next_page(self):
        return {
            'url': self._get_url(path=self.get_path(), getvars=self.get_vars(),
                                 limit=self.limit, offset=(self.offset + self.limit)),
            'page_number': self.offset / self.limit + 1
        }

    def prev_page(self):
        return {
            'url': self._get_url(path=self.get_path(), getvars=self.get_vars(),
                                 limit=self.limit, offset=(self.offset - self.limit)),
            'page_number': self.offset / self.limit - 1
        }

    def pages(self):
        ps = []
        for page_number in xrange(self.pages_count):
            ps.append({
                'url': self._get_url(path=self.get_path(),
                    getvars=self.get_vars(), limit=self.limit,
                    offset=page_number * self.limit),
                'page_number': page_number,
                })
        return ps

    def get_first(self):
        return {
            'url': self._get_url(path=self.get_path(), getvars=self.get_vars(),
                                 limit=self.limit, offset=0),
            'page_number': 0
        }

    def get_last(self):
        return {
            'url': self._get_url(path=self.get_path(), getvars=self.get_vars(),
                limit=self.limit, offset=(self.pages_count - 1) * self.limit),
            'page_number': self.pages_count - 1
        }

    def has_prev(self):
        return self.offset > 0

    def has_next(self):
        return (self.num_results - self.offset) > self.limit

    def _get_url(self, path, getvars, limit, offset):
        url = self.url_template.format(path=path, getvars=getvars,
            limit=limit, offset=offset)
        if '?&' in url:
            url = url.replace('?&', '?')
        return url


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
        old_limit = get.get('limit', None)

        if ((not old_limit and limit == settings.DEFAULT_PAGINATOR_LIMIT) or
            old_limit == str(limit)):
            link = '%d' % limit
        else:
            get['limit'] = str(limit)
            path = request.path + '?' + get.urlencode()
            link = '<a href="%s">%d</a>' % (path.replace('&', '&amp;'), limit)
        links += '&nbsp;' + link + '&nbsp;|'

    return '<div class="items-per-page-label">Items per page:{0}</div>'.format(
        links[:-1])
