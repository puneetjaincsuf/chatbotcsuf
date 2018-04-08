import scraper.College as College
import requests
from lxml import html
import scraper.ScraperConstants as const
import re
import multiprocessing as mp


def get_general_courses():
    """ Scrape general courses from CSUF catalog.

    :return: dictionary:
                Key -> Program URL
                Value -> [Program Name, Department Name, Program Type]
    """
    general_courses_dict = {}
    try:
        colleges = College.get_colleges();
        pool = mp.Pool()
        for url, college in colleges.items():
            page = requests.get(const.BASE_URL + url)
            tree = html.fromstring(page.content)
            general_courses = tree.xpath(const.GENERAL_COURSE_XPATH)
            for i in range(len(general_courses)):
                college_name = college.get()[0]
                course_preview_url = general_courses[i].attrib[const.HREF];
                args = (course_preview_url, college_name)
                general_courses_dict[course_preview_url] = pool.apply_async(__scrape_general, args)
    except Exception as e:
        print(e)

    return general_courses_dict;


def __scrape_general(course_preview_url, college_name):
    """
    This method runs in a pool and scrape general courses

    :param course_preview_url:
    :param program_name:
    :return:
    """
    try:
        general_course = []
        course_preview_page = requests.get(const.BASE_URL + const.SLASH + course_preview_url)
        course_preview_tree = html.fromstring(course_preview_page.content)

        '''get the course information'''
        preview_page_header = course_preview_tree.xpath(const.COURSE_PREVIEW_XPATH)
        header_information = preview_page_header[0].text
        units, short_name, course_name = __build_course_data(header_information)

        '''get the course description'''
        preview_page_description = course_preview_tree.xpath(const.COURSE_DESCRIPTION_XPATH)
        course_description = preview_page_description[0]

        '''get the course prerequisite/corequisite'''
        course_prerequisite = []
        preview_page_prerequisite = course_preview_tree.xpath(const.COURSE_PREREQUISITE_TYPE)

        if "Prerequisites:" in course_description or "Prerequisite:" in course_description:
            type, prereq = __build_type(course_description)
        type, prereq = __build_type(preview_page_prerequisite[0])

        if prereq:
            course_prerequisite.append(prereq)

        if type:
            temp = course_preview_tree.xpath(const.TEMP)
            for i in range(len(temp)):
                text = temp[i].text
                if text != None and text.strip() != "" and text.strip() != " ":
                    course_prerequisite.append(text.strip())

        general_course.append(units)
        general_course.append(short_name.strip())
        general_course.append(course_name.strip())
        general_course.append(course_description.strip())
        general_course.append(type)
        general_course.append(course_prerequisite)
        general_course.append(college_name)
    except Exception as e:
        print(e)

    return general_course


def __build_course_data(course_header):
    """
    Create data such as units, short name, name for a general course

    :param course_header:
    :return: units, short name, course name
    """
    try:
        header = course_header
        units = header[header.find("(")+1:header.find(")")]
        data = re.split('[-:]', header)
        short_name = data[0]
        course_name = re.split('[(:]', data[1])[0]
    except Exception as e:
        print(e)

    return units, short_name, course_name


def __build_type(preview_page_prerequisite):
    """
    Extract type related information

    :param preview_page_prerequisite:
    :return: type of a general course
    """
    try:
        prereq = preview_page_prerequisite;
        split_type = re.split('[:]', prereq)
        type = re.sub('\s+', ' ', split_type[0])

        if (len(split_type) > 1):
            return type.strip(), split_type[1].strip()
    except Exception as e:
        print(e)

    return type.strip(), ""
