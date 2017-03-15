
from datetime import datetime
import time
import os
import random
from random import randint
from flask import Flask, jsonify, request, session, g, redirect, url_for, abort,make_response,render_template, flash
#from flask_mysqldb MySQL

import modules.db_connector as db
from modules.urlSafety import *

from modules.universalDbObject import UniversalDbObject as dbObj


import unicodedata
from base64 import b64encode
#Used for flashing html code
from flask import Markup


app = Flask(__name__)
app.secret_key = 'KJFdjashuf_!)#"!?::;hlufahuhdfijiH((!/(/?)(WDF)?)I=RU9jofa9+3nv2r)!/((/=)!5aoq__:wjmfabsr910'

@app.route('/')
def index():
	
	return "Root dir"


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        con,cur = db.connect()
        try:	
	    userID = request.form['id']
    	    try:
	        cur.execute("""SELECT * FROM d0020e.users WHERE userID=%s""",(str(userID),))
	        data = cur.fetchone()
	        if data!=None:
	            if data[4]!=1:
	                return "{'success':0, 'error':'User is not activated!'}"
	    	    return "{'success':1, 'error':'None', 'userID':"+str(data[0])+", 'name':'"+data[1]+"', 'lastname':'"+data[2]+"', 'socialSecurityNr':"+str(data[3])+"}"
		else:
	    	    return "{'success':0, 'error':'User not found!'}"
    	    except:
	        return "No data recieved from the database!"
        except:
	    return "Invalid userID!"
    except:
	return "Database connection could not ge established!"

@app.route('/gettasktest', methods=['GET', 'POST'])
def gettasktest():
	if 1==1:
	#try:
		userID=request.form['userID']
		result = gettaskfromuser(userID)
		taskid = str(result[0])
		if result == "error":
			return "{'success':'0','message':'user has no task!'}"
		con, cur = db.connect()
		cur.execute("""SELECT title, description, taskID, areaID, checklistID FROM d0020e.task WHERE taskID=%s""",(str(taskid),))
		data1 = cur.fetchone()
		types=equipmentDetails(data1[4])

		result = "{'title':'"+data1[0]+"', 'description':'"+data1[1]+" \n\n You need this kind of equipment \n -"+types.title()+"','taskID':'"+str(data1[2])+"','area':'"+str(getarea(data1[3]))+"'"
		cur.execute("""SELECT subtasktitle, subtaskdescription, imagesrc, subtaskID, status FROM d0020e.subtasks WHERE taskID=%s ORDER BY subtaskID ASC""",(str(taskid),))
		data = cur.fetchone()
		i=0
		while data is not None:
			result+=",'subtasktitle"+str(i)+"':'"+data[0]+"','subtaskdescription"+str(i)+"':'"+data[1]+"','imagesrc"+str(i)+"':'"+str(data[2])+"','subtaskID"+str(i)+"':'"+str(data[3])+"','subtaskstatus"+str(i)+"':'"+str(data[4])+"'"

			data = cur.fetchone()			
			i=i+1
		result+=",'amountofsubtasks':'"+str(cur.rowcount)+"'}"
		
		return result
		
	#except:
		#return "error"

#
#	Help method to print all the equipment to description above.
#
def equipmentDetails(checklistID):
	con, cur = db.connect()
	cur.execute("""SELECT type FROM d0020e.checklist WHERE checklistID = %s""",(str(checklistID),))
	types = cur.fetchall()
	return str(types[0][0].replace("-", "\n -"))

#	A help funtion that returns the x, y, z cordinates along with width, depth and height given a areaID
#
#	Working!
#
def getarea(area):
	con, cur = db.connect()
	cur.execute("""SELECT x, y, z, width, depth, height FROM d0020e.area WHERE areaID = %s""",(str(area),))
	cordinates = cur.fetchall()
	return cordinates[0]

