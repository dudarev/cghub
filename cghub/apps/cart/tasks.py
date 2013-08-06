import datetime
import os
import logging

from celery.task import task

from celery import states
from djcelery.models import TaskState

from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone

from cghub.apps.cart.cache import (
        AnalysisFileException, save_to_cart_cache, is_cart_cache_exists)

from cghub.apps.core.utils import (
                    decrease_start_date, is_celery_alive,
                    generate_task_id, WSAPIRequest)


cart_logger = logging.getLogger('cart')


@task(ignore_result=True)
def cache_results_task(analysis_id, last_modified):
    """
    If file for specified uid not exists in settings.CART_CACHE_DIR,
    attributes will be received and saved.
    Two different files will be saved,
    the first contains all attributes and the second only most necessary ones.

    :param analysis_id: file analysis id
    :param last_modified: file last_modified
    """
    try:
        save_to_cart_cache(analysis_id, last_modified)
    except AnalysisFileException as e:
        cart_logger.error(str(e))


def cache_file(analysis_id, last_modified, asinc=False):
    """
    Create celery task if asinc==True, or execute task function.
    Previously check that task was not created yet.
    """
    if not asinc:
        cache_results_task(analysis_id, last_modified)
        return
    task_id = generate_task_id(analysis_id=analysis_id, last_modified=last_modified)
    try:
        task = TaskState.objects.get(task_id=task_id)
        # task failed, reexecute task
        if (task.state == states.FAILURE or
            task.tstamp < timezone.now() - datetime.timedelta(days=2)):
            # restart
            task.tstamp = timezone.now()
            task.save()
            cache_results_task.apply_async(
                    kwargs={
                        'analysis_id': analysis_id,
                        'last_modified': last_modified},
                    task_id=task_id)
    except TaskState.DoesNotExist:
        # run
        cache_results_task.apply_async(
                    kwargs={
                        'analysis_id': analysis_id,
                        'last_modified': last_modified},
                    task_id=task_id)


@task(ignore_result=True)
def add_files_to_cart_by_query_task(queries, attributes, session_key):
    """
    Obtains all results for specified query and adds them to cart

    :param queries: list of queries data should be obtained by
    :param attributes: list of attributes should be added to cart
    :param session_key: Session.session_key

    How to change variables stored in session:
    https://docs.djangoproject.com/en/dev/topics/http/sessions/#using-sessions-out-of-views
    """
    # check session exists
    try:
         Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return
    # modify session
    session_store = SessionStore(session_key=session_key)
    cart = session_store.get('cart', {})

    celery_alive = is_celery_alive()

    def callback(data):
        analysis_id = data['analysis_id']
        if analysis_id not in cart:
            return
        filtered_data = {}
        for attr in attributes:
            filtered_data[attr] = data.get(attr)
        cart[analysis_id] = filtered_data
        last_modified = data['last_modified']
        if not is_cart_cache_exists(analysis_id, last_modified):
            cache_file(analysis_id, last_modified, celery_alive)


    for query in queries:
        if query:
            query = decrease_start_date(query)
            result = WSAPIRequest(query=query, callback=callback)

    session_store['cart'] = cart
    session_store.save()
