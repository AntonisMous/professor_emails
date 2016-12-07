import urllib2
import json
from bs4 import BeautifulSoup

url = ('https://ajax.googleapis.com/ajax/services/search/patent?' +
       'v=1.0&q=barack%20obama')
request = urllib2.Request(url, None, {})
response = urllib2.urlopen(request)
jsonResponse = json.load(response)
print jsonResponse
responseData = jsonResponse['responseData']
results = responseData["results"]

print "This doesn't work, no assignee data..."
for result in results:
    print "patent no.: ", result["patentNumber"]
    print "assignee: ", result["assignee"]
    print " "

print "...but this seems to."
for result in results:
    URL = "https://www.google.com/patents/"+result["patentNumber"]
    req = urllib2.Request(URL, headers={'User-Agent' : "python"})
    _file = urllib2.urlopen(req)
    patent_html = _file.read()
    soup = BeautifulSoup(patent_html, 'html.parser')
    patentNumber = soup.find("span", { "class" : "patent-number" }).text
    assigneeMetaTag = soup.find("meta", { "scheme" : "assignee"})
    patentAssignee = assigneeMetaTag.attrs["content"]
    print "patent no.: ", patentNumber
    print "assignee: ", patentAssignee
    print " "