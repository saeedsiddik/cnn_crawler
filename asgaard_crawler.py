'''
Author: Md Saeed Siddik, IIT DU, BD
'''
import pymysql
import newspaper

#mysql database connection 
def database_connection_start(host, user, password, database_name):
	db = pymysql.connect(host, user, password, database_name)
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchone()
	print ("Database version : %s " % data)  # check the db is connected
	
	return db

#data preprocessing to store in database
def article_preprocessing_for_database(text_data):
	processed_data = pymysql.escape_string(text_data)
	processed_data = processed_data.replace("\\n" , "<br />")
	processed_data = processed_data.replace("'" , "`")
	processed_data = processed_data.replace("-" , "\-")
	processed_data = processed_data.replace("%" , "\%")
	return processed_data

#newspaper content loading based on the url
def newspaper_article_build(newspaper_url):
	newspaper_content_build = newspaper.build(newspaper_url, memoize_articles=False)
	return newspaper_content_build

def individual_article_process_for_db_store(db, table_name, newspaper_name, newspaper_content_build, article_topic_to_show, number_of_article_to_show):
	news_counter = 0	# to check the maximum number of article in show	
	cursor = db.cursor()
	
	for article in newspaper_content_build.articles:		# loop for investigating entire articles
		if (news_counter >=number_of_article_to_show):		# check the maximum data 
		    break
		try:							# handle exception 
		    article.download()					# download the article details
		    article.parse()					# parse the article 
		    if article_topic_to_show in article.text:		# check the targeted topic in article
		        news_counter += 1
		        id = news_counter				# news ID 
		        title = article_preprocessing_for_database(article.title)
		        description = article_preprocessing_for_database(article.text)
		        url = article.url
		        authors = article_preprocessing_for_database(', '.join([str(elem) for elem in article.authors]))	#hence, authors is a list, it it needed to convert a String
		        article_insert_in_database(db, table_name, newspaper_name, id,title,description, url, authors)		# call database insertion query
		except Exception as e:
		    print (e)
		    continue
	print ("END")

#insert newspaper article to database table
def article_insert_in_database(db, table_name, newspaper_name, id,title,description, url, authors):
      
	cursor = db.cursor()
	sql = "INSERT INTO %s(id, title, description, authors,type) VALUES ('%s','%s','%s', '%s','%s')"%(table_name,id, title,description, authors, newspaper_name)
	try:
		cursor.execute(sql)
		db.commit()
		print("OK; "+ newspaper_name+ "; "  +title)
	except:
		print ("Problem; "+ newspaper_name+ "; "  +title)
# 		print (description)
		db.rollback()
		
# database content clear for fresh data
def database_clear(db, table_name):
    cursor = db.cursor()
    sql1 = "TRUNCATE TABLE %s"%table_name 
    try:
        cursor.execute(sql1)
        db.commit()
    except:
        db.rollback()


# show data for checking 
def article_show_in_console(db, table):
	cursor = db.cursor()
	sql = "SELECT * FROM '%s'"%(table)
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

#database connection close
def database_connection_close(db):
	db.close()

def main():
	print ("program start for article crawler in asgaard lab assignment")
	topic = "Covid-19"
	
	host = "localhost"
	user = "root"
	password = "1987"
	database_name = "crawler"
	table_name = "news"
	
	db = database_connection_start(host,user,password,database_name)	# connect MySQL database with credintial 
	database_clear(db, table_name)						# clear the database table content for storing fresh article 

	newsList = [["cnn", "https://edition.cnn.com"], ["dailystar", "https://www.thedailystar.net/"]]	# targeted newspaper URL for articel collection
	for newsInfo in newsList:
		newspaper_content_build = newspaper_article_build(newsInfo[1])		# build the newspaper URL using python-newspaper3k library
		individual_article_process_for_db_store(db, table_name, newsInfo[0], newspaper_content_build, topic, 25)

	database_connection_close(db)
	print("Program end")

# Python main function to start the code
if __name__ == '__main__':
    main()

