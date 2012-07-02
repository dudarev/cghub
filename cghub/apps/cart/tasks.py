import glob
import datetime
from celery.task import task
import os
from django.conf import settings
from lxml import etree
from cghub.cghub_api import api
from cghub.cghub_api.api import request as api_request


@task(ignore_result=True)
def cache_results_task(file_dict):
    analysis_id = file_dict.get('analysis_id')
    filename_with_attributes = os.path.join(settings.API_RESULTS_CACHE_FOLDER,
        "{0}_with_attributes".format(analysis_id))
    filename_without_attributes = os.path.join(settings.API_RESULTS_CACHE_FOLDER,
        "{0}_without_attributes".format(analysis_id))
    if os.path.isfile(filename_with_attributes) and os.path.isfile(filename_without_attributes):
        return
    result = api_request(query='analysis_id={0}'.format(analysis_id))
    with open(filename_with_attributes, 'w') as f:
        f.write(etree.tostring(result))
    with open(filename_without_attributes, 'w') as f:
        result.Result.remove(result.Result.find('sample_accession'))
        result.Result.remove(result.Result.find('legacy_sample_id'))
        result.Result.remove(result.Result.find('disease_abbr'))
        result.Result.remove(result.Result.find('tss_id'))
        result.Result.remove(result.Result.find('participant_id'))
        result.Result.remove(result.Result.find('sample_id'))
        result.Result.remove(result.Result.find('analyte_code'))
        result.Result.remove(result.Result.find('sample_type'))
        result.Result.remove(result.Result.find('library_strategy'))
        result.Result.remove(result.Result.find('platform'))
        result.Result.remove(result.Result.find('analysis_xml'))
        result.Result.remove(result.Result.find('run_xml'))
        result.Result.remove(result.Result.find('experiment_xml'))
        analysis_attribute_uri = etree.Element('analysis_attribute_uri')
        analysis_attribute_uri.text = api.CGHUB_SERVER + api.CGHUB_ANALYSIS_ATTRIBUTES_URI + '/' + analysis_id
        result.Result.append(analysis_attribute_uri)
        f.write(etree.tostring(result))


@task(ignore_result=True)
def cache_clear_task():
    files = glob.glob(os.path.join(settings.API_RESULTS_CACHE_FOLDER, '*'))
    now = datetime.datetime.now()
    for file in files:
        time_file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if now - time_file_modified > settings.TIME_DELETE_CACHE_FILES_OLDER:
            os.remove(file)
