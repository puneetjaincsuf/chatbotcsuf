import scraper.Department as Department
import requests
from lxml import html
import scraper.ScraperConstants as const
import multiprocessing as mp


def get_programs():
    """ Scrape programs from CSUF catalog.
    :return: dictionary:
                Key -> Program URL
                Value -> [Program Name, Department Name, Program Type]
    """
    programs_dict = {}
    try:
        departments = Department.get_departments();
        pool = mp.Pool()
        for url, department in departments.items():
            page = requests.get(const.BASE_URL+const.SLASH+ url)
            tree = html.fromstring(page.content)
            programs = tree.xpath(const.PROGRAM_XPATH)
            for i in range(len(programs)):
                program_url = programs[i].attrib[const.HREF];
                program_name = programs[i].text;
                args = (program_name, department.get()[0])
                programs_dict[program_url] = pool.apply_async(__scrape_programs, args)
    except Exception as e:
        print(e)

    return programs_dict;


def __scrape_programs(program_name, department_name):
    """
    This method runs in a pool and scrape programs

    :param course_preview_url:
    :param program_name:
    :return:
    """
    try:
        program_list = []
        program_list.append(program_name)
        program_list.append(department_name)
        program_list.append(__check_program_type(program_name))
    except Exception as e:
        print(e)

    return program_list


def __check_program_type(name):
    """
    Check and return appropriate program

    :param name:
    :return:
    """
    if name.endswith(const.MASTER):
        return const.MASTER_TYPE
    elif name.endswith(const.BACHELOR):
        return const.BACHELOR_TYPE
    elif name.endswith(const.MINOR):
        return const.MINOR_TYPE
    elif name.endswith(const.CERTIFICATE):
        return const.CERTIFICATE_TYPE
    elif name.endswith(const.DOCTORATE):
        return const.DOCTORATE_TYPE
    elif name.endswith(const.INTERN):
        return const.INTERN_TYPE
    elif name.endswith(const.CREDENTIAL):
        return const.CREDENTIAL_TYPE
