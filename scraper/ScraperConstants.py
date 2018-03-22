""" General Constants """

PREVIEW_URL = "/preview_entity.php";
SHOW_COURSE = "/ajax/preview_course.php";
CAT_OID = "?catoid=";
ENT_OID = "&ent_oid=";
C_OID = "&coid=";
SHOW_PARAM = "&show"
BASE_URL = "http://catalog.fullerton.edu"
HREF = "href"
SLASH = "/"

""" College Constants """

COLLEGE_XPATH = "//td[@id = 'acalog-navigation']/div/a"
COLLEGE = "College"
COLLEGE_DESC_XPATH = "//strong[contains(text(), 'College Website')]/parent::*/following-sibling::p"

"""Department Constants"""

DEPARTMENT_XPATH = ".//h3[@id[starts-with(.,'ent')]]"
PROGRAM_XPATH_HREF = "//h3[@id[starts-with(.,'ent')]][1]/following-sibling::a"
DEPARTMENT_DESC_XPATH = "//h3[contains(text(), 'Introduction')]/following-sibling::p[1]"

""" Program Constants """

PROGRAM_XPATH = "//h3[.='Programs']/following-sibling::ul[following-sibling::h3[.='Courses']]/li/a"

MASTER = ("M.S.", "M.A.", "M.F.A.", "M.B.A.", "M.P.H.", "M.S.W.", "MA", "M.M.", "M.S. (online only)")
BACHELOR = ("B.S.", "B.A.", "B.F.A.", "B.M.", "B.A. (online only)")
MINOR = "Minor"
CERTIFICATE = "Certificate"
DOCTORATE = "Ed.D."
INTERN = ("Intern Program", "University Internship")
CREDENTIAL = ("Credential Program", "Severe Credential","Education Credential")

MASTER_TYPE = "Master"
BACHELOR_TYPE = "Bachelor"
MINOR_TYPE = "Minor"
CERTIFICATE_TYPE = "Certificate"
DOCTORATE_TYPE = "Doctorate"
CREDENTIAL_TYPE = "Credential"
INTERN_TYPE = "Intern"

""" Course Constants """

COURSE_PREVIEW_XPATH = "//h1[@id='course_preview_title']"
COURSE_DESCRIPTION_XPATH = "//h1[@id='course_preview_title']/following-sibling::text()[1]"
COURSE_PREREQUISITE_TYPE = "//h1[@id='course_preview_title']/following-sibling::text()[2]"
COURSE_PREREQUISITE = "//h1[@id='course_preview_title']/following-sibling::a" #"//h1[@id='course_preview_title']/following-sibling::a"
COURSE_PREREQUISITE_DESC = "//h1[@id='course_preview_title']/following-sibling::text()[2]"

TEMP = "//h1[@id='course_preview_title']/following-sibling::text()[2]/following-sibling::*"


""" General Course Constants """

GENERAL_COURSE_XPATH = "//*[starts-with(text(), 'GENERAL') and substring(text(), string-length(text()) - string-length('COURSES') +1) = 'COURSES']/parent::*/following-sibling::ul/li/a"


""" Specific Course Constants """

ALL_COURSES_DIV = "//div[count(h3)>0]/ul/li/span/a"
SPECIFIC_COURSE_PREVIEW_XPATH = "//div[@class='ajaxcourseindentfix']/h3"
SPECIFIC_COURSE_DESCRIPTION_XPATH = "//div[@class='ajaxcourseindentfix']/h3/following-sibling::text()[2]"
SPECIFIC_COURSE_PREREQUISITE_TYPE = "//div[@class='ajaxcourseindentfix']/h3/following-sibling::text()[3]"
SPECIFIC_COURSE_PREREQUISITE = "//div[@class='ajaxcourseindentfix']/h3/following-sibling::text()[2]/following-sibling::*"