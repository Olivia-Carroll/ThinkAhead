
##############################################################################
# Author: Olivia Carroll
# Project Title: ThinkAhead
##############################################################################
from cmu_112_graphics import *
##############################################################################

##############################################################################
# API MODULE
##############################################################################

import googlemaps
import random
import os
import time
from google.cloud import translate

#https://docs.python.org/3/library/datetime.html
from datetime import date
from datetime import datetime
now = datetime.now()
exactTime = now.strftime('%H:%M:%S')
print(f"The Time is Now:{exactTime}")

today = date.today()
weekdayNum = date.today().weekday()
weekdays = [[0,'Monday', 'app.monday'],[1,'Tuesday','app.tuesday'],\
    [2,'Wednesday','app.wednesday'],[3,'Thursday','app.thursday'],\
        [4,'Friday','app.friday'],[5,'Saturday','app.saturday'],\
            [6,'Sunday','app.sunday']]
for row in weekdays:
    if row[0]==weekdayNum:
        weekday = row[1]
weekday = weekday
print(f"Todays Date is: {today}, {weekday}")

#https://developers.google.com/maps
API_KEY = 'AIzaSyDTQNcSwYrhPDcmWcEIOsI4SVQpHxYl5Fs'
#alluser_file = open('usernames','x')
googlemapssearch = googlemaps.Client(key = API_KEY)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

##############################################################################
# Log in Class
##############################################################################
class users(object):
    def __init__(self, allusers, username, password):
        self.password = password
        self.username = username

##############################################################################
# Log in Mode
##############################################################################
def logInMode_redrawAll(app, canvas):
    fill='black'
    if app.night_Mode == True:
        canvas.create_rectangle(0,0,1200,800,fill='black')
        fill='white'
    font = 'Courier 26 bold'
    canvas.create_text(app.width/2, 150, text='The Sympathetic Shadow', 
                                                                    font=font,fill = fill)
    font = 'Courier 18 bold'
    canvas.create_text(app.width/2, 200, text='Username and Password:', 
                                                                    font=font,fill = fill)
    canvas.create_text(app.width/2, 225, 
                                    text='Press any key to enter', font=font,fill = fill)
def logInMode_keyPressed(app,event):
    approved = {}
    with open('username.txt','r') as userInfo:
        for line in userInfo:
            username, password = line.strip().split(':')
            approved[username]=password
    app.username = app.getUserInput('What is your Username')
    if app.username in approved:
        app.password = app.getUserInput('What is your password?')
        approvedP = approved[app.username]
        if approvedP==app.password:
            dayAppRead(app, app.username)
            weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
                [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
                [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                    [6,'Sunday',app.sunday]]
            day = weekdayNum   
            for days in weekdays:
                if days[0] == day:
                    appMode = days[2]
            app.esl = sortedappMode(app, appMode)
            addPastDue(app)
            commonwordFinder(app)
            x = app.commonMiss
            y = []
            for value in x:
                assignment = value[0]
                if assignment not in y:
                    y.append(assignment)
            if y != [ ]:
                app.commonMissing = True
            app.mode='mainMenuMode'
        else:
            app.showMessage('Wrong Password')
    elif app.username not in approved:
        password = app.getUserInput('Account Not Found, type in a password to\
 create an account or exit to continue')
        file = open('username.txt','a')
        file.write(f'\n{app.username}:{password}')
        file.close()
        commonwordFinder(app)
        dayAppWrite(app, app.username)
        dayAppRead(app, app.username)
        addPastDue(app)
        app.mode='mainMenuMode'


##############################################################################
# dayApp
# -going to change day apps
# current project 
##############################################################################
def dayAppRead(app, username):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    for days in weekdays:
        day = days[2]
        dayN = days[1]
        import ast
        with open(f'{username}{dayN}.txt','r') as dayInfoR:
            for l in dayInfoR:
                # https://docs.python.org/3/library/ast.html
                # for AST and grammar with txt files
                newLine = ast.literal_eval(l)  
            for value in newLine:
                if value not in day:
                    day.append(value)
            day = newLine

def dayAppWrite(app, username):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    for days in weekdays:
        day = days[2]
        dayN = days[1]
        with open(f'{username}{dayN}.txt','w') as dayInfoW:
            lineList = []
            for line in day:
                if day.index(line)==0:
                    line = '0'
                else:
                    lineList.append(line)
            s = ''
            line2=str(lineList)
            s+=line2 + "\n"
            dayInfoW.write(s)

def turnedinWrite(app, username, ):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    turnedin = app.turnedin
    for days in weekdays:
        day = days[2]
        dayN = days[1]
        with open(f'{username}{dayN}.txt','w') as dayInfoW:
            lineList = []
            for line in day:
                if day.index(line)==0:
                    line = '0'
                else:
                    lineList.append(line)
            s = ''
            line2=str(lineList)
            s+=line2 + "\n"
            dayInfoW.write(s)


##############################################################################
# MainMenu Mode
##############################################################################

def mainMenuMode_redrawAll(app, canvas):
    fill = 'black'
    if app.night_Mode == True:
        canvas.create_rectangle(0,0,1200,800,fill='black')
        fill ='white'
    today = date.today()
    weekdayNum = date.today().weekday()
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    for row in weekdays:
        if row[0]==weekdayNum:
            weekday = row[1]
    canvas.create_text(app.width/2, 50, text=f'Welcome {app.username}', font='Courier 26',fill=fill)
    from datetime import datetime
    now = datetime.now()
    exactTime = now.strftime('%H:%M:%S')
    #Time syntax
    #https://docs.python.org/3/library/datetime.html
    canvas.create_text(app.width/2, 80, text=f'{exactTime}', font='Courier 20', fill=fill)

    #sessions:
    canvas.create_rectangle(30, 180, 300, 230, outline='orange',width=3)
    canvas.create_text(165, 205, text='Focus Session', font = 'Courier 20', fill = fill)
    canvas.create_rectangle(30, 290, 300, 340, outline='blue',width=3)
    canvas.create_text(165, 315, text='Relax/Break', font = 'Courier 20', fill =fill)
    canvas.create_rectangle(30, 400, 300, 450, outline='green',width=3)
    canvas.create_text(165, 425, text='Adventure', font = 'Courier 20', fill = fill)

    #Preferences
    canvas.create_rectangle(30, 510, 300, 560, outline=fill,width=3)
    canvas.create_text(165, 535, text='Settings', font = 'Courier 20', fill = fill)
    canvas.create_text(950, 175, text=f'Events for {weekday}: {today}', font = 'Courier 20', fill = fill)
    canvas.create_rectangle(850, 675, 1050, 725, outline=fill,width=3)
    canvas.create_text(950, 700, text='Calendar', font = 'Courier 20', fill = fill)

    if app.pastDue == True:
        canvas.create_rectangle(1000,50,1150,80, width = 2, outline = 'red')
        canvas.create_text(1075,65, text='past due!',font='Courier 10 bold', fill=fill)
    if app.commonMissing == True:
        canvas.create_rectangle(1000,100,1150,130, width = 2, outline = fill)
        canvas.create_text(1075,115, text='Notification',font='Courier 10 bold', fill=fill)
    day = weekdayNum
    for row in weekdays:
        if row[0]==day:
            weekday = row[1]
            appMode = row[2]
            counter = 0
            for events in app.esl:
                s = str()
                for value in events[0]:
                    s += value
                if 'Break' in s:
                    continue
                canvas.create_rectangle(750,150,1150,650, outline = fill, width=3)
                counter += 1
                eventName = events[0]
                eventHourEnd = int(events[1])
                eventMinEnd = (events[2])
                dx = 780
                dy = 160 + (counter*50)
                if len(events)<4: # to do item
                    dx = 780
                    dy = 160 + (counter*50)
                    canvas.create_line(dx+60,dy+30,dx+250,dy+30, width = 2,fill=fill)
                    if eventMinEnd <10:
                        canvas.create_text(dx+150,dy+15, text=f'{eventName} due at {eventHourEnd}:0{eventMinEnd}',fill=fill)

                    else:
                        canvas.create_text(dx+150,dy+15, text=f'{eventName} due at {eventHourEnd}:{eventMinEnd}',fill=fill)

                if len(events)>3: # event to go to
                    canvas.create_rectangle(dx+10,dy, dx +330, dy+40,outline=fill)
                    eventHS = int(events[3])
                    eventMS = int(events[4])
                    if eventMinEnd <10:
                        if eventMS <10:
                            canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill=fill)
                        else:
                            canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill=fill)
                    elif eventMS <10:
                        canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)
                    elif eventMinEnd > 10 and eventMS > 10:
                        canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)

                    else:
                        canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)


def mainMenuMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    FRAdx = [[30,300],[850,1050],[1000,1150]]
    FRAdy = [[180,230,'focusMode'],[290,340,'relaxMode'],\
        [400,450,'adventureMode'],[510,560,'settingsMode'],\
            [675,725,'calendarMode'],[50,80,'pastdueMode'],[110,140,'notification']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                if value[2]=='adventureMode':
                    Placetype = app.getUserInput('What kind of destination?')
                    app.places_return = googlemapssearch.places_nearby(app.location, radius = 400000, open_now = True, type=f'{Placetype}')
                    app.mode = value[2]
                elif value[2]=='notification':
                    x = app.commonMiss
                    y = []
                    for value in x:
                        assignment = value[0]
                        if assignment not in y:
                            y.append(assignment)
                    if y != [ ]:
                        app.showMessage(f'Start Assignment {y}!\
                            \nIn the past you have shown tendancies to turn\
                            \nthis subject in late.\
                                  \nThis is a reminder to start,or reach out for help ')
                else:
                    app.mode = value[2]

##############################################################################
# Calendar Mode
##############################################################################
today = date.today()
weekdayNum = (date.today().weekday())
#Time is Imported to display the next 5 days of due dates

def calendarMode_redrawAll(app, canvas):
    fill = 'black'
    if app.night_Mode == True:
        fill ='white'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_text(app.width//2,50,text='Week Calendar',font='Courier 25',fill=fill)
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    canvas.create_rectangle(100,100,1100,665, outline=fill, width=2)
    canvas.create_line(50,150,1100,150, fill=fill, width=2)
    canvas.create_text(1050,725, text='Back', font = 'Courier 20', fill = fill)
    canvas.create_rectangle(50,100,100,665, width=2,outline=fill)
    canvas.create_text(75,125, text='Time:', font='Courier 8',fill=fill)
    
    for hours in range(24):
        dy = hours
        canvas.create_text(75,160+(dy*21), text=f'{hours}:00', font='Courier 12',fill=fill)
    hourList = [[0,160],[1,181],[2,202],[3,223],[4,244],[5,265],[6,286],\
        [7,307],[8,28],[9,349],[10,370],[11,391],[12,412],[13,433],[14,454],\
            [15,475],[16,496],[17,517],[18,538],[19,559],[20,570],[21,591],\
                [22,612],[23,33]]
    for value in range(5):
        day = int(weekdayNum) + value
        if int(weekdayNum) + value > 6:
            day = day - 7
        for row in weekdays:
            if row[0]==day:
                weekday = row[1]
                appMode = row[2]
        x= 200 + (value*200)
        for events in appMode:
            if appMode.index(events)==0:
                    continue
            s = str()
            for value2 in events[0]:
                s += value2
            if 'Break' in s:
                continue
            if len(events)>3:
                eventName = events[0]
                eventHourEnd = int(events[1])
                eventMinEnd = int(events[2])
                eventHourStart = int(events[3])
                eventMinStart = int(events [4])
                dyS = (170+(20*eventHourStart))+(.5*(eventMinStart))
                dyE = (170+(20*eventHourEnd))+(.5*(eventMinEnd))
                canvas.create_rectangle((x-70),dyS,(x+70),dyE,outline=fill)
                canvas.create_text(x,(dyS+((dyE-dyS)//2)), text=f'{eventName}',fill=fill)
                if value==0:
                    canvas.create_rectangle((x-70),dyS,(x+70),dyE, outline='blue', width=2)
            if len(events)<4:
                eventName = events[0]
                eventHourEnd = events[1]
                eventMinEnd = events[2]
                dyE = (170+(20*eventHourEnd))+(.5*(eventMinEnd))
                canvas.create_line(x-50,dyE+10,x+50,dyE+10,fill=fill)
                canvas.create_text(x,dyE, text=f'{eventName}',fill=fill)
                if value==0:
                    canvas.create_line(x-50,dyE+10,x+50,dyE+10, fill='red')
        canvas.create_text(x,125,text=f'{weekday}',fill=fill)

    canvas.create_rectangle(100,700,300,750,outline = fill, width= 3) 
    canvas.create_text(200,725, text='Add Event', font = 'Courier 15',fill=fill)
    canvas.create_rectangle(700,700,900,750,outline = fill, width= 3)
    canvas.create_text(800,725, text='Past Due', font = 'Courier 15',fill=fill)
    canvas.create_rectangle(400,700,600,750,outline = fill, width= 3)
    canvas.create_text(500,725, text='Complete Task', font = 'Courier 15',fill=fill)
    canvas.create_rectangle(1000,700,1100,750, outline=fill, width=3)


def calendarMode_mousePressed(app, event):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    turnedin = app.turnedin
    dx = event.x
    dy = event.y
    FRAdx = [[100,300,'addTask'],[1000,1100,'mainMenuMode'],[400,600,'completeTask'],[700,900,'pastdueMode']]
    FRAdy = [[700,750]]
    for value2 in FRAdx:
        for value in FRAdy:
            if (value[0]<dy<value[1] and value2[0]<dx<value2[1]):
                if (value2[2]=='addTask'):
                    eventDay = app.getUserInput('What day would you like to add an event?')
                    if eventDay == "":
                        app.showMessage('canceled')
                        break
                    eventType = app.getUserInput('What type of Event?\n  Types: \n  due date\n  event\n  study')
                    if eventType == "":
                        app.showMessage('canceled')
                        break
                    if (eventType == 'study' or eventType == 'event'):
                        eventStartTime = app.getUserInput('What time does the event or study time start?\nin military time please:\nEx: 5 pm == 1700 \n3:00 am == 0300')
                        if eventStartTime == "":
                            app.showMessage('canceled')
                            break
                        if len(eventStartTime)<4:
                            hourStart = eventStartTime[0]
                            minuteStart = eventStartTime[1:3]
                        if len(eventStartTime)>3:
                            hourStart = eventStartTime[0:2]
                            minuteStart = eventStartTime[2:4]
                    endTime = app.getUserInput('What is the end time in military time?\nEx 5 pm == 1700 \n6:15 am == 615')
                    if len(endTime)<4:
                        hourEnd = int(endTime[0])
                        minuteEnd = int(endTime[1:3])
                    if len(endTime)>3:
                        hourEnd = int(endTime[0:2])
                        minuteEnd = int(endTime[2:4])
                    eventName = app.getUserInput('What is the class name and assignment type?')
                    if eventName == '':
                        app.showMessage('canceled')
                        break
                    for row in weekdays:
                        if row[1]==eventDay:
                            appMode = row[2]
                            if (eventType == 'study' or eventType == 'event'):
                                appMode.append([eventName,hourEnd, minuteEnd,\
                                     hourStart, minuteStart])
                                dayAppWrite(app, app.username)
                                dayAppRead(app, app.username)
                                if row[0]==weekdayNum:
                                    app.esl = sortedappMode(app, appMode)
                            else:
                                appMode.append([eventName,hourEnd,minuteEnd])
                                dayAppWrite(app, app.username)
                                dayAppRead(app, app.username)
                                if row[0]==weekdayNum:
                                    app.esl = sortedappMode(app, appMode)

                elif (value2[2]=='completeTask'):

                    dayTask = app.getUserInput('What is the day of the task?')
                    nameTask = app.getUserInput('What is the name of the task?')
                    dayOfWeek = weekdayNum

                    for row in weekdays:
                        if row[1]==dayTask:
                            dayNum = row[0]
                            if dayNum > dayOfWeek:
                                app.getUserInput('Did you forget to complete the assignment?')
                            appMode = row[2] 
                            for events in appMode:
                                if appMode.index(events)==0:
                                    continue
                                if events[0]==nameTask:
                                    turnedin.add(events)
                                    appMode.remove(events)
                    
                    dayAppWrite(app, app.username)
                    dayAppRead(app, app.username)

                else:
                    dayAppRead(app, app.username)
                    app.mode = value2[2]


##############################################################################
# Past Due calendar mode
##############################################################################

def pastdueMode_redrawAll(app,canvas):
    fill = 'black'
    if app.night_Mode == True:
        fill ='white'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_text(app.width//2,50, text='Past Due Assignments', font= 'Courier 30', fill=fill)
    canvas.create_text(1050,725, text='Back', font = 'Courier 20', fill = fill)
    canvas.create_rectangle(1000,700,1100,750, outline=fill, width=3)

    x = 950
    counter = 0
    for events in app.missedDates:
        w = app.width//2
        canvas.create_rectangle(w-200,150,w+200,700, outline = fill, width=3)
        counter += 1
        eventName = events[0]
        eventHourEnd = int(events[1])
        eventMinEnd = (events[2])
        eventday = events[3]
        dx = 410
        dy = 115 + (counter*50)
        if len(events)<6: # to do item
            dx = 410
            dy = 115 + (counter*50)
            canvas.create_rectangle(dx,dy,dx+30,dy+30, width = 2, outline=fill)
            dx = dx + 50
            if eventMinEnd <10:
                
                canvas.create_text(dx+150,dy+15, text=f'{eventName} due at {eventHourEnd}:0{eventMinEnd} on {eventday}',fill=fill)

            else:
                canvas.create_text(dx+100,dy, text=f'{eventName} due at {eventHourEnd}:{eventMinEnd}',fill=fill)
        if len(events)>5: # event to go to
            canvas.create_rectangle(dx+10,dy, dx +330, dy+40,outline=fill)
            eventHS = int(events[3])
            eventMS = int(events[4])
            if eventMinEnd <10:
                if eventMS <10:
                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:0{eventMinEnd} on {eventday}',fill=fill)
                else:
                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:0{eventMinEnd} on {eventday}',fill=fill)
            elif eventMS <10:
                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:{eventMinEnd} on {eventday}',fill=fill)
            elif eventMinEnd > 10 and eventMS > 10:
                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd} on {eventday}',fill=fill)

            else:
                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd} on {eventday}',fill=fill)


def pastdueMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    # each check is at (410,dy,430,dy+30) dy is 160+(counter*50) so 160+(50x)

    FRAdx = [[1000,1100],[410,430]]
    FRAdy = [[700,750,'calendarMode']]
    eventNum = len(app.missedDates)
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                if value[2]=='show':
                    addPastDue(app)
                else:
                    app.mode = value[2]

    if app.pastDue == True:
        ex = event.x
        ey = event.y
        FRAdx = [[410,440]]
        FRAdy = []
        for checks in range(eventNum):
            dy = 115+(50*(checks+1))
            FRAdy.append([dy,dy+30,'checks',f'{checks}'])
        
        eventNum = len(app.missedDates)
        for value in FRAdy:
            for value2 in FRAdx:
                if value[0]<ey<value[1] and value2[0]<ex<value2[1]:
                    if value[2]=='checks':
                        truth = app.getUserInput('Did you forget to do this assignment yes/no?')
                        if truth == 'yes':
                            for events in app.missedDates:
                                if events[4]==value[3]:
                                    name = events[0]
                                    file = open('pastDueHistory.txt','a')
                                    file.write(f'\n{name}')
                                    file.close()
                            app.showMessage('It is suggested that \
you complete this assignment or move it to a better time. \n\
Information has been stored to notify you earlier of \
similar assignments')
                    '''for events in app.missedDates:
                        if events[4]==value[3]:
                            events = events
                    app.missedDates.remove(events)'''
                    

##############################################################################
# past due info add
# - addPastDue adds all past due tasks
##############################################################################
        
def addPastDue(app):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    counter = 0
    for value in range(3):
        if value == 0:
            continue
        x = weekdayNum
        x = x - value
        if x < 0:
            x = x + 7
        for row in weekdays:
            if row[0]==x:
                weekday = row[1]
                appMode = row[2]

        for events in appMode:
            if appMode.index(events)==0:
                continue
            if len(events)<4:
                app.pastDue = True
                counter += 1
                appMode.remove(events)
                events.append(f'{weekday}')
                events.append(f'{counter}')
                app.missedDates.append(events)
                #app.pastDue = True



##############################################################################
# Common Misses
# finds commonly missed assignments
# Opens file 'pastDueHistory.txt' and reads the assignments that have been
#  submitted late
##############################################################################
def wordFinder(app):
    with open('pastDueHistory.txt','r') as pastHistory:
        words = []
        for line in pastHistory:
            currW = ''
            for value in line:
                if value.isspace():
                    words.append(currW)
                    currW=''
                else:
                    currW += value
                
        for word in words:
            low = ['Homework','homework','Lecture','HW','hw','','project','PS','Problem Set']
            for wordlow in low:
                if word == wordlow:
                    words.remove(word)
        return words


def commonwordFinder(app):
    foundwords = wordFinder(app)
    day = weekdayNum
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    for row in weekdays:
        if row[0]==day:
            weekday = row[1]
            appMode = row[2]
    for events in appMode:
        if appMode.index(events)==0:
            continue
        name = events[0]
        words = []
        currW = ''
        for letter in name:
            if letter.isspace():
                words.append(currW)
                currW=''
            else:
                currW += letter
        for word in words:
            for wordlow in foundwords:
                if word == wordlow:
                    app.commonMiss.append(events)


##############################################################################
# Focus Mode
##############################################################################

import requests
import json
app_id = "a56dea3e"
app_key = "9f94d98774a5fdd378172c12c455ec58"
language = "en-gb"
word_id = "example"
#https://developer.oxforddictionaries.com/documentation/getting_started
#grammar and information on import for future
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
def focusMode_redrawAll(app,canvas):
    fill = 'black'
    fill2 = 'grey'
    fill3='grey'
    fill4 ='black'
    if app.night_Mode == True:
        fill ='white'
        fill3='dark grey'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_text(app.width/2, 50, text='Focus', font='Courier 30',fill='orange')
    canvas.create_rectangle(50,675,300,725, outline='orange', width=3)
    canvas.create_text(175,700, text='Main Menu', font = 'Courier 20', fill = fill)
    from datetime import datetime
    now = datetime.now()
    exactTime = now.strftime('%H:%M:%S')
    canvas.create_text(app.width/2, 80, text=f'{exactTime}', font='Courier 20', fill=fill)
    
    canvas.create_rectangle(50,75,300,125, outline = 'orange', width = 3)
    canvas.create_text(175,100, text='Timer', font='Courier 20', fill=fill)

    canvas.create_rectangle(50,175,300,225, outline = 'orange', width= 3)
    canvas.create_text(175,200, text = 'Focus Tasks', font='Courier 20', fill=fill)
    
    ### Class aids
    if app.night_Mode == True:
        canvas.create_rectangle(900,200,1150,400,width=5,outline='blue',fill=fill3)
    if app.night_Mode == False:
        canvas.create_rectangle(900,200,1150,400,width=5,outline='blue')
    canvas.create_text(1025,225,text='Class Aids',font='Courier 18',fill=fill4)
    canvas.create_line(970,235,1080,235,width=2,fill=fill4)

    canvas.create_rectangle(930,250,1120,300,width=2,outline=fill4)
    canvas.create_text(1025,275,text='Calculator',font='Courier 18',fill=fill4)
    canvas.create_rectangle(930,315,1120,365,width=2,outline=fill4)
    canvas.create_text(1025,340,text='Dictionary',font='Courier 18',fill=fill4)
    #canvas.create_rectangle(930,380,1120,430,width=2,outline=fill4)
    #canvas.create_text(1025,405,text='Translator',font='Courier 18',fill=fill4)

    if app.calculator == True:
        canvas.create_image(1025, 550, image=ImageTk.PhotoImage(app.image1))
        canvas.create_text(1025,470,text=f'Calculated: {app.calculated}',font='Courier 12 bold',fill='black')
    if app.dictionary == True:
        app.calculator = False
        counter = -1
        for value in app.dictDef:
            counter += 1
            dy = 470 + (counter*15)
            dx = 1025
            definition = value
            x = len(value)
            splits = []
            if x>10:
                y = int(x/2)
                while y > 10:
                    y = int(y/2)
                    if y not in splits:
                        splits.append(y)
            counter = 0
            if splits != [ ]:
                print(splits)
                for value in splits:
                    while value.isalnum:
                        value += 1
                        print(value)
                        counter += 1
                        if counter > 5:
                            input()

                    counter += 1
                    print(value)
                    i = int(value)
                    h2 = definition[i:]
                    h1 = definition[:i]
                    h3 = definition[i+x:]
                    h4 = definition[:i+x]
                    h1 += '\n'
                    h4 += '\n'
                    definition = h1 + h2
                    print(definition)
                    if counter > 5:
                        input()





            canvas.create_text(dx,dy,text=f'{definition}',font="Courier 10",fill=fill3)
            canvas.create_rectangle(910,dy-10,1140,dy+10,width=3,outline=fill3)

    if app.focusHours != 0 or app.focusMinutes != 0:
        if app.focusHours < 10:
            if app.focusMinutes <10:
                canvas.create_text(1025, 125, text=f'0{app.focusHours}:0{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(890,75,1145,175, outline = 'orange', width = 4)

            else:
                canvas.create_text(1025, 125, text=f'0{app.focusHours}:{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(900,75,1150,175, outline = 'orange', width = 4)                
        else:

            canvas.create_rectangle(900,75,1150,175, outline = 'orange', width = 4)
            canvas.create_text(1025, 125, text=f'{app.focusHours}:{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
    if app.cuTimer == True:
        if app.focusHours < 10:
            if app.focusMinutes <10:
                canvas.create_text(1025, 125, text=f'0{app.focusHours}:0{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(900,75,1150,175, outline = 'orange', width = 4)

            else:
                canvas.create_text(1025, 125, text=f'0{app.focusHours}:{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(900,75,1150,175, outline = 'orange', width = 4)                
        else:

            canvas.create_rectangle(900,75,1150,175, outline = 'orange', width = 4)
            canvas.create_text(1025, 125, text=f'{app.focusHours}:{app.focusMinutes}:{app.focusSeconds}', font='Courier 30', fill=fill)
    if app.focusTasksOn == True:
        canvas.create_rectangle(50,375,300,425, outline = 'orange', width= 3)
        canvas.create_text(175,400, text = 'add Tasks', font='Courier 20', fill=fill)
        canvas.create_rectangle(50,475,300,525, outline = 'orange', width= 3)
        canvas.create_text(175,500, text = 'set breaks', font='Courier 20', fill=fill)
        weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
        day = weekdayNum
        for row in weekdays:
            if row[0]==day:
                weekday = row[1]
                appMode = row[2]
                counter = 0
                
                counter = -1
                for focusEvents in app.esl:
                    canvas.create_rectangle(430,140,840,700, outline = fill, width=3)
                    counter += 1
                    eventName = focusEvents[0]
                    eventHourEnd = int(focusEvents[1])
                    eventMinEnd = (focusEvents[2])
                    dx = 460
                    dy = 160 + (counter*50)
                    if len(focusEvents)<4: # to do item
                        dx = 460
                        dy = 160 + (counter*50)
                        canvas.create_rectangle(dx,dy,dx+30,dy+30, width = 2,outline=fill)
                        if eventMinEnd <10:
                            
                            canvas.create_text(dx+150,dy+15, text=f'{eventName} due at {eventHourEnd}:0{eventMinEnd}',fill=fill)

                        else:
                            canvas.create_text(dx+150,dy+15, text=f'{eventName} due at {eventHourEnd}:{eventMinEnd}',fill=fill)
                    if len(focusEvents)>3: # event to go to
                        eventHS = int(focusEvents[3])
                        eventMS = int(focusEvents[4])
                        s = str()
                        for value in focusEvents[0]:
                            s += value
                        if 'Break' in s:
                            canvas.create_rectangle(dx+10,dy, dx +330, dy+40,outline='grey', width=2)
                            if eventMinEnd <10:
                                if eventMS <10:
                                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill='grey')
                                else:
                                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill='grey')
                            elif eventMS <10:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:{eventMinEnd}',fill='grey')
                            elif eventMinEnd > 10 and eventMS > 10:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill='grey')

                            else:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill='grey')

                        else:
                            canvas.create_rectangle(dx+10,dy, dx +330, dy+40,outline=fill)
                            if eventMinEnd <10:
                                if eventMS <10:
                                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill=fill)
                                else:
                                    canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:0{eventMinEnd}',fill=fill)
                            elif eventMS <10:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:0{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)
                            elif eventMinEnd > 10 and eventMS > 10:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)

                            else:
                                canvas.create_text(dx+150,dy+20, text=f'{eventName} from {eventHS}:{eventMS} at {eventHourEnd}:{eventMinEnd}',fill=fill)

                    if app.timer == True:
                        fH = app.focusHours
                        fM = app.focusMinutes
                        eventHourEnd
                        eventMinEnd
                        eT = ((eventHourEnd *100)+eventMinEnd)
                        cTH=now.strftime('%H')
                        cTM=now.strftime('%M')
                        cTS=now.strftime('%S')
                        cTH = int(cTH)
                        cTM = int(cTM)
                        cT = ((int(cTH) *100)+int(cTM))
                        cTfH = ((cTH + fH)*100)
                        cTfM = (cTM + fM)
                        while cTfM > 59:
                            cTfM = cTfM - 60
                            cTfH += 100
                        cTF = cTfH+cTfM
                        if cT<eT<cTF:
                            canvas.create_rectangle(dx+365,dy+5,dx+375,dy+35, width=2, fill = 'orange',outline='grey')
import requests
import json

def focusMode_mousePressed(app, event):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    dx = event.x
    dy = event.y
    FRAdx = [[50,300]]
    FRAdy = [[675,725,'mainMenuMode'],[75,125,'focusTimer'],[175,225,'focusTask'],[375,425,'addTasks'],[475,525,'addBreaks'],[575,625,'blankSession']]
    if dx<650:
        for value in FRAdy:
            for value2 in FRAdx:
                if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                    if value[2]=='focusTimer':
                        if app.timer ==True:
                            app.timer=False
                            app.cuTimer = False
                            app.focusHours = 0
                            app.focusMinutes = 0
                            break
                        app.timer = True
                        type = app.getUserInput('Count Down or Count Up?\nPlease type in cd or cu please')
                        if type == '':
                            continue
                        if type =='cd':
                            hoursTotal = int(app.getUserInput('How many hours? If None enter 0'))
                            minutesTotal = int(app.getUserInput('How many minutes? if None enter 0'))
                            app.focusHours = hoursTotal
                            app.focusMinutes = minutesTotal
                        if type =='cu':
                            app.cuTimer = True
                    elif value[2]=='focusTask':  
                        weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
                            [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
                                [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                                    [6,'Sunday',app.sunday]]
                        day = weekdayNum
                        for row in weekdays:
                            if row[0]==day:
                                appMode = row[2]
                        dayAppRead(app, app.username)
                        app.esl = sortedappMode(app, appMode)
                        if app.focusTasksOn == True:
                            app.focusTasksOn = False
                        elif app.focusTasksOn == False:
                            app.focusTasksOn = True
                            
                    
                    elif value[2]=='addTasks':
                        weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
                        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
                            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                                [6,'Sunday',app.sunday]]
                        eventType = app.getUserInput('What type of Event?\n  Types: \n  due date\n  event')
                        if eventType == '':
                            app.showMessage('canceled')
                            break
                        if (eventType == 'study' or eventType == 'event'):
                            eventStartTime = app.getUserInput('What time does the event start?\nin military time please:\nEx: 5 pm == 1700 \n3:00 am == 0300')
                            if eventStartTime == '':
                                app.showMessage('canceled')
                                break
                            if len(eventStartTime)<4:
                                hourStart = eventStartTime[0]
                                minuteStart = eventStartTime[1:3]
                            if len(eventStartTime)>3:
                                hourStart = eventStartTime[0:2]
                                minuteStart = eventStartTime[2:4]
                        endTime = app.getUserInput('What is the end time in military time?\nEx 5 pm == 1700 \n6:15 am == 615')
                        if len(endTime)<4:
                            hourEnd = int(endTime[0])
                            minuteEnd = int(endTime[1:3])
                        if len(endTime)>3:
                            hourEnd = int(endTime[0:2])
                            minuteEnd = int(endTime[2:4])
                        eventName = app.getUserInput('What is the name of this event?')
                        if eventName == '':
                            app.showMessage('canceled')
                            break
                        eventDay = weekdayNum
                        for row in weekdays:
                            if row[0]==eventDay:
                                appMode = row[2]
                                dayAppRead(app, app.username)
                                if eventType == 'event':
                                    appMode.append([eventName,hourEnd, minuteEnd,\
                                        hourStart, minuteStart])
                                    app.esl = sortedappMode(app, appMode)
                                else:
                                    appMode.append([eventName,hourEnd,minuteEnd])
                                    app.esl = sortedappMode(app, appMode)

                    elif value[2]=='addBreaks':
                        dayAppRead(app, app.username)
                        if app.timer == False:
                            app.showMessage('You are Currently not in a timed focus session.\n Joining one, no matter how short, will help plan a better break schedule')
                        else:
                            ammtB =app.getUserInput('How Many Breaks During Session?\nLeave Blank to cancel')
                            if ammtB == '':
                                continue
                            timeB = app.getUserInput('How Long of breaks would you like?')
                            app.breaksList.append([int(ammtB),int(timeB)])

                            addbreaks(app)
                            eventDay = weekdayNum
                            for row in weekdays:
                                if row[0]==eventDay:
                                    appMode = row[2]
                            app.esl = sortedappMode(app, appMode)
                        
                    elif value[2]=='blankSession':
                        app
                    else:
                        app.mode = value[2]
    else:
        FRAdx = [[930,1120]]
        FRAdy = [[250,300,'calculator'],[315,365,'dictionary'],[380,430,'translator']]
        for value in FRAdy:
            for value2 in FRAdx:
                if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                    if value[2]=='dictionary':
                        if app.dictionary == True:
                            app.dictionary = False
                            break
                        else:
                            app_id = "a56dea3e"
                            app_key = "9f94d98774a5fdd378172c12c455ec58"
                            endpoint = "entries"
                            language_code = "en-us"
                            word_id = app.getUserInput('Search a word in the English Dictionary')
                            app.word = word_id
                            fields = 'definitions'
                            strictMatch = 'false'
                            url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower() + '?fields=' + fields + '&strictMatch=' + strictMatch;
                            #https://developer.oxforddictionaries.com/documentation
                            #https://developer.oxforddictionaries.com/documentation/getting_started
                            #Citation for grammar and information on how I learned how to import
                            r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
                            import ast
                            newD = r.text
                            newD = ast.literal_eval(newD)  
                            counter = 0
                            definitions=[]
                            for value in newD:
                                if value == "results":
                                    value1 = newD['results']
                                    value2 = value1[0]
                                    for value3 in value2:
                                        if value3=="lexicalEntries":
                                            value4 = value2[value3]
                                            value5 = value4[0]
                                            for value6 in value5:
                                                if value6=="entries":
                                                    value7=value5[value6]
                                                    value8=value7[0]
                                                    for value9 in value8:
                                                        if value9=="senses":
                                                            value10=value8[value9]
                                                            value11=value10[0]
                                                            for value12 in value11:
                                                                if value12=="definitions":
                                                                    value13=value11[value12]
                                                                    value14=value13[0]
                                                                    print(value)
                                                                    if value14 not in definitions:
                                                                        definitions.append(value14)
                                                                        counter+=1
                            for defapp in definitions:
                                app.showMessage(defapp)

                    elif value[2]=='translator':
                        app_id2 = "a56dea3e"
                        app_key2 = "a689129ad643ca1334d79017af6be23b"
                        language1 = 'en'
                        strictMatch = 'false'
                        #language2 = app.getUserInput('What language?\nenglish=en\nspanish=es')
                        language2 = 'es'
                        word_id2 = app.getUserInput(f'what {language2} word would you like to translate to english?')
                        app.word2 = word_id2

                        url2 = "https://od-api.oxforddictionaries.com:443/api/v2/translations/"+ language2 + "/"  + language1 + "/" + word_id2.lower()
                        r2 = requests.get(url2, headers={"app_id": app_id2, "app_key": app_key2})
                        newD2 = r2.text
                        import ast 
                        counter = 0
                        translations=[]
                        for value in newD2:
                            print(value)
                            if value == "results":
                                value1 = newD2['results']
                                value2 = value1[0]
                                for value3 in value2:
                                    if value3=="lexicalEntries":
                                        value4 = value2[value3]
                                        value5 = value4[0]
                                        #print(value5)
                                        print('5')
                                        for value6 in value5:
                                            if value6=="compounds":
                                                value7=value5[value6]
                                                value8=value7[0]
                                                for value9 in value8:
                                                    if value9=="domains":
                                                        value10=value8[value9]
                                                        value11=value10[0]
                                                        #print(value11)
                                                        print('11')
                                                        for value12 in value11:
                                                            if value12=="text":
                                                                value13=value11[value12]
                                                                value14=value13[0]
                                                                print(value14)
                                                                if value14 not in translations:
                                                                    translations.append(value14)
                                                                    counter+=1
                            for transapp in translations:
                                app.showMessage(transapp)

                    elif value[2]=='calculator':
                        if app.calculator == True:
                            app.calculator = False
                        else:
                            typeMath = int(app.getUserInput('What type of math?\
                                \n1) Add\
                                \n2) Subtract\
                                \n3) Multiply\
                                \n4) Divide\
                                \n Input the number corresponding with the type\
                                \n ie: to add type 1 and enter'))
                            if typeMath == 1:
                                fN = int(app.getUserInput('First number'))
                                sN = int(app.getUserInput('Second number'))
                                x = fN + sN
                                app.calculated = x
                                app.calculator = True
                            elif typeMath == 2:
                                fN = int(app.getUserInput('First number'))
                                sN = int(app.getUserInput('Second number'))
                                x = fN - sN
                                app.calculated = x
                                app.calculator = True
                            elif typeMath == 3:
                                fN = int(app.getUserInput('First number'))
                                sN = int(app.getUserInput('Second number'))
                                x = fN * sN
                                app.calculated = x
                                app.calculator = True
                            elif typeMath == 4:
                                fN = int(app.getUserInput('First number'))
                                sN = int(app.getUserInput('Second number'))
                                x = fN / sN
                                app.calculated = x
                                app.calculator = True
                            app.calculated = round(app.calculated,5)
                            


def focusMode_timerFired(app):
    if app.focusHours != 0 or app.focusMinutes != 0:
        if app.focusSeconds <= 0:
            app.focusSeconds = 59
            app.focusMinutes -= 1
        app.focusSeconds -= 1
        if app.focusMinutes <= 0:
            app.focusHours -= 1
            app.focusMinutes = 59
        if app.focusHours < 0:
            app.focusMinutes = 0
            app.focusSeconds = 0
            app.focusHours = 0
    if app.cuTimer == True:
        app.focusSeconds += 1
        if app.focusSeconds >= 59:
            app.focusSeconds = 0
            app.focusMinutes += 1
        if app.focusMinutes >= 59:
            app.focusHours += 1
            app.focusMinutes = 0


#################################################################################
# Add breaks recursive and other recursive
#################################################################################

def addbreaks(app):
    '''app.breaksList
    app.focusHours 
    app.focusMinutes
    app.esl'''
    from datetime import datetime
    now = datetime.now()
    exactTime = now.strftime('%H:%M:%S')

    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    day = weekdayNum
    for row in weekdays:
        if row[0]==day:
            weekday = row[1]
            appMode = row[2]
            counter = 0
    for events in appMode:
        if appMode.index(events)==0:
            continue
        eventName = events[0]
        eventHourEnd = int(events[1])
        eventMinEnd = int(events[2])
        eventTime = ((int(eventHourEnd)*100)+int(eventMinEnd))
        

        fH = app.focusHours
        fM = app.focusMinutes
        f = ((int(fH)*100)+int(fM))
        
        cTH=now.strftime('%H')
        cTM=now.strftime('%M')
        cTS=now.strftime('%S')
        cT = ((int(cTH)*100)+int(cTM))
        if cT<eventTime<(cT+f):
            app.inSess.append(events) # List of all events that are in sess
        breakadder(app)

################################################################################
# checker
# ex availabilityCheck(app, 'Saturday', 1040,1230) or (app, 'Saturday', 0,2) for event
#################################################################################

def breakadder(app):
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    from datetime import datetime
    now = datetime.now()
    exactTime = now.strftime('%H:%M:%S')
    day = weekdayNum
    for apps in weekdays:
        if apps[0]==day:
            appmode = apps[2]
    eventsNow = app.inSess
    for value in app.breaksList:
        ammtB = value[0]
        timeB = value[1]
    fH = app.focusHours
    fM = app.focusMinutes
    f = ((int(fH)*100)+int(fM))
    
    cTH=int(now.strftime('%H'))
    cTM=int(now.strftime('%M'))
    cTS=int(now.strftime('%S'))
    cT = ((int(cTH)*100)+int(cTM))
    import math
    for breaks in range(ammtB):
        eTH = (fH+cTH)
        eTM = (fM + cTM)
        endtimer_time = int((eTH*100)+eTM)
        
        blocks = roundHalfUp(math.floor((fH/(ammtB+1))*60)+(fM/ammtB))
        breakChecker(app,blocks)
      

def breakChecker(app,blocks):
    count = 0
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    from datetime import datetime
    now = datetime.now()
    exactTime = now.strftime('%H:%M:%S')
    day = weekdayNum
    for apps in weekdays:
        if apps[0]==day:
            appmode = apps[2]
    fH = app.focusHours
    fM = app.focusMinutes
    f = ((int(fH)*100)+int(fM))
    cTH=int(now.strftime('%H'))
    cTM=int(now.strftime('%M'))
    cTS=int(now.strftime('%S'))
    cT = ((int(cTH)*100)+int(cTM))
    for value in app.breaksList:
        ammtB = value[0]
        timeB = value[1]
    for breaks in range(ammtB):
        counter = 0
        if count > ammtB:
            break
        if app.breaks == ammtB:
                break
        for check in range(5):
            if app.breaks == ammtB:
                break
            if counter > 0:
                break
            day = weekdayNum
            sT_min = (blocks*breaks)+(timeB*check)
            if sT_min < 59:
                addB = blocks + sT_min
                if addB > 59:
                    xB = 0
                    while addB > 59:
                        addB = addB - 60
                        xB += 1
                    addBH = xB
                    addBM = addB
                    sH = cTH + addBH
                    sM = cTM + addBM
                    if sM > 59:
                        sM = sM - 60
                        sH += 1
                    startTime = ((int(sH)*100)+int(sM))
                    eM = sM + timeB
                    eH = sH
                    if eM > 59:
                        eM = eM - 60
                        eH += 1
                    endTime = ((int(eH)*100)+int(eM))
                    if availabilityCheck(app,day,startTime,endTime)==True:
                        app.breaks += 1
                        counter += 1
                        count += 1
                        day = weekdayNum
                        for apps in weekdays:
                            if apps[0]==day:
                                appmode = apps[2]
                        eventName = f'{timeB} Minute Break'
                        hourEnd = eH
                        minuteEnd = eM
                        hourStart = sH
                        minuteStart = sM
                        appmode.append([eventName,hourEnd, minuteEnd,\
                                       hourStart, minuteStart])
                
                        #['ECE Class', 21, 30, '20', '30']
                else:
                    addBH = 0
                    addBM = addB
                    sH = cTH + addBH
                    sM = cTM + addBM
                    if sM > 59:
                        sM = sM - 60
                        sH += 1
                    startTime = ((int(sH)*100)+int(sM))
                    eM = sM + timeB
                    eH = sH
                    if eM > 59:
                        eM = eM - 60
                        eH += 1
                    endTime = ((int(eH)*100)+int(eM))
                    if availabilityCheck(app,day,startTime,endTime)==True:
                        app.breaks += 1
                        counter += 1
                        count += 1
                        day = weekdayNum
                        for apps in weekdays:
                            if apps[0]==day:
                                appmode = apps[2]
                        eventName = f'{timeB} Minute Break'
                        hourEnd = eH
                        minuteEnd = eM
                        hourStart = sH
                        minuteStart = sM
                        appmode.append([eventName,hourEnd, minuteEnd,\
                                       hourStart, minuteStart])

            elif sT_min > 59:
                #= (blocks*breaks)+(timeB*check) 
                addB = blocks + sT_min
                if addB > 59:
                    xB = 0
                    while addB > 59:
                        addB = addB - 60
                        xB += 1
                    addBH = xB
                    addBM = addB
                    sH = cTH + addBH
                    sM = cTM + addBM
                    if sM > 59:
                        sM = sM - 60
                        sH += 1
                    startTime = ((int(sH)*100)+int(sM))
                    eM = sM + timeB
                    eH = sH
                    if eM > 59:
                        eM = eM - 60
                        eH += 1
                    endTime = ((int(eH)*100)+int(eM))
                    if availabilityCheck(app,day,startTime,endTime)==True:
                        app.breaks += 1
                        counter += 1
                        count += 1
                        day = weekdayNum
                        for apps in weekdays:
                            if apps[0]==day:
                                appmode = apps[2]
                        eventName = f'{timeB} Minute Break'
                        hourEnd = eH
                        minuteEnd = eM
                        hourStart = sH
                        minuteStart = sM
                        appmode.append([eventName,hourEnd, minuteEnd,\
                                       hourStart, minuteStart])
                
                else:
                    addBH = 0
                    addBM = addB
                    sH = cTH + addBH
                    sM = cTM + addBM
                    if sM > 59:
                        sM = sM - 60
                        sH += 1
                    startTime = ((int(sH)*100)+int(sM))
                    eM = sM + timeB
                    eH = sH
                    if eM > 59:
                        eM = eM - 60
                        eH += 1
                    endTime = ((int(eH)*100)+int(eM))
                    if availabilityCheck(app,day,startTime,endTime)==True:
                        app.breaks += 1
                        counter += 1
                        count += 1
                        day = weekdayNum
                        for apps in weekdays:
                            if apps[0]==day:
                                appmode = apps[2]
                        eventName = f'{timeB} Minute Break'
                        hourEnd = eH
                        minuteEnd = eM
                        hourStart = sH
                        minuteStart = sM
                        appmode.append([eventName,hourEnd, minuteEnd,\
                                       hourStart, minuteStart])

def availabilityCheck(app, day, startTime, endTime):
   # ['15-112 Class', 14, 30, '13', '00'],['ECE Homework', 22, 00]]
   #Recursive backtracking check 
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    if startTime < 1000:
        #830
        sHours = startTime//1000
        sMin = startTime % 100
    if startTime > 999:
        sHours = startTime//100
        sMin = startTime % 100
    if endTime < 1000:
        #830
        eHours = endTime//1000
        eMin = endTime % 100
    if endTime > 999:
        eHours = endTime//100
        eMin = endTime % 100
    day = weekdayNum
    for apps in weekdays:
        if apps[0]==day:
            appmode = apps[2]
            for events in appmode:
                if appmode.index(events)==0:
                    continue
                if len(events)<4:
                    currEH = int(events[1])
                    currEM = int(events[2])
                    if startTime == 0:
                        if ((currEH * 100)+currEM) == ((eHours * 100)+eMin):
                            x = ['impDueDateD']
                            return ['impDueDateD']
                    if startTime != 0:
                        if ((sHours * 100)+sMin) <= ((currEH * 100)+currEM) <= ((eHours * 100)+eMin):
                            x = ['impDueDateE']
                            return ['impDueDateE']
                                # checks if my event or due date is able to fit in a due date

                if len(events)>3: #event now
                    currSH = int(events[3])
                    currSM = int(events[4])
                    currEH = int(events[1])
                    currEM = int(events[2])
                    if startTime == 0: # due date
                        if ((currSH *100)+currSM)<((eHours * 100)+eMin)<((currEH * 100)+currEM):
                            x = ['impEventD']
                            return ['impEventD']
                    if startTime != 0:
                        # my break event eH and eM is after cSH and crSM but before currEH and currEM
                        # my sH and sM is after cSH and CRM but before currEH and currEH
                        if ((currSH *100)+currSM)<((eHours * 100)+eMin)<((currEH * 100)+currEM):
                            x = ['impEventE']
                            return ['impEventE']
                        if ((currSH *100)+currSM)<((sHours * 100)+sMin)<((currEH * 100)+currEM):
                           x = ['impEventE']
                           return ['impEventE']
            else:
                return True
    

###############################################################################
# Recursive scheduler
###############################################################################
def sortedappMode(app, appMode):
    eventsNum = len(appMode)-1
    esl = sorted2dCreate(eventsNum)
    appMode = appMode[1:]
    solver(app, esl, 0, appMode)
    return esl

def solver(app, esl, eventNum, appMode):
    if eventNum > len(appMode)-1:
        return esl
    else:
        event = appMode[eventNum]
        for row in range(len(esl)):
            if islegalAdd(app, esl, row, eventNum, appMode):
                esl[row]=event
                solution = solver(app, esl, eventNum+1, appMode)
                if (solution != None):
                    return solution
                esl[row]=[0]
        return None

def islegalAdd(app, esl, row, eventNum, appMode):
    if esl[row]!=[0]:
        return False
    event = appMode[eventNum]
    if len(event)>3:
        currSH = int(event[3])
        currSM = int(event[4])
    currEH = int(event[1])
    currEM = int(event[2])
    if (row==0 and esl[row]==[0]):
        return True
    else:
        if row==0:
            return False
        if len(esl)>1:
            for value in esl:
                if value == [0]:
                    break
                if esl.index(value)>row:
                    break
                if esl.index(value)<row:
                    vEH = value[1]
                    vEM = value[2]
                if vEH == currEH:
                    if vEM>currEM:
                        return False
                else:
                    if vEH>currEH:
                        return False
        firstE = esl[row-1]
        if firstE==[0]:
            return True
        feEH = firstE[1]
        feEM = firstE[2]
        if feEH == currEH:
            if feEM>currEM:
                return False
            elif feEM<currEM:
                return True
        else:
            if feEH>currEH:
                return False
            else:
                return True
def sorted2dCreate(eventsNum):
    return [[0]*1 for events in range(eventsNum)]

##############################################################################
# Vibes
##############################################################################
def relaxMode_redrawAll(app,canvas):
    fill = 'black'
    fill2 = 'blue'
    if app.night_Mode == True:
        fill ='white'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_text(app.width/2, 30, text='Relaxation and Breaks', font='Courier 26',fill='light blue')
    canvas.create_rectangle(1000,700,1150,750, outline=fill, width=2)
    canvas.create_text(1075,725, text='Main Menu', font = 'Courier 14', fill = fill)
    #canvas.create_text(app.width/2,100, text='Under Construction! Come back soon!',font='Courier 30',fill='orange')
    canvas.create_rectangle(30,200,300,300,outline=fill2, width= 3)
    canvas.create_text(165, 250, text='Focused Breathing', font='Courier 18', fill=fill2)
    canvas.create_text(165,450,text='Draw',font='Courier 18', fill=fill2)
    canvas.create_rectangle(30,400,300,500, outline=fill2,width=3)
    
def relaxMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    FRAdx = [[30,300],[1025,1125]]
    FRAdy = [[700,750,'mainMenuMode'],[200,300,'breathMode'],[400,500,'drawMode']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                    app.mode = value[2]
##############################################################################
# Draw Mode
##############################################################################
def drawMode_redrawAll(app,canvas):
    fill = 'black'
    fill2 = 'grey'
    fill3='light grey'
    if app.night_Mode == True:
        fill ='white'
        fill2 = 'black'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_rectangle(20,20,860,760,outline='grey',fill=app.canvasColor,width=5)
    canvas.create_rectangle(1000,675,1150,725, outline=fill3, width=2)
    canvas.create_text(1075,700, text='back', font = 'Courier 14',fill=fill)
    canvas.create_rectangle(900,100,1175,545,outline=fill,fill='white',width=3)
    canvas.create_rectangle(905,105,1170,540,outline='black',width=2)
    
    canvas.create_rectangle(920,120,1155,150, outline = fill2,width=2)
    canvas.create_text(1037,135,text='Line',font='Courier 10', fill=fill2)
    
    canvas.create_rectangle(920,160,1155,190, outline = fill2,width=2)
    canvas.create_text(1037,175,text='Rectangle',font='Courier 10', fill=fill2)
    
    canvas.create_rectangle(920,200,1155,230, outline = fill2,width=2)
    canvas.create_text(1037,215,text='Oval',font='Courier 10', fill=fill2)


    canvas.create_rectangle(920,440,1155,470, outline = fill2,width=2)
    canvas.create_text(1037,455,text='Change Color',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,240,1155,270, outline = fill2,width=2)
    canvas.create_text(1037,255,text='Add Fill',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,280,1155,310, outline = fill2,width=2)
    canvas.create_text(1037,295,text='delete Drawings',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,320,1155,350, outline = fill2,width=2)
    canvas.create_text(1037,335,text='delete last line',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,360,1155,390, outline = fill2,width=2)
    canvas.create_text(1037,375,text='delete last rectangle',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,400,1155,430, outline = fill2,width=2)
    canvas.create_text(1037,415,text='delete last Oval',font='Courier 10', fill=fill2)
    canvas.create_rectangle(920,480,1155,510, outline = fill2,width=2)
    canvas.create_text(1037,495,text='change Canvas Color',font='Courier 10', fill=fill2)


    for drawlines in app.lines:
        dLX = drawlines[0]
        dLY = drawlines[1]
        dFX=drawlines[2]
        dFY=drawlines[3]
        canvas.create_line(dLX,dLY,dFX,dFY,width=2,fill=app.color)
    for drawrectangle in app.rectangles:
        dLX = drawrectangle[0]
        dLY = drawrectangle[1]
        dFX= drawrectangle[2]
        dFY= drawrectangle[3]
        if app.fillColor == '0':
            canvas.create_rectangle(dLX,dLY,dFX,dFY,width=2,outline=app.color)
        else:
            canvas.create_rectangle(dLX,dLY,dFX,dFY,width=2,outline=app.color,fill=app.fillColor)
    for drawOval in app.ovals:
        dLX = drawOval[0]
        dLY = drawOval[1]
        dFX= drawOval[2]
        dFY= drawOval[3]
        if app.fillColor == '0':
            print('oval?')
            canvas.create_oval(dLX,dLY,dFX,dFY,width=2,outline=app.color)
        else:
            print('oval?')
            canvas.create_oval(dLX,dLY,dFX,dFY,width=2,outline=app.color,fill=app.fillColor)

def drawMode_mousePressed(app,event):
    dx = event.x
    dy = event.y
    if 900<dx<1200:
        FRAdx = [[1025,1125],[920,1155]]
        FRAdy = [[675,725,'relaxMode'],[120,150,'drawLine'],[160,190,'drawRectangle'],[200,230,'drawOval'],[240,270,'addFill'],[280,310,'delAll'],[360,390,'delR'],[320,350,'delL'],[400,430,'delO'],[440,470,'changeColor'],[480,510,'canvasC']]
        for value in FRAdy:
            for value2 in FRAdx:
                if (value[0]<dy<value[1] and value2[0]<dx<value2[1]):
                    if value[2]=='changeColor':
                        color = app.getUserInput('What color?')
                        app.color = color
                        break
                    elif value[2]=='delR':
                        vr = app.rectangles[-1]
                        app.rectangles.remove(vr)
                        break
                    elif value[2]=='delO':
                        vo = app.ovals[-1]
                        app.ovals.remove(vo)
                        break
                    elif value[2]=='delAll':
                        app.rectangles = []
                        app.lines = []
                        break
                    elif value[2]=='canvasC':
                        app.canvasColor = app.getUserInput('What color would you like the canvas on the left?')
                        break
                    elif value[2]=='delL':
                        vl = app.lines[-1]
                        app.lines.remove(vl)
                        break
                    elif value[2]=='addFill':
                        app.fillColor = app.getUserInput('What color would you like your fill?')
                        break
                    elif value[2]=='drawOval':
                        print('hello')
                        app.drawLine = False
                        app.drawRectangle = False
                        if app.drawOvals != True:
                            print('true')
                            app.drawOvals = True
                            app.drawCounter = 0
                        else:
                            print('false')
                            app.drawOvals = False
                            app.drawCounter = 0
                        break
                    elif value[2]=='drawLine':
                        app.drawRectangle = False
                        app.drawOvals = False
                        if app.drawLine == True:
                            app.drawLine = False
                            app.drawCounter = 0
                        else:
                            app.drawLine = True
                        break
                    elif value[2]=='drawRectangle':
                        app.drawLine = False
                        app.drawOvals = False
                        if app.drawLine == True:
                            app.drawLine = False
                        else:
                            app.drawRectangle = True
                        break
                    else:
                        app.mode = value[2]

    else:
        if app.drawLine==True:
            app.drawRectangle = False
            app.drawOvals = False
            if app.drawCounter ==0:
                app.dLX = dx
                app.dLY = dy
            elif app.drawCounter ==1:
                app.dFX = dx
                app.dFY = dy
            app.drawCounter += 1
            if app.drawCounter == 2:
                app.lines.append([app.dLX,app.dLY,app.dFX,app.dFY])
                app.drawCounter = 0
        elif app.drawRectangle==True:
            app.drawLine = False
            app.drawOvals = False
            if app.drawCounter ==0:
                app.dLX = dx
                app.dLY = dy
            elif app.drawCounter ==1:
                app.dFX = dx
                app.dFY = dy
            app.drawCounter += 1
            if app.drawCounter == 2:
                app.rectangles.append([app.dLX,app.dLY,app.dFX,app.dFY])
                app.drawCounter = 0
        elif app.drawOvals == True:
            app.drawLine = False
            app.drawRectangle = False
            if app.drawCounter==0:
                app.dLX = dx
                app.dLY = dy
            elif app.drawCounter==1:
                app.dFX = dx
                app.dFY = dy
            app.drawCounter += 1
            if app.drawCounter == 2:
                app.ovals.append([app.dLX,app.dLY,app.dFX,app.dFY])
                app.drawCounter = 0

##############################################################################
# MeditationMode
##############################################################################
def meditationMode_redrawAll(app,canvas):
    fill = 'grey'
    fill2 = 'blue'
    fill3 = 'black'
    if app.night_Mode == True:
        fill3 = 'white'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_rectangle(1000,675,1150,725, outline=fill3, width=2)
    canvas.create_text(1075,700, text='back', font = 'Courier 14', fill = fill)
    canvas.create_text(app.width//2,50,text='Meditation')
    canvas.create_rectangle(30,100,300,200,outline=fill2,width=2)
    canvas.create_text(165,150,text='Search for Video',fill=fill2,font='Carrier 16')
def meditationMode_mousePressed(app,event):
    dx = event.x
    dy = event.y
    a = app.width//2
    ac = 300
    ar = int(app.breathRadius)
    FRAdx = [[30,300],[1000,1150]]
    FRAdy = [[675,725,'relaxMode']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                if value[2]=='inB':
                    app.breathing = True
                else:
                    app.mode = value[2]
##############################################################################
# focused breathing
##############################################################################

def breathMode_redrawAll(app,canvas):
    fill = 'grey'
    fill2 = 'light blue'
    fill3 = 'black'
    fill4 = 'green'
    if app.night_Mode == True:
        fill3 = 'white'
        fill4 = 'dark green'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_rectangle(1000,700,1150,750, outline=fill, width=2)
    canvas.create_text(1075,725, text='back', font = 'Courier 14', fill = fill)
    canvas.create_rectangle(1000,625,1150,675, outline=fill4, width=2)
    canvas.create_text(1075,650, text='Breath Settings', font = 'Courier 14', fill = fill4)
    canvas.create_text(app.width/2, 50, text='Focused Breathing',fill=fill2, font='Courier 26')
    canvas.create_rectangle(1000, 550, 1150, 600, outline=fill2, width=2)
    canvas.create_text(1075,575, text='Display Information', font='Courier 12', fill=fill2)
    canvas.create_rectangle(1000, 475, 1150, 525, outline='blue', width=2)
    canvas.create_text(1075,500, text='breath Timer', font='Courier 12', fill='blue')

    cx = app.width//2
    cy = 300
    r = int(app.breathRadius)
    if app.breathing == True or app.breathingOut == True or app.breathHold==True:
        if app.breathing == True:
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,outline=fill,width=2, fill='blue')
        elif app.breathingOut == True:
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,outline=fill,width=2, fill='blue')
        elif app.breathHold == True:
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,outline=fill,width=2, fill='blue')
    cx = app.width//2
    cy = 300
    r = 100
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,outline=fill,width=2, fill='light blue')
    if app.breathing == True or app.breathingOut == True or app.breathHold==True:
        if app.breathing == True:
            canvas.create_text(app.width//2,300,text='Breath In',font='Courier 10')
        elif app.breathingOut == True:
            canvas.create_text(app.width//2,300,text='Breath Out',font='Courier 10')
        elif app.breathHold == True:
            canvas.create_text(app.width//2,300,text='Hold',font='Courier 15')
    if app.breathSolved == False:
        if app.longestB != 0 and app.breathRadius < app.longestB:
            x = int(app.longestB)
            canvas.create_oval(cx-x,cy-x,cx+x,cy+x, outline = 'orange', width=2)
    if app.breathSolved == True:
        x = int(app.breathS)
        canvas.create_oval(cx-x,cy-x,cx+x,cy+x, outline = 'orange', width=2)
    if app.display == True:
        canvas.create_rectangle(15,200,400,500, outline=fill3,width=3,fill='grey')
        canvas.create_text(245,350,text='Welcome to Focused Breathing.\
            \n\nBreath In: Click and Hold\
            \nBreath Out: Release Button\
            \nHold: Hold exhale, settings can be changed\
            \n\nAfter 5 breaths, the system will calibrate\
            \nA new calibrated circle will be generated\
            \nThis is your goal circle now\
            \nTo change, change in settings',font='Courier 14',fill=fill2)
    if (app.fastBreath == True and (app.breathingOut==True or app.breathHold ==True)):
        canvas.create_text(app.width//2,600,text='breathe in slower...',fill='red',font='Courier 20')
    if app.btimer == True:
        if app.bMinutes <10:
            if app.bSeconds <10:
                canvas.create_text(1025, 125, text=f'0{app.bMinutes}:0{app.bSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(910,90,1125,160, outline = 'blue', width = 4)
            else:
                canvas.create_text(1025, 125, text=f'0{app.bMinutes}:{app.bSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(910,90,1125,160, outline = 'blue', width = 4)

        else:
            if app.bSeconds <10:
                canvas.create_text(1025, 125, text=f'{app.bMinutes}:0{app.bSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(910,90,1125,160, outline = 'blue', width = 4)
            else:
                canvas.create_text(1025, 125, text=f'{app.bMinutes}:{app.bSeconds}', font='Courier 30', fill=fill)
                canvas.create_rectangle(910,90,1125,160, outline = 'blue', width = 4)                


def breathMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    a = app.width//2
    ac = 300
    ar = int(app.breathRadius)
    FRAdx = [[30,300],[1000,1150],[a-ar,a+ar]]
    FRAdy = [[700,750,'relaxMode'],[550,600,'display'],[625,675,'breathS'],[ac-ar,ac+ar,'inB'],[475,525,'bTimer']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                if value[2]=='inB':
                    app.breathing = True
                    break
                elif value[2]=='bTimer':
                    if app.btimer == True:
                        app.btimer = False
                        app.bHours = 0
                        app.bMinutes = 0
                    else:
                        minutesTotal = int(app.getUserInput('How many minutes? if None enter 0'))
                        if minutesTotal == '':
                            continue
                        secondsTotal = int(app.getUserInput('How many seconds? if None enter 0'))
                        if minutesTotal == '':
                            continue
                        app.bSeconds = secondsTotal
                        app.bMinutes = minutesTotal
                        app.btimer = True
                elif value[2]=='display':
                    if app.display == True:
                        app.display = False
                    else:
                        app.display = True
                    break
                elif value[2]=='breathS':
                    app.holds = app.getUserInput('How Long would you like to hold for in seconds?')
                    circleYN = app.getUserInput('Would you like to change the goal circle (in orange)? (yes/no)')
                    if circleYN == ('yes' or 'Yes'):
                        app.breathS = app.getUserInput(f'Your circle is currently:{app.breathS}\
                            \n input a similar value to test, and change at will')
                    if circleYN ==('no'or 'No'):
                        break
                else:
                    app.mode = value[2]
                    break

    
def breathMode_mouseReleased(app, event):
    dx = event.x
    dy = event.y
    a = app.width//2
    ac = 300
    ar = int(app.breathRadius) - 5
    FRAdx = [[a-ar,a+ar]]
    FRAdy = [[ac-ar,ac+ar,'inB']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                if app.breathRadius >= app.longestB:
                    app.longestB = app.breathRadius
                app.breathing = False
                app.breathHold = True
                if len(app.endBs) < 5:
                    app.endBs.append(app.breathRadius)
                if len(app.endBs) > 4:
                    endBs(app)
                    app.breathSolved = True

def breathMode_timerFired(app):
    if app.bMinutes >= 0:
        if app.bSeconds <= 0:
            app.bSeconds = 59
            app.bMinutes -= 1
        app.bSeconds -= 1
        if app.bMinutes < 0:
            app.btimer = False
            app.bSeconds = 0
    if app.flashing ==True:
        app.flashing = False
    elif app.flashing ==False:
        app.flashing = True
    if app.breathing == True:
        app.breathRadius += 5
    elif app.breathingOut == True:
        app.breathRadius -= 5
    elif app.breathHold == True:
        app.holdCounter += 1
        if app.holdCounter == app.holds:
            app.breathHold = False
            app.breathingOut = True
            app.holdCounter = 0
    if app.breathRadius < 110:
        app.breathingOut = False
    if app.longestB < 115:
        app.fastBreath = True
    if app.longestB > 115:
        app.fastBreath = False

def endBs(app):
    endBs = app.endBs
    z = len(endBs)
    L = 0
    for value in endBs:
        L += int(value)
    app.breathS = L//z


    
##############################################################################
# Adventure
##############################################################################
def adventureMode_redrawAll(app,canvas):
    fill = 'black'
    fill1 = 'grey'
    if app.night_Mode == True:
        fill ='white'
        fill1 ='dark grey'
        canvas.create_rectangle(0,0,1200,800,fill='black')
    canvas.create_text(app.width/2, 30, text='Adventure Search Results', font='Courier 26',fill='green')
    canvas.create_rectangle(1000,650,1150,750, outline=fill, width=3)
    canvas.create_text(1075,700, text='Main Menu', font = 'Courier 10 bold', fill = fill)
    count = -1
    canvas.create_rectangle(30,100,1170,500, outline=fill, width=3)
    canvas.create_text(app.width//2,75,text='Only Currently Open Place Will Show', font='Courier 10',fill=fill1)
    for value in app.places_return['results']:
        nameTitle = value['name']
        font = 'Courier 10 bold'
        font2 = 'Courier 10'
        if len(nameTitle)> 40:
            font = 'Courier 8 bold'
            continue
        count += 1
        dx = 200
        if count > 3:
            dx = 600
        if count > 7:
            dx = 1000
        if count > 11:
            break
        Vicinity = value['vicinity']
        if count > 3:
            dy = 150 + ((count%4)*50)
        else:
            dy = 150 + (count*50)
        canvas.create_text(dx, dy, text=f'{nameTitle}',\
             font = font, fill = fill) 
        canvas.create_text(dx, dy+15, text=f'Address:{Vicinity}',\
             font = font2, fill = fill) 

def adventureMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    FRAdx = [[30,300],[1000,1150]]
    FRAdy = [[650,750,'mainMenuMode']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                app.mode = value[2]

##############################################################################
# Settings
##############################################################################
def settingsMode_redrawAll(app,canvas):
    fill = 'black'
    if app.night_Mode == True:
        canvas.create_rectangle(0,0,1200,800,fill='black')
        fill ='white'
    canvas.create_text(app.width/2, 30, text='Settings and Preferences', font='Courier 26',fill=fill)
    canvas.create_rectangle(620,700,770,750, outline=fill, width=5)
    canvas.create_text(695,725, text='Main Menu', font = 'Courier 20 bold', fill = fill)
    canvas.create_rectangle(30, 500, 300, 550, outline=fill,width=5)
    canvas.create_text(170,525, text='Adventure Location', font = 'Courier 20', fill =fill)
    canvas.create_rectangle(30, 300, 300, 350, outline=fill,width=5)
    canvas.create_text(170,325, text='Night Mode', font = 'Courier 20', fill =fill)
    

def settingsMode_mousePressed(app, event):
    dx = event.x
    dy = event.y
    FRAdx = [[30,300],[620,770]]
    FRAdy = [[165,175,'NeuroDivergentDiagnosis'],[300,350,'night_Mode'],[700,750,'mainMenuMode'],[500,550, 'AdventureLocation']]
    for value in FRAdy:
        for value2 in FRAdx:
            if value[0]<dy<value[1] and value2[0]<dx<value2[1]:
                    if value[2]=='AdventureLocation':
                        location = app.getUserInput('Input the coordinates of your destination, ex: CMUs input location= 40.443322,-79.943583 ')
                        app.location = str(location)
                    elif value[2]=='night_Mode':
                        if app.night_Mode == False:
                            app.night_Mode = True
                        elif app.night_Mode == True:
                            app.night_Mode = False
                    else:
                        app.mode = value[2]

##############################################################################
# Key/Mouse Pressed
##############################################################################
def screen_keyPressed(app, event):
    if (event.key == 'd'):
        app.mode == 'mainMenuMode'



##############################################################################
#  App
##############################################################################
def appStarted(app):
    app.places_return = None
    app.username = ''
    app.password = ''
    app.monday = [0]
    app.tuesday = [1]
    app.wednesday = [2]
    app.thursday = [3]
    app.friday = [4]
    app.saturday = [5]
    app.sunday = [6]
    app.image1 = app.loadImage('calculator.png')
    app.image1 = app.scaleImage(app.image1, 9/18)
    app.calculator = False
    app.calculated = 0
    weekdays = [[0,'Monday', app.monday],[1,'Tuesday',app.tuesday],\
        [2,'Wednesday',app.wednesday],[3,'Thursday',app.thursday],\
            [4,'Friday',app.friday],[5,'Saturday',app.saturday],\
                [6,'Sunday',app.sunday]]
    app.focusHours = 0
    app.focusMinutes = 0
    app.focusSeconds = 0
    app.timerDelay = 1000
    app.timer = False
    app.bHours = 0
    app.bMinutes = 0
    app.bSeconds = 0
    app.btimer = False
    app.location = '40.443322,-79.943583'
    app.focusTasksOn = False
    app.tasksList = []
    app.breaksList = []
    app.definitions = []
    app.cuTimer = False
    day = weekdayNum
    for list in weekdays:
        if list[0]==day:
            appMode = list[2]
    app.esl = sortedappMode(app, appMode)
    app.inSess = []
    app.addBreaks = False
    app.missedDates = []
    app.pastDue = False
    app.show = False
    app.commonMiss = []
    app.commonMissing = False
    app.breaks = 0
    app.night_Mode = False
    app.breathing = False
    app.breathingOut = False
    app.drawLine = False
    app.drawRectangle = False
    app.drawOvals = False
    app.drawCounter = 0
    app.breathRadius = 105
    app.longestB = 0
    app.fastBreath = False
    app.dLX = 0
    app.dLY = 0
    app.dFX = 0
    app.dFY = 0
    app.lines = []
    app.rectangles=[]
    app.ovals = []
    app.display = False
    app.dictionary = False
    app.dictDef = []
    app.fillColor = '0'
    app.color = 'white'
    app.canvasColor = 'white'
    if app.night_Mode==True:
        app.canvasColor = 'black'
    if len(app.missedDates)>0:
        app.pastDue = True
    app.mode = 'logInMode'
    app.breathHold = False
    app.holds = 2
    app.holdCounter = 0
    app.flashing = False
    app.endBs = []
    app.breathSolved = False
    app.breathS = 0


    app.word = ''
    app.word2 = ''
    app.dictionary = False
runApp(width=1200, height=800)

