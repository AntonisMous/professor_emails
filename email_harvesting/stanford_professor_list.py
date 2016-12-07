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

        self.professor = dict()
        self.professor_list = list()

        self.new_prof = False
        self.span_tag_found = False
        self.get_name = False
        self.get_title = False


    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs:
            if attrs[0][0] == 'class' and attrs[0][1] == 'views-field views-field-field-profile-photo':
                print "----------------------------------"
                self.professor = dict()
                self.new_prof = True

        if self.new_prof:
            if tag == 'span':
                self.span_tag_found = True

        if self.span_tag_found and tag == 'a' and attrs:
            self.get_name = True
            link = "https://ed.stanford.edu" + attrs[0][1]
            # print link
            self.professor['link'] = link

        if self.span_tag_found and tag == 'div' and attrs:
            if attrs[0][1] == "field-content":
                self.get_title = True
                self.span_tag_found = False

    def handle_data(self, data):
        if self.get_name:
            self.professor['name'] = data
            # print data
            self.get_name = False

        if self.get_title:
            self.professor['title'] = data
            # print data
            self.new_prof = False
            self.get_title = False

            self.professor_list.append(self.professor)


class MyHTMLParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mail = ""
        self.get_mail = False
        self.return_flag = True

    def handle_starttag(self, tag, attrs):
        if self.return_flag:
            if tag == 'a' and attrs:
                if attrs[0][0] == 'href' and 'mailto:' in attrs[0][1]:
                    self.get_mail = True

    def handle_data(self, data):
        if self.get_mail:
            self.mail = data
            print self.mail
            self.return_flag = False
            self.get_mail = False

# instantiate the parser and fed it some HTML
professor_list = list()

# for i in range(1, 10):
parser = MyHTMLParser()
f = urllib.urlopen("https://ed.stanford.edu/faculty/profiles")
html = f.read()
parser.feed(html)

professor_list = parser.professor_list
parser.close()


for row in professor_list:
    parser2 = MyHTMLParser2()
    f = urllib.urlopen(row['link'])

    html = f.read()
    parser2.feed(html)
    row['mail'] = parser2.mail
print professor_list

style0 = xlwt.easyxf('font: bold on')

book = xlwt.Workbook()

sheet1 = book.add_sheet('Mit')
sheet1.write(0, 0, 'Name', style0)
sheet1.write(0, 1, 'Title', style0)
sheet1.write(0, 2, 'Mail', style0)
sheet1.write(0, 3, 'Link', style0)

grid = {'Name': 0,
        'Title': 1,
        'Mail': 2,
        'Link': 3}

for i, row in enumerate(professor_list):

    for key in row:
        # print row
        # print key, row[key]
        if key == 'name':
            print row[key],
            print type(row[key])
            sheet1.write(i + 1, 0, unicode(row[key]))
        if key == 'title':
            sheet1.write(i + 1, 1, str(row[key]))
        if key == 'Dept:':
            sheet1.write(i + 1, grid['Dept'], str(row[key]))
        if key == 'Addr:':
            sheet1.write(i + 1, grid['Addr'], str(row[key]))
        if key == 'mail':
            print key
            sheet1.write(i + 1, grid['Mail'], str(row[key]))
        if key == 'link':
            sheet1.write(i + 1, grid['Link'], str(row[key]))
        if key == 'Mail':
            sheet1.write(i + 1, 2, str(row[key]))
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

name = "Stanford University professor list.xls"
book.save(name)
book.save(TemporaryFile())



