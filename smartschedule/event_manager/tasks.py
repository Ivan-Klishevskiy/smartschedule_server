from celery import shared_task

from data_processing.event_generation.scrapers.goout_scraper import collect_script_contents_gout

@shared_task
def collect_script_contents_gout_task():
    collect_script_contents_gout()
