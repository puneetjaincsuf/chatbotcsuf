import scraper.College as College
import requests
from lxml import html
import scraper.ScraperConstants as const


def get_departments():
    """ Scrape departments from CSUF catalog.

    :return: dictionary:
                Key -> Department URL
                Value -> [Department Name, College Name]
    """
    department_dict = {}
    try:
        colleges = College.get_colleges();
        for url, name in colleges.items():
            page = requests.get(const.BASE_URL + url)
            tree = html.fromstring(page.content)
            departments = tree.xpath(const.DEPARTMENT_XPATH)
            for i in range(len(departments)):
                program_href = tree.xpath(const.PROGRAM_XPATH_HREF)
                department_url = program_href[i].attrib[const.HREF];
                department_page = requests.get(const.BASE_URL + const.SLASH + department_url)
                department_tree = html.fromstring(department_page.content)
                desc = department_tree.xpath(const.DEPARTMENT_DESC_XPATH)
                description = ""
                if (len(desc) > 0):
                    description = desc[0].text
                    description = description[0:description.find('.')]
                department_dict[department_url] = [ swapDepartmentName(departments[i].text),
                                                    description , name ];
    except Exception as e:
        print("Error Occured" + e)

    return department_dict;


def swapDepartmentName(name):
    # Department names are in form of name followed by department of
    # They needs to be converted to department of followed by name
    names = name.strip().split(",")
    if len(names) <= 1:
        return name
    return names[1] +" "+ names[0]
