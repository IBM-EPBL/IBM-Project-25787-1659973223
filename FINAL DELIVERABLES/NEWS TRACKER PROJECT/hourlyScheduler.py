from newsHandler import getRecentNews
from mailer import sendMailThroughSendGrid
from bodyHTMLRender import getHTMLBody
from dao import dbCon
from ibm_db import fetch_assoc,exec_immediate,prepare,bind_param,execute


def sample():
    articles = getRecentNews()
    stmt = exec_immediate(dbCon,"Select USERNAME,CATEGORY from user_credentials where EMAIL_PREF = true")
    dict = fetch_assoc(stmt)
    while dict!= False:
        l = []
        for i in articles:
            if any(check in dict['CATEGORY'].split(",") for check in i['category']):
                l.append(i)
        sendMailThroughSendGrid(getHTMLBody(l if len(l)<=20 else l[:20]),dict['USERNAME'])
        dict = fetch_assoc(stmt)
    delete_sql = "delete from news_data"
    del_stmt = prepare(dbCon,delete_sql)
    execute(del_stmt)
    insert_sql = "insert into news_data (TITLE,CATEGORY,LINK,SOURCE) values(?,?,?,?)"
    for i in articles:
        prep_stmt = prepare(dbCon, insert_sql)
        bind_param(prep_stmt, 1, i['title'])
        bind_param(prep_stmt, 2, i['category'])
        bind_param(prep_stmt, 3, i['link'])
        bind_param(prep_stmt, 4, i['source_id'])
        execute(prep_stmt)