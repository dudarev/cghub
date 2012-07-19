import csv
import glob
import random
import os
import sys
from profiler import profile
import time
from cghub_api.api import request as api_request
from cghub_api.settings import CACHE_DIR


STATS_DIR = 'cghub_api/utils/profile/stats'

good_three_pos_queries = (
    'xml_text=e79*', 'xml_text=bab*', 'xml_text=34d*', 'xml_text=afb*', 'xml_text=01f*', 'xml_text=4a7*',
    'xml_text=1b2*', 'xml_text=07c*', 'xml_text=5cd*', 'xml_text=e8c*', 'xml_text=f0f*', 'xml_text=8f6*',
    'xml_text=f5a*', 'xml_text=8bf*', 'xml_text=ecc*', 'xml_text=151*', 'xml_text=238*', 'xml_text=98f*',
    'xml_text=51d*', 'xml_text=723*', 'xml_text=a69*', 'xml_text=9a7*', 'xml_text=253*', 'xml_text=a50*',
    'xml_text=92b*', 'xml_text=c36*', 'xml_text=451*', 'xml_text=8cc*', 'xml_text=7c0*', 'xml_text=9b1*',
    'xml_text=fca*', 'xml_text=2d7*', 'xml_text=62c*', 'xml_text=794*', 'xml_text=d09*', 'xml_text=afe*',
    'xml_text=383*', 'xml_text=bfc*', 'xml_text=5f4*', 'xml_text=66d*', 'xml_text=4ab*', 'xml_text=8d7*',
    'xml_text=d5b*', 'xml_text=0f5*', 'xml_text=cc5*', 'xml_text=830*', 'xml_text=779*', 'xml_text=d56*',
    'xml_text=0d6*', 'xml_text=b85*', 'xml_text=b95*', 'xml_text=b22*', 'xml_text=a68*', 'xml_text=a21*',
    'xml_text=79a*', 'xml_text=9b6*', 'xml_text=292*', 'xml_text=903*', 'xml_text=265*', 'xml_text=71c*',
    'xml_text=5ac*', 'xml_text=8ad*', 'xml_text=2af*', 'xml_text=a0f*', 'xml_text=818*', 'xml_text=aca*',
    'xml_text=0b7*', 'xml_text=5d9*', 'xml_text=1ca*', 'xml_text=a79*', 'xml_text=bbd*', 'xml_text=9d5*',
    'xml_text=756*', 'xml_text=f25*', 'xml_text=4dd*', 'xml_text=11b*', 'xml_text=75c*', 'xml_text=a8a*',
    'xml_text=f9f*', 'xml_text=978*', 'xml_text=5da*', 'xml_text=757*', 'xml_text=b55*', 'xml_text=c16*',
    'xml_text=812*', 'xml_text=ccf*', 'xml_text=99a*', 'xml_text=8b2*', 'xml_text=6f0*', 'xml_text=5b6*',
    'xml_text=22c*', 'xml_text=831*', 'xml_text=130*', 'xml_text=b6a*', 'xml_text=814*', 'xml_text=e7b*',
    'xml_text=1a7*', 'xml_text=f14*', 'xml_text=7a8*', 'xml_text=18f*',
    )
