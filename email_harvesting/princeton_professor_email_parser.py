from HTMLParser import HTMLParser
import urllib
import xlwt
from tempfile import TemporaryFile


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = False
        self.key_data = False
        self.value_data = False
        self.professor = dict()
        self.professor_list = list()

    def handle_starttag(self, tag, attrs):

        if attrs:
            if attrs[0] == ('class', 'entry vcard'):
                self.recording = True
                self.professor = dict()
                # print "I encountered a new professor "

            if attrs[0] == ('class', 'clear'):
                self.professor_list.append(self.professor)
                # print "-------------------------------+"
                self.recording = False

        if self.recording:
            if attrs:
                if attrs[0][0] == 'class':
                    if attrs[0][1] == 'key':
                        self.key_data = True
                    elif "value" in attrs[0][1]:
                        self.value_data = True

    def handle_data(self, data):
        if self.key_data:
            self.key = data
            self.key_data = False

        if self.value_data:
            self.value = data
            # print self.key, self.value
            self.professor[self.key] = self.value
            self.value_data = False

# instantiate the parser and fed it some HTML
professor_list = list()

for i in range(1, 10):
    parser = MyHTMLParser()
    f = urllib.urlopen("http://search.princeton.edu/search/index/ff/c/f//af/c/a//lf/c/l//pf/c/p//tf/c/t//faf/c/fa//df/c/d//ef/c/e//submit/submit/page/"+str(i))
    html = f.read()
    parser.feed(html)

    professor_list = professor_list+parser.professor_list
    parser.close()

print professor_list
style0 = xlwt.easyxf('font: bold on')

book = xlwt.Workbook()

sheet1 = book.add_sheet('Mit')
sheet1.write(0, 0, 'Name', style0)
sheet1.write(0, 1, 'Title', style0)
sheet1.write(0, 2, 'Dept', style0)
sheet1.write(0, 3, 'Addr', style0)
sheet1.write(0, 4, 'Mail', style0)
sheet1.write(0, 5, 'Phone', style0)
sheet1.write(0, 6, 'E-Mail', style0)
sheet1.write(0, 7, 'Netid', style0)
sheet1.write(0, 8, 'Id', style0)
sheet1.write(0, 9, 'Voice', style0)
sheet1.write(0, 10, 'URL', style0)

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
        if key == 'Name:':
            sheet1.write(i + 1, grid['Name'], str(row[key]))
        if key == 'Title:':
            sheet1.write(i + 1, grid['Title'], str(row[key]))
        if key == 'Dept:':
            sheet1.write(i + 1, grid['Dept'], str(row[key]))
        if key == 'Addr:':
            sheet1.write(i + 1, grid['Addr'], str(row[key]))
        if key == 'Mail:':
            sheet1.write(i + 1, grid['Mail'], str(row[key]))
        if key == 'Phone:':
            sheet1.write(i + 1, grid['Phone'], str(row[key]))
        if key == 'E-Mail:':
            sheet1.write(i + 1, grid['E-Mail'], str(row[key]))
        if key == 'Netid:':
            sheet1.write(i + 1, grid['Netid'], str(row[key]))
        if key == 'Id #:':
            sheet1.write(i + 1, grid['Id'], str(row[key]))
        if key == 'Voice:':
            sheet1.write(i + 1, grid['Voice'], str(row[key]))
        if key == 'URL:':
            sheet1.write(i + 1, grid['URL'], str(row[key]))


name = "Uni.xls"
book.save(name)
book.save(TemporaryFile())

