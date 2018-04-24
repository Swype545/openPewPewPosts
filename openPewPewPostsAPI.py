#!flask/bin/python
from flask import Flask, jsonify, make_response, request
from flask import request

import sqlite3
import time
import jwt

app = Flask(__name__)

# ----------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------	
pathToDb = "C:/Users/13069/Documents/openPewPewPosts/posts.db"

def connectDb():
	try:
		conn = sqlite3.connect(pathToDb)
		c = conn.cursor()
		return [conn,c]
	except:
		return False

def closeDb(conn, c):
	try:
		conn.commit()
		conn.close()
		return True
	except:
		return False

def createPostsTable():
	try:
		c.execute('''CREATE TABLE posts (user integer, content text, date integer)''')
		return True
	except:
		return False
		

# Create a post in the posts table
def addPostToDb(userId, content, timestamp):
	try: 
		[conn, c] = connectDb()
		
		# Specify the column necessary because there is an ID
		c.execute("INSERT INTO posts(user,content,date) VALUES(?,?,?)",(int(userId),str(content),int(timestamp)))
		if(closeDb(conn, c)==True):
			print("Correctly closed the DB")
		else:
			print("Error while closing the DB")
		return True
	except:
		return False

# Get all posts from the posts table
# If a userId is defined, return all posts of this user

def getPostsFromDb(userId=0):
	try: 
		[conn, c] = connectDb()
		postList=[]
		
		if(userId == 0): 
			posts = c.execute("select * from posts")
		else:
			posts = c.execute("select * from posts WHERE posts.user IS ?",(userId,))
			
		
		jsonResponse = {'payload':[]}
		
		for post in posts:
			print(post)
			postInfo = {
				'id':post[0],
				'userId':post[1],
				'content':post[2],
				'timestamp':post[3],
			}
			postList.append(postInfo)
		
		for element in postList:
			jsonResponse['payload'].append(element)
		
		closeDb(conn,c)
		return jsonResponse
	except:
		return False
	
def getPostFromDb(userId=None, postId=None):
	try: 
		[conn, c] = connectDb()
		postList=[]
		jsonResponse = {'payload':[]}
		
		# If both of them are defined, we send an error
		
		if(userId is not None and postId is "last"):
			posts = c.execute("select * from posts WHERE posts.user IS ? ORDER BY date DESC LIMIT 1",(int(userId),))
		elif(userId is None and postId is not None):
			posts = c.execute("select * from posts WHERE posts.id IS ?",(int(postId),))
		elif(userId is None and postId is None):
			return False	
		elif(userId is not None and postId is None):
			return False
		else:
			posts=[]
		
		for post in posts:
			# posts[0] is id, 1 is userId, 2 is content and 3 is timestamp
			postInfo = {
				'id': post[0],
				'userId':post[1],
				'content':post[2],
				'timestamp':post[3],
			}
			postList.append(postInfo)
		
		for element in postList:
			jsonResponse['payload'].append(element)
		
		closeDb(conn,c)
		
		return jsonResponse
	except:
		return False
		
# ----------------------------------------------------------------
# GET
# ----------------------------------------------------------------

@app.route('/posts',methods=['GET'])
def getPosts():
	jsonResponse = getPostsFromDb()
	
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200
	
@app.route('/posts/<int:postId>',methods=['GET'])
def getPost(postId):
	jsonResponse = getPostFromDb(postId=postId)
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200
	
@app.route('/users/<int:userId>/posts',methods=['GET'])
def getUserPosts(userId):
	jsonResponse = getPostsFromDb(userId)
	
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200

@app.route('/users/<int:userId>/posts/last',methods=['GET'])
def getlastPost(userId):
	jsonResponse = getPostFromDb(userId=userId, postId="last")
	
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200
	
@app.route('/user/posts',methods=['GET'])
def getMyPosts():
	# This need to be changed with the TOKEN
	myId = "13069"
	jsonResponse = getPostsFromDb(myId)
	
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200

@app.route('/user/posts/last',methods=['GET'])
def getMyLastPost():
	# This need to be changed with the TOKEN
	myId = "13069"
	jsonResponse = getPostFromDb(userId=myId, postId="last")
	
	if(jsonResponse == False):
		return jsonify("{}"),500
	else:
		return jsonify(jsonResponse),200

# ----------------------------------------------------------------
# POST
# ----------------------------------------------------------------	
	
# Creating a new POST
@app.route('/posts',methods=['POST'])
def postPost():
	
	# We don't expect timestamp, we'll generate it
	# We don't need the user, it is in the token
	
	# This need to be changed with the TOKEN
	myId = "13069"
	if (not request.json or
	not 'content' in request.json['payload']):
		jsonResponse = {
			'payload': 'Wrong payload',
		}
		return jsonify(jsonResponse),400
	else:
		check = addPostToDb(int(myId),request.json['payload']['content'],int(time.time()))
		if(check == True):
			jsonResponse = {
				'payload': 'Correctly created the post',
			}
			return jsonify(jsonResponse), 200
		else:
			jsonResponse = {
				'payload': 'error while inserting in DB',
			}
			return jsonify(jsonResponse), 500
	return 404

# ----------------------------------------------------------------
# TOKEN GESTURE
# ----------------------------------------------------------------
def tokenToId(token):
	secretKey = "secret"
	
# Main script
if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')
	# app.run(debug=True)
	closeDb(conn,c)