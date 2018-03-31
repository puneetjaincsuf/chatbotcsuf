import requests
from lxml import html
import scraper.ScraperConstants as const


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
        for i in range(len(colleges)):
            if const.COLLEGE in colleges[i].text:
                college_url = colleges[i].attrib[const.HREF]
                description = ""
                college_page = requests.get(const.BASE_URL + const.SLASH + college_url)
                college_tree = html.fromstring(college_page.content)
                desc = college_tree.xpath(const.COLLEGE_DESC_XPATH)
                if (len(desc) > 0):
                    description = desc[0].text
                college_dict[college_url] = [colleges[i].text, description[0:description.find('.')]]
    except Exception as e:
        print("Error Occured"+ e)
    return college_dict
