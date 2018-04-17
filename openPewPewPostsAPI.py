#!flask/bin/python
from flask import Flask, jsonify, make_response, request
from flask import request
import sqlite3

app = Flask(__name__)

# ----------------------------------------------------------------
# DATABASE
# ----------------------------------------------------------------	
pathToDb = "C:/Users/13069/Documents/openPewPewPosts/posts.db"

def connectDb():
	conn = sqlite3.connect(pathToDb)
	c = conn.cursor()
	return [conn,c]

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
	[conn, c] = connectDb()
	c.execute("INSERT INTO posts VALUES(?,?,?)",(int(userId),str(content),int(timestamp)))
	if(closeDb(conn, c)==True):
		print("Correctly closed the DB")
	else:
		print("Error while closing the DB")
	return True

# Get all posts from the posts table
def getPostsFromDb():
	[conn, c] = connectDb()
	posts = c.execute("select * from posts")
	postList=[]
	jsonResponse = {'payload':[]}
	
	for post in posts:
		postInfo = {
			'userId':post[0],
			'content':post[1],
			'timestamp':post[2],
		}
		postList.append(postInfo)
	
	for element in postList:
		jsonResponse['payload'].append(element)
	
	closeDb(conn,c)
	return jsonResponse
		
# ----------------------------------------------------------------
# GET
# ----------------------------------------------------------------

@app.route('/posts',methods=['GET'])
def getPosts():
	jsonResponse = getPostsFromDb()
	return jsonify(jsonResponse),200

@app.route('/posts/<int:post_id>',methods=['GET'])
def getPost(post_id):
	return 'Return the post: '+str(post_id)	

# ----------------------------------------------------------------
# POST
# ----------------------------------------------------------------	
	
# Creating a new POST
@app.route('/posts',methods=['POST'])
def postPost():
	if (not request.json or
	not 'userId' in request.json['payload'] or
	not 'content' in request.json['payload'] or
	not 'timestamp' in request.json['payload']):
		jsonResponse = {
			'payload': 'Wrong payload',
		}
		return jsonify(jsonResponse),400
	else:
		check = addPostToDb(request.json['payload']['userId'],request.json['payload']['content'],request.json['payload']['timestamp'])
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

# Main script
if __name__ == '__main__':
	app.run(debug=True)
	closeDb(conn,c)