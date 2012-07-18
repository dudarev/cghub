import glob
import os
import random
import sys
from profiler import profile
from cghub_api.api import request as api_request
from cghub_api.settings import CACHE_DIR


def perform_queries_for(queries, stats_filename):
    api_request_in_profiler = profile(api_request, stats_filename)
    for q in queries:
        print("\tquery={0}".format(q))
        api_request_in_profiler(q)


def perform_profiling(queries_count):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    files = glob.glob(os.path.join(CACHE_DIR, '*'))
    for file in files:
        os.remove(file)

    three_pos_queries = ('xml_text={0:3x}*'.format(random.randrange(0, 0xfff)) for d in xrange(queries_count))
    four_pos_queries = ('xml_text={0:4x}*'.format(random.randrange(0, 0xffff)) for d in xrange(queries_count))

    print("Perform 3 pos queries without cache:")
    perform_queries_for(three_pos_queries, 'three_pos_queries_without_cache.stats')

    print("Perform 4 pos queries without cache:")
    perform_queries_for(four_pos_queries, 'four_pos_queries_without_cache.stats')

    print("Perform 3 pos queries with cache:")
    perform_queries_for(three_pos_queries, 'three_pos_queries_with_cache.stats')

    print("Perform 4 pos queries with cache:")
    perform_queries_for(four_pos_queries, 'four_pos_queries_with_cache.stats')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            queries_count = int(sys.argv[1])
            perform_profiling(queries_count)
        else:
            print("Queries count is not a number!")
    else:
        print("Queries count isn't specified!")
