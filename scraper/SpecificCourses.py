import scraper.Program as Program
import requests
from lxml import html
import scraper.ScraperConstants as const
import re
from bs4 import BeautifulSoup, NavigableString
import unicodedata

def get_specific_courses():
    """ Scrape specific courses from CSUF catalog.

    :return: dictionary:
                Key -> Program URL
                Value -> [Program Name, Department Name, Program Type]
    """
    specific_courses_dict = {}
    programs = Program.get_programs()
    for url, program in programs.items():
        page = requests.get(const.BASE_URL +const.SLASH+ url)

        tree = html.fromstring(page.content)

        specific_courses = tree.xpath(const.ALL_COURSES_DIV)

        for i in range(len(specific_courses)):
            course_preview_action = specific_courses[i].attrib[const.ON_CLICK];
            coid, catoid = extract_url_info(course_preview_action)
            course_preview_URL = const.BASE_URL + const.SHOW_COURSE + const.CAT_OID + coid + const.C_OID + catoid + const.SHOW_PARAM;
            course_prereq = []
            type = []
            units, short_name, course_name, course_description, type = "", "", "", "", ""
            course_preview_page = requests.get(course_preview_URL)
            soup = BeautifulSoup(course_preview_page.content, const.PARSER)

            whole = soup.find(const.TD, {const.CLASS: 'custompad_10'})
            thedivs = whole.find_all(const.DIV)

            title_h3 = thedivs[2]

            mytitle = title_h3.h3

            units, short_name, course_name = build_course_data(mytitle.text)

            mylist = list(mytitle.next_elements)

            description = mylist[3]

            for item in mylist[5:]:
                if isinstance(item.string, NavigableString):
                    course_prereq.append(unicodedata.normalize(const.NORMALIZATION_FORM, item.string))

            course_prerequisites = remove_duplicates(course_prereq)
            type = build_type(course_prerequisites)

            specific_courses_dict[course_preview_URL] = [units, short_name, course_name, description, type, course_prerequisites, program[0]]

    return specific_courses_dict;


def build_course_data(course_header):
    try:
        header = course_header
        units = header[header.find("(")+1:header.find(")")].strip()
        data = header.split("-", 1)
        short_name = data[0].strip()
        course_name = data[1].split("(", 1)[0].strip()
        return units, short_name, course_name
    except Exception as e:
        print("Error Occured" + e)


def build_type(prerequisites):
    try:
        types = []
        for type in prerequisites:
            if type in ('Prerequisite', 'Prerequisites', 'Corequisites', 'Corequisite', 'Corerequisite', 'Corerequisites'):

                types.append(type)
        return types
    except Exception as e:
        print("Error Occured" + e)


def remove_duplicates(duplicate):
    try:
        final_list = []
        for num in duplicate:
            if num not in final_list and num not in (' ', ', ', '\n', '.'):
                final_list.append(num.strip('. :'))
        return final_list
    except Exception as e:
        print("Error Occured" + e)


def extract_url_info(url):
    try:
        number = re.findall(r'\d+', url)
        return number[0], number[1]
    except Exception as e:
        print("Error Occured"+ e)
