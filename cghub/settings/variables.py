import datetime

# also specified in search.js
LAST_QUERY_COOKIE = 'last_query'

# max_age should be a number of seconds, or None (default) if the cookie should last only as long as the client's browser session
COOKIE_MAX_AGE = datetime.timedelta(days=365).total_seconds()
