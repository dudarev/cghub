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
        getvars = request.GET.copy()
        if 'limit' in getvars:
            del getvars['limit']
        if 'offset' in getvars:
            del getvars['offset']

        # pages count
        pages_count, partial_page = divmod(self.num_results, self.limit or self.num_results)
        self.pages_count = pages_count + (partial_page and 1 or 0)


        # getvars
        if len(getvars.keys()) > 0:
            self.getvars = '{0}'.format(getvars.urlencode())
        else:
            self.getvars = ''

        # url tempalte
        self.url_template = '{path}?{getvars}&offset={offset}&limit={limit}'

    def get_path(self):
        request = self.context['request']
        # patch for the home page were all paginator links should refer to search page
        if request.path == u'/':
            return u'/search/'
        return request.path

    def current_page(self):
        return {
            'url': self.url_template.format(
                path=self.get_path(), getvars=self.getvars, limit=self.limit, offset=self.offset),
            'page_number': self.offset / self.limit,
            }

    def next_page(self):
        return {
            'url': self.url_template.format(
                path=self.get_path(), getvars=self.getvars, limit=self.limit, offset=self.offset + self.limit),
            'page_number': self.offset / self.limit + 1
        }

    def prev_page(self):
        return {
            'url': self.url_template.format(
                path=self.get_path(), getvars=self.getvars, limit=self.limit, offset=self.offset - self.limit),
            'page_number': self.offset / self.limit - 1
        }

    def pages(self):
        ps = []
        for page_number in xrange(self.pages_count):
            ps.append({
                'url': self.url_template.format(
                    path=self.get_path(), getvars=self.getvars, limit=self.limit, offset=page_number * self.limit),
                'page_number': page_number,
                })
        return ps

    def has_prev(self):
        return self.offset > 0

    def has_next(self):
        return (self.num_results - self.offset) > self.limit


@register.inclusion_tag('pagination.html', takes_context=True)
def pagination(context):
    context['paginator'] = Paginator(context)
    return context
