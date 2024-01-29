import json
from data_processing.drivers.selenium_manager import SeleniumManager
import logging
from event_manager.models import Event
from datetime import datetime
import pytz

logger = logging.getLogger('func_log')


def create_event_from_json(json_data):
    try:
        event = Event()

        event.title = json_data.get('name', '')
        event.description = json_data.get('description', '')
        event.image_url = json_data.get('image', '')

        start_date_str = json_data.get('startDate', '')
        end_date_str = json_data.get('endDate', '')
        if start_date_str:
            start_date_str = start_date_str.split('(')[0].strip()
            event.start_date = datetime.strptime(
                start_date_str, '%a %b %d %Y %H:%M:%S GMT+0000')
            event.start_date = event.start_date.replace(tzinfo=pytz.UTC)
        if end_date_str:
            end_date_str = end_date_str.split('(')[0].strip()
            event.end_date = datetime.strptime(
                end_date_str, '%a %b %d %Y %H:%M:%S GMT+0000')
            event.end_date = event.end_date.replace(tzinfo=pytz.UTC)

        location_info = json_data.get('location', {})
        event.location = location_info.get('name', '')
        event.source_url = json_data.get('url', '')

        event.save()

        return event

    except ValueError as e:
        logger.error("ValueError in create_event_from_json: {e}")
    except Exception as e:
        logger.error("Exception in create_event_from_json: {e}")

def parse_script_content_to_event(script_content):
    try:
        data = json.loads(script_content)
        create_event_from_json(data)
    except json.JSONDecodeError:
        logger.error('Error parsing data to json')


def collect_script_contents_gout():
    
    url_page = 'https://goout.net/en/poland/events/lezxxnfti/'
    driver = SeleniumManager.setup_driver()
    SeleniumManager.open_url(driver, url_page)
    SeleniumManager.scroll_page(driver, 5)
    main_element = SeleniumManager.find_element_by_class_name(
        driver, 'content')
    
    event_list_page = SeleniumManager.find_element_by_class_name(
        main_element, 'event-listing-page')
    
    listing_grid = SeleniumManager.find_element_by_xpath(
        event_list_page, "//div[@data-v-dcaa2bd2 and contains(@class, 'items row')]")
    
    scripts = SeleniumManager.find_elements_by_xpath(
            listing_grid, "//script[@data-v-483a2913 and @type='application/ld+json']")
    
    for el in scripts:
        script_content = SeleniumManager.get_attribute(el, "innerHTML")
        print(script_content)
        if script_content:
            parse_script_content_to_event(script_content)

    SeleniumManager.close(driver)