good_four_pos_queries = (
    'xml_text=f144*', 'xml_text=e187*', 'xml_text=b17d*', 'xml_text=11c1*', 'xml_text=5c4b*', 'xml_text=86eb*',
    'xml_text=4d00*', 'xml_text=bfda*', 'xml_text=d308*', 'xml_text=68fb*', 'xml_text=cbef*', 'xml_text=a9d4*',
    'xml_text=1652*', 'xml_text=c892*', 'xml_text=976a*', 'xml_text=ea35*', 'xml_text=d70f*', 'xml_text=9eed*',
    'xml_text=97bf*', 'xml_text=50fe*', 'xml_text=f13d*', 'xml_text=e1bb*', 'xml_text=292a*', 'xml_text=815c*',
    'xml_text=75bc*', 'xml_text=891f*', 'xml_text=c643*', 'xml_text=272b*', 'xml_text=1a9f*', 'xml_text=c4c4*',
    'xml_text=002f*', 'xml_text=2f2b*', 'xml_text=05dd*', 'xml_text=eff5*', 'xml_text=cdce*', 'xml_text=9e7b*',
    'xml_text=6347*', 'xml_text=9fd5*', 'xml_text=402c*', 'xml_text=5d61*', 'xml_text=1d9b*', 'xml_text=3b0c*',
    'xml_text=3373*', 'xml_text=f30a*', 'xml_text=2ed3*', 'xml_text=4768*', 'xml_text=10e2*', 'xml_text=4137*',
    'xml_text=75b4*', 'xml_text=0f79*', 'xml_text=9a46*', 'xml_text=f749*', 'xml_text=8100*', 'xml_text=a468*',
    'xml_text=b39a*', 'xml_text=8136*', 'xml_text=8fd8*', 'xml_text=451a*', 'xml_text=6c8b*', 'xml_text=8356*',
    'xml_text=e4bd*', 'xml_text=544c*', 'xml_text=7645*', 'xml_text=8373*', 'xml_text=26ee*', 'xml_text=13b9*',
    'xml_text=3355*', 'xml_text=586d*', 'xml_text=51c4*', 'xml_text=fb4f*', 'xml_text=cd39*', 'xml_text=c0d6*',
    'xml_text=7047*', 'xml_text=df42*', 'xml_text=7a22*', 'xml_text=4ac8*', 'xml_text=fc1d*', 'xml_text=6a74*',
    'xml_text=2cc4*', 'xml_text=0a3b*', 'xml_text=65a6*', 'xml_text=a8b3*', 'xml_text=49e5*', 'xml_text=92ef*',
    'xml_text=56ce*', 'xml_text=e4a9*', 'xml_text=93bd*', 'xml_text=225a*', 'xml_text=f411*', 'xml_text=13a7*',
    'xml_text=d6f2*', 'xml_text=b564*', 'xml_text=19a9*', 'xml_text=6123*', 'xml_text=c303*', 'xml_text=2d80*',
    'xml_text=7751*', 'xml_text=2762*', 'xml_text=0361*', 'xml_text=1bc9*'
    )


def perform_queries_for(queries, filename):
    path_to_file = os.path.join(STATS_DIR, filename)
    api_request_in_profiler = profile(api_request, path_to_file + '.stats')
    with open(path_to_file + '.csv', 'wb') as f:
        statistics = csv.writer(f)
        statistics.writerow(['query', 'results count', 'time'])
        for q in queries:
            print("\t{0}".format(q))
            start_time = time.time()
            results = api_request_in_profiler(q)
            end_time = time.time()
            query_time = end_time - start_time
            results_count = len(results.Result) if hasattr(results, 'Result') else 0
            statistics.writerow([q, results_count, query_time])


def perform_profiling(queries_count):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    files = glob.glob(os.path.join(CACHE_DIR, '*'))
    for file in files:
        os.remove(file)

    # three_pos_queries = ['xml_text={0:03x}*'.format(random.randrange(0, 0xfff)) for d in xrange(queries_count)]
    # four_pos_queries = ['xml_text={0:04x}*'.format(random.randrange(0, 0xffff)) for d in xrange(queries_count)]
    three_pos_queries = set()
    while len(three_pos_queries) < queries_count:
        three_pos_queries.add(random.choice(good_three_pos_queries))
    four_pos_queries = set()
    while len(four_pos_queries) < queries_count:
        four_pos_queries.add(random.choice(good_four_pos_queries))

    print("Perform 3 pos queries without cache:")
    perform_queries_for(three_pos_queries, 'three_pos_queries_without_cache')

    print("Perform 4 pos queries without cache:")
    perform_queries_for(four_pos_queries, 'four_pos_queries_without_cache')

    print("Perform 3 pos queries with cache:")
    perform_queries_for(three_pos_queries, 'three_pos_queries_with_cache')

    print("Perform 4 pos queries with cache:")
    perform_queries_for(four_pos_queries, 'four_pos_queries_with_cache')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            queries_count = int(sys.argv[1])
            if 0 < queries_count <= 100:
                perform_profiling(queries_count)
            else:
                print("Queries count should be in range from 1 to 100!")
        else:
            print("Queries count is not a number!")
    else:
        print("Queries count isn't specified!")
