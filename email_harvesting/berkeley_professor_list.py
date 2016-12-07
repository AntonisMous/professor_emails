from HTMLParser import HTMLParser

import urllib
import xlwt
from tempfile import TemporaryFile


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.professor = dict()
        self.professor_list = list()
        self.counter = 0
        self.get_department = False
        self.get_name = False

        self.get_data = False


    def handle_starttag(self, tag, attrs):

        if tag == 'a' and attrs:
            if attrs[0][0] == 'href' and "/faculty/" in attrs[0][1]:
                # print "I encountered a new professor "
                self.professor = dict()
                self.counter += 1
                self.get_name = True

                self.professor['link'] = "http://vcresearch.berkeley.edu"+attrs[0][1]
                # self.link = "http://vcresearch.berkeley.edu"+attrs[0][1]
                self.professor_list.append(self.professor)

            if attrs[0][0] == 'href' and "/taxonomy/" in attrs[0][1]:
                self.get_department = True

    def handle_data(self, data):
        if self.get_name:
            self.professor['name'] = data
            # print data, " ", self.link
            self.get_name = False

        if self.get_department:
            self.professor['department'] = data
            # print data, " ", self.link
            self.get_department = False


class MyHTMLParser2(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.mail = ""
        self.return_flag = True

    def handle_data(self, data):

        if "@" in data and self.return_flag:
            self.mail = data
            # print self.mail
            self.return_flag = False




# instantiate the parser and fed it some HTML
professor_list = list()
new_professor_list = list()
#
# for i in range(1, 10):
parser = MyHTMLParser()
f = urllib.urlopen("http://vcresearch.berkeley.edu/faculty-expertise?name=&expertise_area=&term_node_tid_depth=")
html = f.read()
parser.feed(html)

professor_list = professor_list + parser.professor_list
# print professor_list
# print parser.counter, len(professor_list)
parser.close()

print "page 1"
for i, row in enumerate(professor_list):
    # print "-------------------------------"
    # print row['name']
    try:
        parser2 = MyHTMLParser2()
        f = urllib.urlopen(row['link'])

        html = f.read()
        parser2.feed(html)
        row['mail'] = parser2.mail
        parser2.close()
    except:
        # print "--not ok--"
        del professor_list[i]

for i in range(1, 49):
    print "page ", i+1
    new_professor_list = list()
    parser = MyHTMLParser()
    f = urllib.urlopen("http://vcresearch.berkeley.edu/faculty-expertise?name=&expertise_area=&term_node_tid_depth=&page="+str(i))
    html = f.read()
    parser.feed(html)

    new_professor_list = new_professor_list + parser.professor_list
    # print professor_list
    # print parser.counter, len(professor_list)
    parser.close()

    for i, row in enumerate(new_professor_list):
        # if row['name'] == 'George A. Akerlof':
        # print "-------------------------------"
        # print row['name']
        try:
            parser2 = MyHTMLParser2()
            f = urllib.urlopen(row['link'])

            html = f.read()
            parser2.feed(html)
            row['mail'] = parser2.mail
            parser2.close()
        except:
            # print "--not ok--"
            del new_professor_list[i]

    professor_list = professor_list + new_professor_list

print professor_list
print parser.counter, len(professor_list)


# print professor_list
style0 = xlwt.easyxf('font: bold on')

book = xlwt.Workbook()

sheet1 = book.add_sheet('Berkeley')
sheet1.write(0, 0, 'Name', style0)
sheet1.write(0, 1, 'Department', style0)
sheet1.write(0, 2, 'Mail', style0)
sheet1.write(0, 3, 'Link', style0)

grid = {'Name': 0,
        'Title': 1,
        'Dept': 2,
        'Addr': 3,
        'Mail': 4,
        'Phone': 5,
        'E-Mail': 6,
        'Netid': 7,
        'Id': 8,
        'Voice': 9,
        'URL': 10}


for i, row in enumerate(professor_list):
    for key in row:
        # print row
        # print key, row[key]
        if key == 'name':
            print row['name']
            sheet1.write(i + 1, 0, row[key].decode('utf-8'))
        if key == 'department':
            print row['department']
            sheet1.write(i + 1, 1, unicode(row[key]))
        if key == 'mail':
            print row["mail"]
            sheet1.write(i + 1, 2, unicode(row[key]))
        if key == 'link':
            print row['link']
            sheet1.write(i + 1, 3, unicode(row[key]))



name = "Berkeley.xls"
book.save(name)
book.save(TemporaryFile())
#
