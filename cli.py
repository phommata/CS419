import MySQLdb
import curses
import smtplib
from meeting_invitation import meeting_invitation

screen = curses.initscr()
#curses.noecho() #Stops key presses from the user from showing on screen
#curses.curs_set(0) #removes cursor from screen
#curse.cbreak() react instantly, user doesn't have to press the enter key
screen.keypad(1) #mode the screen uses to pature key presses.
db = MySQLdb.connect("mysql.eecs.oregonstate.edu", "cs419-g6", "group6data", "cs419-g6")
cursor = db.cursor() 
screen.scrollok(1)



#check that the user input for advisor name is in database.	
def realName(named):
	nameCheck = "SELECT ad_name FROM advising_schedule WHERE ad_name = " + named + "\n"
	cursor.execute(nameCheck)
	getback = cursor.fetchall()
	if getback:
		return 1;
	else:
		return 0;

#Function to print menu and get user selection
#No parameters, returns char user selcted.
def printMenu():
	screen.addstr("\n\tPlease Select from the following menu:\n")
	screen.addstr("\t1)View Appointments\n\t2)Cancel Appointment\n\t3)Exit\n")
	selection = screen.getch()
	return selection;


#function to handle the reading of the database
#2 parameters, advisor's name as a string with literal quotes 
#and advisor's name as normal string. 
#Returns the number of rows / appointments
def readDatabase(str_advisor, advisor):
	sql_read = "SELECT date_time, ad_name, st_name FROM advising_schedule WHERE advising_schedule.ad_name = " + str_advisor + " ORDER BY date_time\n"
	#screen.addstr("\nSQL query is: " + sql_read) #Debugging SQL query 
	try:	
		cursor.execute(sql_read)
		results = cursor.fetchall()
		num = 0
		for row in results:
			num = num + 1
			d_t = row[0]
			aname = row[1]
			sname = row[2]
			m = str(d_t.month)
			d = str(d_t.day)
			y = str(d_t.year)
			h = str(d_t.hour)
			mi = str(d_t.minute)
			newdate_time = str(d_t) #must change from object to string
			screen.addstr("\n\tAppointment " + str(num) + " with: " + sname + " On: " + m + "/" + d + "/" + y + " At: " + h + ":" + mi + "\n")
	except:
		screen.addstr("\tNo Adviser by name of " + name + "\n")
	return num;

#Send email using meeting invite function
def emailTemp(stu_email, ad_email, student, adviser, date_time):
	rec = [stu_email, ad_email]
	body = "Advising Signup with " + adviser + " CANCELLED\nName: " + student + "\nEmail: " + stu_email + "\nDate: " + str(date_time) + "\n\nPlease contact support@engr.oregonstate.edu if you experience problems.\n"
	method = "CANCEL"
	uid = adviser + " " + str(date_time)
	meeting_invitation(rec, body, date_time, method, uid)

	return;
	
	
def cancelApp(str_advisor, advisor):
	t_rows = readDatabase(str_advisor, advisor)
	str_tRows = str(t_rows)
	screen.addstr("\n\tUsing 1-" + str_tRows + " select the appointment you want to cancel.\n\tTo return to menu: Press 0.\n")
	select = screen.getstr()
	try:
		sel_int = int(select)
	except:
		screen.addstr("\tInvalid input\n")
		return;
	if int(select) > int(t_rows):
		screen.addstr("\tThe number you have selected is too high.\n")
	if int(select) == 0:
		screen.addstr("\tReturning to Menu.\n")
		return;
	elif int(select) > 0 and int(select) <= int(t_rows): 
		#screen.addstr("Get Here?\n")
		sql_read = "SELECT date_time, ad_name, st_name FROM advising_schedule WHERE advising_schedule.ad_name = " + str_advisor + " ORDER BY date_time\n"
		#screen.addstr("SQL query is: " + sql_read) #Debugging checking that SQL query appeared the way it should
		cursor.execute(sql_read)
		results = cursor.fetchall()
		num2 = 0
		for row in results:
			num2 = num2 + 1
			appdate_time = row[0]
			aname = row[1]
			sname = row[2]
			m = str(appdate_time.month)
			d = str(appdate_time.day)
			y = str(appdate_time.year)
			h = str(appdate_time.hour)
			mi = str(appdate_time.minute)
			newdate_time = str(appdate_time) #must change from object to string
			if num2 == int(select):
				#screen.addstr("num == select\n")
				str_s_name = "'" + sname + "'"
				sql_emails = "SELECT ad_email, st_email FROM advising_schedule WHERE ad_name = " + str_advisor + " AND st_name = " + str_s_name + ";\n"
				#screen.addstr("sql emails: \n" + sql_emails + "\n")
				cursor.execute(sql_emails)
				emails = cursor.fetchall()
				for row in emails:
					adv_email = row[0]
					stud_email = row[1]
				screen.addstr("\tCanceling appointment with " + sname + " on " + m + "/" + d + "/" + y + " at " + h + ":" + mi + "\n")
				str_date = "'" + newdate_time + "'"
				sql_del = "DELETE FROM advising_schedule WHERE ad_name = " + str_advisor + " AND st_name = " + str_s_name + " AND date_time = " + str_date + "\n"
				#screen.addstr("SQL DELETE = \n" + sql_del + "\n")
				screen.addstr("\tAre you sure you want to continue? Y/N\n")
				confirm = screen.getch()
				if confirm == ord("y") or confirm == ord("Y"):
					screen.addstr("\n\tAppointment is Cancelled. Emails have been sent.\n")
					cursor.execute(sql_del)
					emailTemp(stud_email, adv_email, sname, advisor, appdate_time)
				elif confirm == ord("n") or confirm == ("N"):
					screen.addstr("\n\tAppointment has not been Cancelled.\n")
				else:
					screen.addstr("\n\tInvalid input. Appointment will not be Cancelled.\n")
				break
	
	return;



def main():
	screen.addstr("\tWelcome to the Simplified Advising Scheduling System\n")
	name = ""
	name2 = ""
	while True:
		screen.addstr("\tTo begin please provide your first and last name. ") #Need their name in every option, so might as well only ask for it once.
		screen.addstr("To exit: Press e\n")
		name = screen.getstr() #get the string they typed
		if name == "e":
			cursor.close()
			db.close()
			curses.endwin()
			return;
		name2 = "'" + name + "'" #force name into a string so it works with the SQL queries
		stat = realName(name2) #check provided name is in database
		if stat == 0: #keep asking til name is right
			screen.addstr("\tNot a valid name. Try Again\n")
		else:
			break
	while True:
		screen.refresh()
		event = printMenu()
	
		if event == ord("3"):  #3 = They want to exit CLI client
			break
		elif event == ord("1"): #1 They want to read their advising schedule
			readDatabase(name2, name)
		elif event == ord("2"): #Cancel appointment
			cancelApp(name2, name)
	cursor.close()
	db.close()
	curses.endwin()
	return;

if __name__ == "__main__":
	main()
