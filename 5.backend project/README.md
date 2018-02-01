# Logs Analysis Project

The goal of this project is to build a reporting tool (in plain text) to answer different questions based on the information stored on a database. The tool will be a Python program using the `psycopg2` module to connect to the database.

## Contents

- [Code Design](#code-design) 
- [Usage](#usage)

## Code Design

The comments on this section will be focused on the backend code, that means the query statements to retrieve the data from the database.

The primary objective is to use a single query in each scenario minimizing the postprocessing code in Python. In all reports this has been achieved and the only postprocessing used is to add some titles to the output.

In the following sections there is the code review for each report.

### 1. What are the most popular three articles of all time?
The tricky part on this report is that the ***log*** table does not contain an easy link to the ***articles*** table

**Log** table example

| path | status | id |
| ------------- | ------------- | ------------- |
| /article/candidate-is-jerk | 200 OK | 1678924 |
| /article/balloon-goons-doomed | 200 OK | 1678927 |


**Articles** table example

| slug | id |
| ------------- | ------------- |
| bad-things-gone | 23 |
| balloon-goons-doomed | 24 |

To solve this problem we use the string operator `||` within the query:

`log.path = '/article/' || articles.slug` 

As last point on this query, just to mention that we've assumed that only the correct requests should be considered, that means that the program will return only the **log** records where the **status** is ok.

So, the final query to fetch the results will be:

```SQL
SELECT articles.title,count(*) AS num
FROM articles,log
WHERE log.status like '2%' AND
      log.path = '/article/' || articles.slug
GROUP BY articles.title
ORDER BY num DESC LIMIT 3
``` 

### 2. Who are the most popular article authors of all time?
In this case the potential issue is that the results are based on **Authors** instead of **Articles**, that means that we should link three tables. This can be done in a single query as follow:

```SQL
SELECT authors.name,count(*) AS num
FROM articles,log,authors
WHERE log.status LIKE '2%' AND
      log.path = '/article/' || articles.slug AND
      articles.author = authors.id
GROUP BY authors.name
ORDER BY num DESC
```

As last point on this query, just to mention that we've assumed that only the correct requests should be considered, that means that the program will return only the **log** records where the **status** is ok.

### 3. On which days did more than 1% of requests lead to errors?
The most difficult parts on this query is to return a column as a calculated value that is based on a subset of data and also filter the final results based on this new value. That means to have something like:

| day | errors |
| ------------- | ------------- |
| 2016-10-05 | 1.4 |
| 2016-08-23 | 1.3 |

Where the **errors** column is a calculation based on a subset of records and the rows shown should be filtered depending on the values of this column (for example greater than 1).

There are different solutions for this item, like the creation of a **View**, but it's also possible to use a single query to achieve the same results, by using a `filter` clause that extends the aggregate functions.

To have the new column with the calculated value we can use:
```
count(status) filter (WHERE status LIKE '4%' OR status LIKE '5%') / count(*)
```
To show the result in a more convenient way we add :
```
ROUND(<previous code>::dec*100,1) 
```
To filter the results to only show the values greater than 1% we should also add the condition as a **HAVING** clause with:
```
HAVING count(status) filter (WHERE status LIKE '4%' OR status LIKE '5%') / 
    count(*)::dec > 0.01;
```
Because the data is stored in a **datetime** format, we should also convert this to a **date** and group the results. The final statement will be:
```SQL
SELECT time::date as day, 
       ROUND(count(status) filter
         (WHERE status LIKE '4%' OR status LIKE '5%') / count(*)::dec*100,1)
FROM log
GROUP BY day
HAVING count(status) filter (WHERE status LIKE '4%' OR status LIKE '5%') / 
       count(*)::dec > 0.01;
```

### Usage

#### 1. Prerequisites

In order to execute the program correctly the following components are needed:
- PostgreSQL
- *news* database
- Python

#### 2. Load the data

[Download the data here](https://www.dropbox.com/s/rhsf1vj1tsr2to8/newsdata.zip?dl=0), it's a zip file, so please unzip the file before using it.
To load the data, go to the folder where you have the file from the zip and use the following command:

`psql -d news -f newsdata.sql` 

This command will connect to your database and execute the SQL commands to populate the data needed to run the python scrypt with the analysis.

#### 3. Running the program

To see the results start a terminal session and point to the folder where the Python program is located. From there:

```
python report.py
```

The results should appear in the terminal window.


-----


Re-use connection but not cursor (http://initd.org/psycopg/docs/faq.html)