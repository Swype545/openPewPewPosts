# ECAM Project : OpenPewPew
## Posts micro-services
This micro-services manage the "Posts" API.

This micro-services is part of the global project "OpenPewPew" constituted by those sub-projects:
* [Comments micro-service (openPewPewComments)](https://github.com/remytms/openPewPewComments)
* [Posts micro-service (openPewPewPosts)](https://github.com/Swype545/openPewPewPosts)
* Users micro-service [(openPiouPiouAuthService)](https://github.com/HadrienCools/openPiouPiouAuthService) (Yes, he's different, as usually)
* UI (openPewPewUI)

## Use the API
There are 7 differents API call you can use with the "Posts" API:

There are the GET calls
* GET /posts : Return all posts from the database
* GET /posts/postId : Return the post with the id "postId"
* GET /users/userId/posts : Return all posts of the user "userId"
* GET /users/userId/posts/last : Return the last post of the user "userId"
* GET /user/posts : Return all the post of the user calling the API
* GET /user/posts/last : Return the last post of the user calling the API

the JSON structure of the response is the following:
{
	"payload": [
		{
			"content":"myContent" (str),
			"id":id (int),
			"timestamp": timestamp (int),
			"userid": userId (int)
		},
		...
	]
}


There is the POST call
* POST /posts : Post a new post in the database

The JSON structure of the POST /posts is the following:
{
	"payload":{
		"content":"myContent" (str)
	}
}





