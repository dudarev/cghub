# also specified in search.js
LAST_QUERY_COOKIE = 'last_query'

# remember filters flag, keep synchronized with search.js
REMEMBER_FILTERS_COOKIE = 'remember_filters'

# paginator limit cookie name
PAGINATOR_LIMIT_COOKIE = 'paginator_limit'

# list of allowed items count per page
PAGINATOR_LIMITS = [15, 25, 50]

# max_age should be a number of seconds, or None (default) if the cookie should last only as long as the client's browser session
# datetime.timedelta(days=365).total_seconds()
# 31536000.0
COOKIE_MAX_AGE = 31536000

# if user will try to add to cart more than specified number of files,
# confirmation popup will be shown
MANY_FILES = 100

# max amount of ids can be placed in one query
# analysis_id=(00007994-abeb-4b16-a6ad-7230300a29e9 or 1003468a-e3a2-4a01-a045-62d53af7cdf2 or ...)
MAX_ITEMS_IN_QUERY = 80

# shows after ... Please contact admin:
SUPPORT_EMAIL = 'support@cghub.ucsc.edu'

# time, after which tooltip will be shown, in ms
TOOLTIP_HOVER_TIME = 250

# regexp for aliquot_id, analysis_id, participant_id, sample_id
ID_PATTERN = '^[0-9abcdef]{8}-[0-9abcdef]{4}-[0-9abcdef]{4}-[0-9abcdef]{4}-[0-9abcdef]{12}$'

# notifications
DATABASE_ERROR_NOTIFICATION = (
        'Your previous add to cart is still in progress, '
        'please try again in a few minutes.')
DATABASE_ERROR_NOTIFICATION_TITLE = (
        'Please try again in a few minutes')
ADDING_TO_CART_IN_PROGRESS_NOTIFICATION = (
        'Adding to cart is still in progress ...')