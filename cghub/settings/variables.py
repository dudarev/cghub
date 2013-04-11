# also specified in search.js
LAST_QUERY_COOKIE = 'last_query'

# max_age should be a number of seconds, or None (default) if the cookie should last only as long as the client's browser session
# datetime.timedelta(days=365).total_seconds()
# 31536000.0
COOKIE_MAX_AGE = 31536000

# if user will try to add to cart more than specified number files,
# confirmation popup will be shown
MANY_FILES = 100
