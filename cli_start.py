import MySQLdb
import curses
screen = curses.initscr()
#curses.noecho() #Stops key presses from the user from showing on screen
#curses.curs_set(0) #removes cursor from screen
#curse.cbreak() react instatnly no enter key
screen.keypad(1) #mode the screen uses to pature key presses.
db = MySQLdb.connect("mysql.eecs.oregonstate.edu", "cs419-g6", "group6data", "cs419-g6")
cursor = db.cursor() 
screen.addstr("Welcome to the Simplified Advising Scheduling System\n")
while True:
	screen.addstr("Please Select from the following menu:\n1)Read your advising appointments\n2)Manage your advising appointments\n3)Exit\n")
	event = screen.getch()
	if event == ord("3"): break
	elif event == ord("1"):
		screen.addstr("Please give your name.\n")
		name = screen.getstr()
		name2 = "'" + name + "'"
		screen.addstr("Schedule for " + name + "\n")
		sql_read = "SELECT * FROM (SELECT a_name, s_name FROM advising_schedule, advisor, student WHERE advising_schedule.ad_id = advisor.a_id AND advising_schedule.stud_id = student.s_id) AS alias WHERE alias.a_name = " + name2 + "\n"
		screen.addstr("SQL query is: " + sql_read)
		try:
			cursor.execute(sql_read)
			results = cursor.fetchall()
			for row in results:
				aname = row[0]
				sname = row[1]
				screen.addstr("Appointment with student: " + sname + "\n")
		except:
			screen.addstr("No advisor by that name.\n")
	elif event == ord("2"):
		screen.addstr("Please give your name and the name of the student.\n")
curses.endwin()
