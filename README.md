A simple terminal program built for one of my classes. Time constraints limited the scope to two functions from the Twitter API.  

One method will search all recent tweets for a given term. This will display tweets with some extra information. It can be helpful for gathering intelligence. The additional metadata can help distinguish real people from the bots. It is up to the user to determine the credibility of any information that they find.  

The second method takes input for a twitter account handle and the number of tweets to sample. It will then provide a simple statistical analysis of the tweet engagement.  

***Update 2022-02-15***: There is now a new feature to search a Twitter user by account name. Some extra metadata is provided.

Future additions could implement more functions from the API. For example, a method that gathers a stream of tweets of a certain topic and then exports the data to a database or a JSON file.  
A possible feature could be to automate commenting and other forms of engagement.  

Add your own Twitter developer keys to the keys.py file to use it.  
Create a project with a main.py and keys.py file and copy this code over.  
pip install all of the required dependencies.  
  
  
Here are a few screenshots of the current version:  

![Options Menu](https://i.imgur.com/1sk3z4C.png)

![Searching Recent Tweets](https://i.imgur.com/7bt9ljc.png)

![Account Engagement](https://i.imgur.com/aY3yT3Q.png)

![Search_User](https://i.imgur.com/9zCIpPE.png)