#	A funtion to check if a user is in a work area or not. Should send an alarm if the user is outside the area.
#
#	In progress...
#
@app.route('/issafe', methods=['GET', 'POST'])
def issafe():
	userID = request.form['userID']
	pos=simpos(userID)
	area=getarea(userID)
	#if (area[0] < pos[0]) & ( pos[0] < area[3]):
	#	return "TEST Pos: "+str(pos[0])+" and limit: "+str(area[0])+", "+str(area[3])+"."
	#else:
	#	return "FALSE Pos: "+str(pos[0])+" and limit: "+str(area[0])+", "+str(area[3])+"."
	if not (area[0] <= pos[0] <= area[3]) & (area[1] <= pos[1] <= area[4]) & (area[2] <= pos[2] <= area[5]):
		return "{'success':'1','message':'ALERT! User is outside the area!','pos':'"+str(pos)+"','area':'"+str(area)+"','alert':'1'}"
	else:
		return "{'success':'1','message':'All is good!','pos':'"+str(pos)+"','area':'"+str(area)+"','alert':'0'}"


def gettaskfromuser(userID):
	try:
		con, cur = db.connect()
		cur.execute("""SELECT taskID from d0020e.task where userID =  %s """,(str(userID),))
		taskID = cur.fetchall()
		return taskID[0]
	except:
		return "error"

#A funtion (and dir) to update the status of a subtask.
#
#	Working!
#
@app.route('/updatesubtask', methods=['GET', 'POST'])
def updatesubtask():
        subtaskID=request.form['subtaskID']
        taskID=request.form['taskID']

        con, cur = db.connect()
        try:
                cur.execute("""SELECT status, taskID FROM d0020e.subtasks WHERE subtaskID=%s""",(str(subtaskID),))
                isDone = cur.fetchone()
                if (str(isDone[0]) == str(0)) &  (str(isDone[1]) == str(taskID)):
			cur.execute("""UPDATE d0020e.subtasks SET status = %s WHERE subtaskID = %s AND taskID = %s""",(str(1), str(subtaskID), str(taskID),))
                        con.commit()
			return "{'success':'1','message':'"+str(check_task(taskID))+"'}"
                elif (str(isDone[0]) == str(1)) &  (str(isDone[1]) == str(taskID)):
                        cur.execute("""UPDATE d0020e.subtasks SET status = %s WHERE subtaskID = %s AND taskID = %s""",(str(0), str(subtaskID), str(taskID),))
                        con.commit()
			return "{'success':'1','message':'"+str(revert_task(taskID))+"'}"

                else:
                        return "No subtask matches that taskID"

        except:
                return "error"

#A funtion to check if all subtasks are completed. If so, set taskID.status to complete.
#
#	WORKING!
#
def check_task(taskID):
        con, cur = db.connect()
	try:
		cur.execute("""select subtaskID, status from subtasks where taskID = %s""",(str(taskID),))
		subtaskarray = cur.fetchall()
		i=len(subtaskarray)
		o=0
		numberOfCompletedSubtasks =0
		while o < i:
			if str(subtaskarray[o][1]) != str(1):
				return "Not all tasks are completed!"
			else:
				o+=1
				numberOfCompletedSubtasks+=1
		if numberOfCompletedSubtasks == i:
			cur.execute("""UPDATE d0020e.task SET status = 1 WHERE taskID = %s""",(str(taskID),))
			con.commit()
			return "Task completed! Good job!"
		else:
			return "Subtask completed!"

	except:
		return "Error getting subtaskID while checking taskID!"

#A short function to set status of a task to 0
#
#	WORKING!
#
def revert_task(taskID):
	con, cur = db.connect()
	try:
		cur.execute("""UPDATE d0020e.task SET status = 0 where taskID = %s""",(str(taskID),))
		con.commit()
		return "Task un-completed!"
	except:
		return "No such taskID!"


@app.route('/getequipment', methods=['GET', 'POST'])
def getequipment():
	MAC=request.form['MAC']
	con, cur = db.connect()
	try:
		cur.execute("""SELECT type, macAddress, takenBy FROM d0020e.equipment WHERE macAddress = %s""",(str(MAC),))
		data = cur.fetchone()
		if data is not None:
			result="{'type':'"+data[0]+"', 'MAC':'"+data[1]+"','note':'match','takenBy':'"+str(data[2])+"'}"
			return result
		else:
			return "{'note':'nomatch'}"
	except:
		return "error"

