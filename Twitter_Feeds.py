#!/usr/bin/python

from datetime import datetime, timedelta
import os
import sys
import re
import twitter

def GenerateFeeds(name, api, n):
	# Try to get the maximum count
	statuses = api.GetUserTimeline(screen_name=name, count=200)

	user_feeds = []
	for status in statuses:
		info = {}
		site_url = ""
		if len(status.urls) > 0 :
			site_url = status.urls[0].expanded_url
		info = {"created":status.created_at, "title":status.text, "url":site_url}
		user_feeds.append(info)

	# process the generated feeds
	ProcessFeeds(name, user_feeds, n)

def ProcessFeeds(name, user_feeds, n):
	# we need to handle IST here, Since tweeter will return 
	n = 5.5 + n
	d = 0
	if n > 12:
		n = n/12
		d = n%12
	_time = datetime.now() + timedelta(hours=-n, days=-d)

	for feed in user_feeds:
		# convert feed time to datetime object
		feedtime = datetime.strptime(feed['created'], "%a %b %d %H:%M:%S +%f %Y")

		if feedtime > _time:

			# Get the time from created date information
			time = int(feed['created'][11:13])
			
			# Extract the date from created_at
			filedate = feed['created'][4:10] + " " + feed['created'][-4:]

			# generate the file and create the folder
			filepath = name + "/" + filedate
			MakeFolder(filepath)
		
			# Get the title of the article
			title = feed['title'].encode('utf-8').strip()

			# Create the filename based on the title
			_name = re.sub('[#<>$!%&*\'\"{}?/:\@ \|\.\,]', ' ', title[:20])
			_name = re.sub('\s+', ' ', _name)
			filename = filepath + "/" + _name + ".txt"
		
			# open the file and write the content
			fo = open(filename, "a")
			fo.write("Title:\n")
			fo.write(feed['title'].encode('utf-8').strip())
			fo.write("\n\nContent URL:\n")
			fo.write(feed['url'])
			
			# close the file object
			fo.close()

# helper function to create the new file
def MakeFolder(filepath):
	if not os.path.exists(filepath):
		try:
			os.makedirs(filepath)
		except OSError:
			print "Unable to create file : ",filepath
			sys.exit()

def main():
	# CONSUMER_KEY and CONSUMER_SECRET
	CONSUMER_KEY = <YOUR_CONSUMER_KEY>
	CONSUMER_SECRET = <YOUR_CONSUMER_SECRET>

	# ACCESS_TOKEN and ACCESS_TOKEN_SECRET
	ACCESS_TOKEN = <YOUR_ACCESS_TOKEN>
	ACCESS_TOKEN_SECRET = <YOUR_ACCESS_TOKEN_SECRET>

	# connect to twitter api
	api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
	users = ['NewIndianXpress', 'thehindu']

	# Get the N from user
	hours = input("Please enter the N : ")
	for user in users:
		GenerateFeeds(user, api, hours)

if __name__ == "__main__":
	main()