import requests as r
import json, datetime
from twilio.rest import Client

with open("creds.json") as creds_json:
	creds = json.load(creds_json)

def main():
	username = creds["github_username"]
	send_text(check_commits_today(username))


def check_commits_today(username):
	today = datetime.datetime.today().strftime('%Y-%m-%d')
	commit_count_today = commit_count_for_date(username,today)
	if commit_count_today == 0:
		return("No commits today mate... WTF!?!")
	else:
		return("Keep up the good work today mate!")


def commit_count_for_date(username,search_date):
	url = "https://api.github.com/search/commits?q=author:%s+author-date:%s" %(username, search_date)
 	headers = {'Accept': 'application/vnd.github.cloak-preview'}
	github_search = r.get(url, headers=headers)
	print(type(github_search.content))
	daily_commit_count = github_search.json()["total_count"]
	return daily_commit_count


def send_text(message):
	sid = creds["sid"]
	auth_token = creds["twilio_auth_token"]
	client = Client(sid, auth_token)
	message = client.api.account.messages.create(
		to=creds["cell_phone"],
		from_=creds["twilio_number"],
		body=message)
	print(message.Status)


main()
