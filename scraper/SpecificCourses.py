import scraper.Program as Program
import requests
from lxml import html
import scraper.ScraperConstants as const
import re
from bs4 import BeautifulSoup

def getSpecificCourses():
    """ Scrape specific courses from CSUF catalog.

    :return: dictionary:
                Key -> Program URL
                Value -> [Program Name, Department Name, Program Type]
    """
    specific_courses_dict = {}
    try:
        programs = Program.getPrograms()
        for url, program in programs.items():
            page = requests.get(const.BASE_URL +const.SLASH+ url)

            tree = html.fromstring(page.content)

            specific_courses = tree.xpath(const.ALL_COURSES_DIV)

            for i in range(len(specific_courses)):

                course_preview_action = specific_courses[i].attrib['onclick'];
                coid, catoid = extractURLInfo(course_preview_action)
                units, short_name, course_name, course_description, type = "", "", "", "", ""
                course_preview_URL = const.BASE_URL + "/ajax/preview_course.php?" + "catoid=" + coid + "&coid=" + catoid+ "&show";
                course_preview_page = requests.get(course_preview_URL)
                soup = BeautifulSoup(course_preview_page.content, 'lxml')
                course_preview_tree = html.fromstring(course_preview_page.content)

                '''get the course information'''
                preview_page_header = course_preview_tree.xpath(const.SPECIFIC_COURSE_PREVIEW_XPATH)
                header_information = preview_page_header[0].text

                if (len(header_information) > 0):
                    units, short_name, course_name = buildCourseData(header_information)

                '''get the course description'''
                preview_page_description = course_preview_tree.xpath(const.SPECIFIC_COURSE_DESCRIPTION_XPATH)
                if (len(preview_page_description) > 0):
                    course_description = preview_page_description[0]

                '''get the course prerequisite/corerequisite'''
                course_prerequisite = []
                preview_page_prerequisite = course_preview_tree.xpath(const.SPECIFIC_COURSE_PREREQUISITE_TYPE)
                if (len(preview_page_prerequisite) > 0):

                    type, prereq = buildType(preview_page_prerequisite[0])
                    if prereq:
                        course_prerequisite.append(prereq)
                    if type:
                        div = soup.select("div.ajaxcourseindentfix")[1]
                        course_prerequisite = " ".join([word for word in div.stripped_strings]).split("Prerequisite: ")[-1]
                        specific_courses_dict[course_preview_URL] = [units.strip(), short_name.strip(), course_name.strip(), course_description.strip(),
                                                                type, course_prerequisite.strip(), program[0]];
    except Exception as e:
        print("Error Occured" + e)

    return specific_courses_dict;


def buildCourseData(course_header):
    try:
        header = course_header
        units = header[header.find("(")+1:header.find(")")]
        data = re.split('[-:]', header)
        short_name = data[0]
        course_name = re.split('[(:]', data[1])[0]
    except Exception as e:
        print("Error Occured" + e)
    return units, short_name, course_name

def buildType(preview_page_prerequisite):
    try:
        prereq = preview_page_prerequisite;
        split_type = re.split('[:]', prereq)
        type = re.sub('\s+', ' ', split_type[0])

        if (len(split_type) > 1):
            return type.strip(), split_type[1]
    except Exception as e:
        print("Error Occured" + e)

    return type.strip(), ""

def extractURLInfo(url):
    try:
        number = re.findall(r'\d+', url)
        return number[0], number[1]
    except Exception as e:
        print("Error Occured"+ e)