#
#	Toggels the boolean value 'takenBy' where MAC == macAddress
#
@app.route('/updateequipment', methods=['GET', 'POST'])
def updateequipment():	
	MAC=request.form['MAC']
	userID=request.form['userID']
	try:	
		con, cur = db.connect()
		# Check if equipment is in use
		cur.execute("""SELECT takenBy from d0020e.equipment WHERE macAddress = %s""",(str(MAC),))		
		status = str(cur.fetchone())
		if status == "("+str(userID)+",)":
			cur.execute("""UPDATE d0020e.equipment SET takenBy = 0 WHERE macAddress = %s""",(str(MAC),))
			con.commit()
			return "{'success':'1','message':'Device un-paired!'}"
	
		elif status[1] == str(0):
			cur.execute("""UPDATE d0020e.equipment SET takenBy = %s WHERE macAddress = %s""",(str(userID), str(MAC),))
			con.commit()
			return "{'success':'1','message':'Device paired!'}"
		else:
			return "{'success':'0','message':'The user does not have any device paired or invalid macAddress!'}"
	except:
			return "{'success':'1','message':'Error updating the equipment!'}"


#
#	Returns the pos in X, Y and Z (in that order). If no data is found the response will respond accordingly.
#
@app.route('/getpos', methods=['GET', 'POST'])
def getpos():
	userID=request.form['userID']
	try:
		con, cur = db.connect()
		cur.execute("""SELECT currentX, currentY, currentZ FROM d0020e.position WHERE userID = %s""",(str(userID),))
		pos=cur.fetchall()
		if pos == []: #If the user does not have any data:
			return "{'success':'0','message':'no data for user "+str(userID)+"'}"
		return "{'success':'1','pos':'"+str(pos[0])+"'}"
	except:
		return "{'success':'0','message':'Could not fetch data from the database!'}"
	

#
#	simulates movement of pos for a user. X = (1, 2048), Y = (1, 2048), Z = (1, 255).
#
def simpos(userID):
	if 1==1:
	#try:
		con, cur = db.connect()
		cur.execute("""SELECT currentX, currentY, currentZ FROM d0020e.position WHERE userID = %s""",(str(userID),))
		pos=cur.fetchall()
		if pos == []: #If the user does not have any data:
			return "-1"
		newpos=[0,0,0]
		newpos[0]=(randint(1,2048))
		newpos[1]=(randint(1,2048))
		newpos[2]=(randint(1,70))
		return newpos
		#return "("+str(newpos[0])+", "+str(newpos[1])+", "+str(newpos[2])+")"
	#except:
	#	return "-1"


@app.route('/getchecklist', methods=['GET', 'POST'])
def getchecklist():
	taskID=request.form['taskID']
	try:
		con, cur = db.connect()
		cur.execute("""SELECT type FROM d0020e.checklist WHERE checklistID=(SELECT checklistID FROM d0020e.task WHERE taskID=%s)""", (str(taskID),))
		result=cur.fetchone()
		return "{'success':'1', 'type':'"+result[0]+"'}"
	except:
		return "{'success':'0', 'type':'None'}"
@app.route('/getequipped', methods=['GET', 'POST'])
def getequipped():
	userID=request.form['userID']
	try:
		con, cur = db.connect()
		cur.execute("""SELECT type FROM d0020e.equipment WHERE takenBy=%s""", (str(userID),))
		result=cur.fetchone()
		equipment="{'success':'1'"
		i = 0
		while result is not None:
			equipment+=",'type"+str(i)+"':'"+result[0]+"'"
			i+=1
			result=cur.fetchone()
		equipment+=", 'totalitems':'"+str(i)+"'}"
		return equipment
	except:
		return "{'success':'0'}"

