def getHTMLBody(filteredArticles):
    st = "<html><body>"
    for i in range(len(filteredArticles)):
        st = st + filteredArticles[i]['title']+"<br>"+"<a href=\""+filteredArticles[i]['link']+"\"> Click Me </a><br><br>"
    st = st + "</body></html>"
    print(st)
    return st

