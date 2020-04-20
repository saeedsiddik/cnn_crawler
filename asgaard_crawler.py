
import pymysql
import newspaper

#mysql database connection 
def database_connection_start(host, user, password, database_name):
#	db = pymysql.connect("localhost","root","1987","crawler" )
	db = pymysql.connect(host, user, password, database_name)
	cursor = db.cursor()
	cursor.execute("SELECT VERSION()")
	data = cursor.fetchone()
	print ("Database version : %s " % data)  # check the db is connected
	
	return db


def article_preprocessing_for_database(text_data):
	processed_data = pymysql.escape_string(text_data)
	processed_data = processed_data.replace("\\n" , "<br />")
	processed_data = processed_data.replace("'" , "`")
	processed_data = processed_data.replace("-" , "\-")
	processed_data = processed_data.replace("%" , "\%")
	return processed_data


def newspaper_article_build(newspaper_url):
	#newspaper content loading
#	cnn_paper = newspaper.build('https://edition.cnn.com', memoize_articles=False)
	newspaper_content_build = newspaper.build(newspaper_url, memoize_articles=False)
	return newspaper_content_build

def individual_article_process_for_db_store(db, table_name, newspaper_content_build, article_topic_to_show, number_of_article_to_show):
	news_counter = 0
	cursor = db.cursor()
	for article in newspaper_content_build.articles[0:10]:
		if (news_counter >=number_of_article_to_show):
		    break
		try:
			article.download()
			article.parse()
			if article_topic_to_show in article.text:
				news_counter += 1
				id = news_counter
				title = article_preprocessing_for_database(article.title)
				description = article_preprocessing_for_database(article.text)
				url = article.url

				article_insert_in_database(db, table_name, id,title,description, url)
		except Exception as e:
			print (e)
			continue


def article_insert_in_database(db, table_name, id,title,description, url):
#insert cnn article to database table
       
	cursor = db.cursor()
	sql = "INSERT INTO cnn_news(id, title, description) VALUES ('%s','%s','%s')"%(id,title,description)
	try:
		cursor.execute(sql)
		db.commit()
	except:
		print ("problem in insert %s"%title)
		print (description)
		db.rollback()
		
	print (id)
	print (url)
	print (title)



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


def database_connection_close(db):
	#database connection close
	db.close()

def main():
	print ("program start for article crawler in asgaard lab assignment")
	newspaper_url = "https://edition.cnn.com"
	newspaper_content_build = newspaper_article_build(newspaper_url)

	db = database_connection_start("localhost","root","1987","crawler")
	individual_article_process_for_db_store(db, "cnn_news", newspaper_content_build, "Covid-19", 25)
	
	print("Program end")

if __name__ == '__main__':
    main()
