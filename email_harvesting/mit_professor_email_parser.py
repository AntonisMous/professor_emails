from HTMLParser import HTMLParser
import urllib
import xlwt
from tempfile import TemporaryFile

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.new_record = False

        self.key = False
        self.name = False
        self.title = False
        self.email = False
        self.per_phone = False
        self.off_phone = False

        self.get_data = False
        self.value_data = False

        self.professor = dict()
        self.professor_list = list()

    def handle_starttag(self, tag, attrs):

        if attrs:
            if attrs[0] == ('class', 'people-list'):
                self.recording = True

                # print "I encountered a new professor "

            if self.recording and tag == 'li':
                self.new_record = True
                # print "I encountered a new professor "
                self.professor = dict()

            if tag == 'div' and self.recording and self.new_record:
                if attrs[0] == ('class', 'views-field views-field-title'):
                    self.key = "Name"
                    self.name = True
                    self.value_data = True

            if tag == 'div' and self.recording and self.new_record:
                if attrs[0] == ('class', 'views-field views-field-field-person-title'):
                    self.key = "Title"
                    self.title = True
                    self.value_data = True

            if tag == 'div' and self.recording and self.new_record:
                if attrs[0] == ('class', 'views-field views-field-field-person-email'):
                    self.key = "Email"
                    self.email = True
                    self.value_data = True

            if tag == 'div' and self.recording and self.new_record:
                if attrs[0] == ('class', 'views-field views-field-field-person-phone'):
                    self.key = "Phone"
                    self.per_phone = True
                    self.value_data = True

        if self.value_data and (tag == 'a' or tag == 'div'):
            self.get_data = True

    def handle_endtag(self, tag):
        if self.recording and tag == 'li':
            # print "--ok--"
            self.professor_list.append(self.professor)
            self.new_record = False

        if tag == 'div' or tag == 'a':
            self.value_data = False

    def handle_data(self, data):
        if self.get_data and len(data) != 0:
            self.professor[self.key] = data

        self.get_data = False

# instantiate the parser and fed it some HTML
professor_list = list()

# for i in range(1, 10):
parser = MyHTMLParser()
f = urllib.urlopen("https://www.eecs.mit.edu/people/faculty-advisors")
html = f.read()
parser.feed(html)

professor_list = parser.professor_list
parser.close()

print professor_list

style0 = xlwt.easyxf('font: bold on')

book = xlwt.Workbook()

sheet1 = book.add_sheet('Mit')
sheet1.write(0, 0, 'Name', style0)
sheet1.write(0, 1, 'Title', style0)
sheet1.write(0, 2, 'Phone', style0)
sheet1.write(0, 3, 'E-Mail', style0)

grid = {'Name': 0,
        'Title': 1,
        'Phone': 2,
        'E-Mail': 3}


for i, row in enumerate(professor_list):
    
    for key in row:
        # print row
        # print key, row[key]
        if key == 'Name':
            print row[key],
            print type(row[key])
            sheet1.write(i + 1, 0, unicode(row[key]))
        if key == 'Title':
            sheet1.write(i + 1, 1, str(row[key]))
        if key == 'Dept:':

            sheet1.write(i + 1, grid['Dept'], str(row[key]))
        if key == 'Addr:':

            sheet1.write(i + 1, grid['Addr'], str(row[key]))
        if key == 'Mail:':
            print key
            sheet1.write(i + 1, grid['Mail'], str(row[key]))
        if key == 'Phone':

            sheet1.write(i + 1, 2, str(row[key]))
        if key == 'Email':
            sheet1.write(i + 1, 3, str(row[key]))
        if key == 'Netid:':
            print key
            sheet1.write(i + 1, grid['Netid'], str(row[key]))
        if key == 'Id #:':
            print key
            sheet1.write(i + 1, grid['Id'], str(row[key]))
        if key == 'Voice:':
            print key
            sheet1.write(i + 1, grid['Voice'], str(row[key]))
        if key == 'URL:':
            print key
            sheet1.write(i + 1, grid['URL'], str(row[key]))


name = "Mit professor list.xls"
book.save(name)
book.save(TemporaryFile())



