## **LOG ANALYSIS PROJECT**

#ALL ABOUT THE PROJECT:
-The project is about building an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

-Here, the database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the code should answer questions about the site's user activity.

-The program we write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

#EXAMPLE:
Example for how this project works in real world applications: it's a point where different pieces of software (a web app and a reporting tool, for instance) can share data.
It is one of many queries Udacity uses for logs anlysis.
```SQL
select event_day as period, sum(current_paid_students) as "Paid students", sum(current_trial_students) as "Free students"
from analytics_tables . paid_enrollment
where ("course_key" = {NANODEGREE}) and current_trial_student > 0
group by period
order by period ASC;
```

#ANSWERS TO FIND OUT FOR:
1.What are the most popular three articles of all time?
2.Who are the most popular article authors of all time?
3.On which days did more than 1% of requests lead to errors?

#REQUIRED LIBRARY:
-python version - 3.x or 2.x
-Database software(provided by Linux virtual machine). - VAGRANT [here](https://www.vagrantup.com/downloads.html)
-The software that actually runs the virtual machine. - VIRTUAL BOX [here](https://www.virtualbox.org/wiki/Downloads)
-Download or clone from [here](https://github.com/udacity/fullstack-nanodegree-vm) for newdsdata.sql file.

#STEPS INVOLVED:
1.Install virtual box but dont need to launch it.
2.Then install the vagrant software for your os and check if it is installed by running
```
vagrant --version
```
3.And you got newsdata.sql file.
4.In git bash, Change directory to vagrant directory then
```
vagrant up
```
command to run the vagrant on vm.
5.To login into vm
```
vagrant ssh
```
6.Then change directory to vagrant by
```
cd /vagrant
```
7.To load the data, cd into the vagrant directory and use the command
```
psql -d news -f newsdata.sql
```
Here's what this command does:
psql — the PostgreSQL command line program
-d news — connect to the database named news which has been set up for you
-f newsdata.sql — run the SQL statements in the file newsdata.sql
Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
-Use \c to connect to database="news".
-use \dt to see the tables in database.
-use \dv to see the views in database.
-use \q to quit the database.
8.The Python code does not build queries itself, rather it relies on views. These views has to be pre generated before running the code. To load the views you have to start psql in the news database:
```
psql -d news
```
Then start loading views.
The view query for 3 most popular articles of all time is as follows:
```SQL
create view view_popular_articles as
  select title, author, count(title) as views
  from articles, log
  where  log.path like concat('%',articles.slug)
  group by articles.title, articles.author
  order by views desc;
```
The view query for the most popular article authors of all time is as follows:
```SQL
create view view_popular_authors as
  select name, sum(view_popular_articles.views) as num
  from view_popular_articles, authors
  where authors.id=view_popular_articles.author
  group by authors.name
  order by num desc;
```
The view query for the days on which more than 1 percent of requests lead to errors:
```SQL
create view view_totalreq as
  select count(*) as count, date(time) as date
  from log
  group by date
  order by count desc;

create view view_errorreq as
  select count(*) as count, date(time) as date
  from log
  where status != '200 OK'
  group by date
  order by count desc;

create view view_err as
  select view_totalreq.date, round((100.0*view_errorreq.count)/view_totalreq.count,2) as err_p
  from view_errorreq, view_totalreq
  where view_errorreq.date = view_totalreq.date;
```
9.We need to write the backend code i.e, python code to run this application.
```.py
psycopg2.connect(database=dbname)
```
Connect to a database dbname. Connect returns a Connection object or raises an exception. And here psycopg2 is a psql database adapter for python programming language.

```.py
db.cursor()
```
Makes a Cursor object from db. Cursors are used to send SQL statements to the database and fetch results.

```.py
db.close()
```
Closes the connection.

```.py
Cursor.execute(statement)
```
Execute an SQL statement on the database.

```.py
Cursor.fetchall()
```
Fetch all the results from the current statement.

#CONTENTS:
README.md
log_analysis.py
example_output.txt

#HOW TO RUN THIS APPLICATION:
Open the git bash and get into project folder then run this command
```
python log_analysis.py
```

#LICENSE:
It is a public domain work and feel free to do whatever you want to do with it.
