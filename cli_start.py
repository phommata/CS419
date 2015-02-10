import MySQLdb
import curses
screen = curses.initscr()
#curses.noecho() #Stops key presses from the user from showing on screen
#curses.curs_set(0) #removes cursor from screen
#curse.cbreak() react instantly, user doesn't have to press the enter key
screen.keypad(1) #mode the screen uses to pature key presses.
db = MySQLdb.connect("mysql.eecs.oregonstate.edu", "cs419-g6", "group6data", "cs419-g6")
cursor = db.cursor() 
screen.addstr("Welcome to the Simplified Advising Scheduling System\n")
while True:
	screen.addstr("\nPlease Select from the following menu:\n1)View Appointments\n2)Delete Appointment\n3)Create Appointment\n4)Exit\n")
	event = screen.getch()
	if event == ord("4"): break # 4 = They want to exit CLI client
	elif event == ord("1"): # 1 They want to read their advising schedule
		screen.addstr("\nPlease give your name.\n") #Need their name to look up their appointments
		name = screen.getstr() #get the string they typed
		name2 = "'" + name + "'" #force name into a string so it works with the SQL query
		
		sql_read = "SELECT * FROM (SELECT data, time, a_name, s_name FROM advising_schedule, advisor, student WHERE advising_schedule.ad_id = advisor.a_id AND advising_schedule.stud_id = student.s_id) AS alias WHERE alias.a_name = " + name2 + "\n"
		screen.addstr("SQL query is: " + sql_read) #Debugging purposes checking that SQL query appeared the way it should
		try:
			screen.addstr("Schedule for " + name + "\n")
			cursor.execute(sql_read)
			results = cursor.fetchall()
			for row in results:
				appdate = row[0]
				apptime = row[1]
				aname = row[2]
				sname = row[3]
				newdate = str(appdate) #must change from object to string
				newtime = str(apptime) #same as above
				screen.addstr("Appointment with student: " + sname + " On: " + newdate + " At: " + newtime +"\n")
		except:
			screen.addstr("No Advisor named: " + name + "\n")
	elif event == ord("2"):
		screen.addstr("Please give your name and the name of the student.\n")
	elif event - ord("3"):
		screen.addstr("Please give your name and the name of the student, and date and time.\n")
curses.endwin()
