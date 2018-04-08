import scraper.College as College
import requests
from lxml import html
import scraper.ScraperConstants as const
import multiprocessing as mp


def get_departments():

    """ Scrape departments from CSUF catalog.

    :return: dictionary:
                Key -> Department URL
                Value -> [Department Name, College Name]
    """
    department_dict = {}
    try:
        colleges = College.get_colleges();
        pool = mp.Pool()
        for url, college in colleges.items():
            page = requests.get(const.BASE_URL + url)
            tree = html.fromstring(page.content)
            departments = tree.xpath(const.DEPARTMENT_XPATH)
            for i in range(len(departments)):
                program_href = tree.xpath(const.PROGRAM_XPATH_HREF)
                department_url = program_href[i].attrib[const.HREF];
                department_name = __swap_department_name(departments[i].text)
                args = (department_url, department_name, college.get()[0])
                department_dict[department_url] = pool.apply_async(__scrape_departments, args)
    except Exception as e:
        print(e)

    return department_dict;


def __scrape_departments(department_url, department_name, college_name):
    """
    This method runs in a pool and scrape departments

    :param course_preview_url:
    :param program_name:
    :return:
    """
    try:
        department_list = []
        department_page = requests.get(const.BASE_URL + const.SLASH + department_url)
        department_tree = html.fromstring(department_page.content)
        desc = department_tree.xpath(const.DEPARTMENT_DESC_XPATH)
        description=""
        if len(desc) > 0:
            description = desc[0].text
            description = description[0:description.find('.')]
        department_list.append(department_name)
        department_list.append(description)
        department_list.append(college_name)
        return department_list;
    except Exception as e:
        print(e)


def __swap_department_name(name):

    """
    Department names are in form of name followed by department of
    They needs to be converted to department of followed by name
    """
    names = name.strip().split(",")
    if len(names) <= 1:
        return name.strip()
    return names[1].strip() +" "+ names[0].strip()
