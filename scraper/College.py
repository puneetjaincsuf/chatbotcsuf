import requests
from lxml import html
import scraper.ScraperConstants as const
import multiprocessing as mp


def get_colleges():

    """ Scrape colleges from CSUF catalog.
        :return: dictionary:
                    Key -> College URL
                    Value -> College Name
    """
    college_dict = {}
    try:
        page = requests.get(const.BASE_URL)
        tree = html.fromstring(page.content)
        colleges = tree.xpath(const.COLLEGE_XPATH)
        pool = mp.Pool()
        for i in range(len(colleges)):
            college_text = colleges[i].text
            if const.COLLEGE in college_text:
                college_url = colleges[i].attrib[const.HREF]
                args = (college_url, college_text)
                college_dict[college_url] = pool.apply_async(__scrape_colleges, args)
    except Exception as e:
        print(e)
    return college_dict


def __scrape_colleges(college_url, college_name):
    """
    This method runs in a pool and scrape colleges

    :param course_preview_url:
    :param program_name:
    :return:
    """
    try:
        college_list = []
        college_page = requests.get(const.BASE_URL + const.SLASH + college_url)
        college_tree = html.fromstring(college_page.content)
        desc = college_tree.xpath(const.COLLEGE_DESC_XPATH)
        if len(desc) > 0:
            description = desc[0].text
            college_list.append(college_name)
            college_list.append(description[0:description.find('.')])
        return college_list
    except Exception as e:
        print(e)