# Newspaper_crawler

Newspaper data crawler for Asgaard Lab Assignment

Crawler Development: 	Python3
Database :			MySQL 
Data Visualization:		PHP
asgaard_crawler.py
Python3 has been used to develop crawler specially article from newspaper. Two different newspapers are selected for crawling named as CNN (https://edition.cnn.com) and Daily Star BD (https://www.thedailystar.net/). However, this code has been designed as a generic one, where any other newspaper link can be used to crawl article. A library has been used to build with article of the targeted newspaper named as Newspaper3k which can be installed via pip in Linux. 

Two python3 libraries are used to develop this code newspaper3k1 and pymysql2, which are.

import pymysql		# for MySQL database handle
import newspaper	# for newspaper content linkup  

Program starts from the main function where, the prerequisite variable are declared, which must be modified based on your environment credentials. 
 
Then the program connect with MySQL database with those prerequisites. 

Then database table needs to be truncated for clearing the existing articles.  

Then the targeted newspaper named and links are stored inside a list. 

Newspaper contents are loaded using a function from newspaper3k library named newspaper_article_build. 

Then those articles are passed for processed. 

Individual article is downloaded, parsed and checked whether it is related to the targeted topic. Then passed article’s title, authors, and description with the article matched number through a database insertion function. All the processes are grouped inside a try-cacth exception handler to bypass unwanted issues. Articles are also prepossessed to fulfill the query execution. 

Processed Articles are now ready to store in database. The insertion query is secured by try-catch exception handling for execution rollback. 

index.php
Raw PHP is used to write the content in web version. It creates the database connection at the very first of its code. 
Two newspapers are analyzed for article collection which are listed as a drop down in PHP. 
Then the visualization results are filtered based on this selection. 
Finally results are displayed in a table with collapse div. When anyone click on the title, the entire description will be loaded. 

