# import sqlite3
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
 
    return conn
 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT *
        FROM FACILITIES
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def main():
    database = "sqlite\db\pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()

    
/* QUESTIONS 
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */
select* 
from Facilities 
where membercost>0;



/* Q2: How many facilities do not charge a fee to members? */
select count(membercost) 
from Facilities 
where membercost=0;



/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */
select facid, name, membercost, monthlymaintenance
from Facilities 
where membercost<0.2*monthlymaintenance;



/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */
select*
from Facilities
where facid in (1,5);




/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */
select name, monthlymaintenance,
    case
      when (monthlymaintenance>100) then 'expensive'
      else 'cheap'    
    end as label
from Facilities;




/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */
select firstname, surname
from Members
where joindate=(select max(joindate)
                from Members)




/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */
select distinct concat(m.firstname,' ', m.surname) as fullname, f.name
from Facilities as f, Members as m, Bookings as b
where (m.memid=b.memid) and (b.facid=f.facid)
order by fullname




/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */
select f.name, concat(m.firstname,' ', m.surname) as fullname, 
    case
      when m.memid=0 and f.guestcost>30 then f.guestcost*b.slots
      when m.memid!=0 and f.membercost>30 then f.membercost*b.slots    
    end as cost
from 
 Members as m                
                inner join Bookings b
                        on m.memid = b.memid
                inner join Facilities as f
                        on b.facid = f.facid

where starttime like '2012-09-14%'
order by cost desc



/* Q9: This time, produce the same result as in Q8, but using a subquery. */
select concat( mem.firstname,  ' ', mem.surname ) AS name, new.name, 
     sum(new.membercost * new.slots) AS cost
From Members AS mem
join(select fac.name,fac.membercost,books.slots,books.memid,fac.facid
     from Bookings books
     join Facilities fac ON books.facid = fac.facid
     where left( starttime, 10 ) =  '2012-09-14'
     ) new on mem.memid = new.memid
where mem.memid != 0
group by mem.memid
having cost >30
union
select'Guest' as name, new.name, (new.guestcost * new.slots) AS Cost
From Members as mem
join (select fac.name,fac.guestcost,books.slots,books.memid,fac.facid
     from Bookings books
     join Facilities fac on books.facid = fac.facid
    where left( starttime, 10 ) =  '2012-09-14'
     ) new on mem.memid = new.memid
where mem.memid =0
having cost >30
order by cost DESC 


/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */


select name, total_revenue FROM
             ( select  f.name 
                  , sum(CASE 
                    when b.memid <> 0 THEN  f.membercost * b.slots 
                    else f.guestcost * b.slots END ) as total_revenue 
               from Bookings b 
               join Facilities f 
                 on b.facid = f.facid 
            group by f.name 
            ) t1 
            where total_revenue < 1000
            order by 2 ;
