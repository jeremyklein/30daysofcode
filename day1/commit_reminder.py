import requests as r
import json, datetime
from pytz import timezone
from twilio.rest import Client
from bs4 import BeautifulSoup

with open("creds.json") as creds_json:
	creds = json.load(creds_json)

def main():
	username = creds["github_username"]
	# send_text(check_commits_today(username))
	check_commit_streak_today(username)

def check_commits_today(username):
	tz = timezone('EST')
	today = datetime.datetime.now(tz).strftime('%Y-%m-%d')
	commit_count_today = commit_count_for_date(username,today)
	if commit_count_today == 0:
		return("No commits today mate... WTF!?!")
	else:
		return("Keep up the good work today mate!")

def check_commit_streak_today(username):
	tz = timezone('EST')
	today = datetime.datetime.now(tz).strftime('%Y-%m-%d')	
	commit_streak = commit_streak_for_date(username,today)
	print(commit_streak) 

def commit_count_for_date(username,search_date):
	# scrape the github page, and check commit streak display
	url = "https://github.com/%s" % username
	response = r.get(url)
	html_doc = response.content
	soup = BeautifulSoup(html_doc, 'html.parser')
	rectangles = soup.find_all('rect')
	for rectangle in rectangles:
		if rectangle['data-date'] == search_date:
			return int(rectangle['data-count'])


def commit_streak_for_date(username,search_date):
	# scrape the github page, and check commit streak display
	url = "https://github.com/%s" % username
	response = r.get(url)
	html_doc = response.content
	soup = BeautifulSoup(html_doc, 'html.parser')
	rectangles = soup.find_all('rect')
	streak = 0
	for rectangle in rectangles:
		if int(rectangle['data-count']) > 0:
			streak += 1
		else:
			if rectangle['data-date'] == search_date:
				return streak	
			else:
				streak = 0


def send_text(message):
	sid = creds["sid"]
	auth_token = creds["twilio_auth_token"]
	client = Client(sid, auth_token)
	message = client.api.account.messages.create(
		to=creds["cell_phone"],
		from_=creds["twilio_number"],
		body=message)


main()
