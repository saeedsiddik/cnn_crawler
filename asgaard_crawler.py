#mysql database connection 
import pymysql
db = pymysql.connect("localhost","root","1987","crawler" )
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)  # check the db is connected

#---- end of database connection

#newspaper content loading
import newspaper
cnn_paper = newspaper.build('https://edition.cnn.com', memoize_articles=False)

#insert cnn article to database table
news_counter = 0
cursor = db.cursor()
for article in cnn_paper.articles:
    if (news_counter >=25):
        break
    try:
        article.download()
        article.parse()
        if "Covid-19" in article.text:
            news_counter += 1
            
            id = news_counter
            title = str(article.title)
            title = title.replace("\'" , "\`")
            desc = str(article.text)
            description = pymysql.escape_string(desc)
            description = description.replace("\\n" , "<br />")
            description = description.replace("'" , "`")
            description = description.replace("-" , "\-")
            description = description.replace("%" , "\%")
#             print (description)
            
            cursor = db.cursor()
            sql = "INSERT INTO cnn_news(id, title, description) VALUES ('%s','%s','%s')"%(id,title,description)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                print ("problem in insert %s"%article.title)
                print (description)
                db.rollback()
                
            print (id)
            print (article.url)
            print (article.title)

    except Exception as e:
        print (e)
        continue

# show data for checking 
'''
cursor = db.cursor()
sql = "SELECT * FROM cnn_news"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sid = row[0]
        title = row[1]
        desc = row[2]
        print (sid, title, desc)
except:
    print ("error in data show")
'''

#database connection close
db.close()


