#!flask/bin/python
from flask import Flask
import sqlite3

app = Flask(__name__)

# ----------------------------------------------------------------
# GET
# ----------------------------------------------------------------

@app.route('/posts',methods=['GET'])
def getPosts():
	return 'Return a list of POST'

@app.route('/post/<int:post_id>',methods=['GET'])
def getPost(post_id):
	return 'Return the post: '+str(post_id)	

# ----------------------------------------------------------------
# GET
# ----------------------------------------------------------------	
	
@app.route('/post',methods=['POST'])
def postPost():
	return 'You sent a POST'
	

	
if __name__ == '__main__':
	app.run(debug=True)