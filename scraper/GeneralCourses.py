import scraper.College as College
import requests
from lxml import html
import scraper.ScraperConstants as const
import re


def get_general_courses():
    """ Scrape general courses from CSUF catalog.

    :return: dictionary:
                Key -> Program URL
                Value -> [Program Name, Department Name, Program Type]
    """
    general_courses_dict = {}
    try:
        colleges = College.get_colleges();
        for url, college in colleges.items():
            page = requests.get(const.BASE_URL + url)
            tree = html.fromstring(page.content)
            general_courses = tree.xpath(const.GENERAL_COURSE_XPATH)
            for i in range(len(general_courses)):
                course_preview_URL = general_courses[i].attrib[const.HREF];
                course_preview_page = requests.get(const.BASE_URL + const.SLASH + course_preview_URL)
                course_preview_tree = html.fromstring(course_preview_page.content)

                units, short_name, course_name, course_description, type = "", "", "", "", ""

                '''get the course information'''
                preview_page_header = course_preview_tree.xpath(const.COURSE_PREVIEW_XPATH)
                header_information = preview_page_header[0].text
                units, short_name, course_name = __build_course_data(header_information)

                '''get the course description'''
                preview_page_description = course_preview_tree.xpath(const.COURSE_DESCRIPTION_XPATH)
                course_description = preview_page_description[0]


                '''get the course prerequisite/corerequisite'''
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
                        if (text != None and text.strip() != "" and text.strip() != " "):
                            course_prerequisite.append(text.strip())

                general_courses_dict[course_preview_URL] = [units.strip(), short_name.strip(), course_name.strip(), course_description.strip(),
                                                            type.strip(), course_prerequisite,
                                                            college[0]];
    except Exception as e:
        print("Error Occured" + e)
    return general_courses_dict;


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
        print("Error Occured" + e)

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
            return type.strip(), split_type[1]
    except Exception as e:
        print("Error Occured" + e)

    return type.strip(), ""