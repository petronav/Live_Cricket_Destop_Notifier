from pycricbuzz import Cricbuzz
from gi.repository import Notify, GdkPixbuf
import requests
from bs4 import BeautifulSoup
import time

def call_pycricbuzz_get_id():
	c = Cricbuzz()
	matches = c.matches()
	for match in matches:
		if match['mchstate'] == 'inprogress':
			#match_status = match['status']
			if match['team1']['name'].lower()=='india' or match['team2']['name'].lower()=='india':
				match_id = match['id']
				return match_id

id_ = call_pycricbuzz_get_id()

def CricApp(summary, body):
	Notify.init('Automated Scoreboard')
	notf = Notify.Notification.new(summary, body)
	image = GdkPixbuf.Pixbuf.new_from_file("cric.png")
	notf.set_icon_from_pixbuf(image)
	notf.set_image_from_pixbuf(image)
	notf.show()


def get_ball_status(match_id, prev_ball):
	last_ball = None
	if last_ball != prev_ball:
		url = f'https://www.cricbuzz.com/live-cricket-scores/{match_id}/'
		r = requests.get(url)
		while r.status_code != 200:
			r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		all_over_balls = soup.find_all('div', {"class": ['cb-mat-mnu-wrp', 'cb-ovr-num', 'ng-binding', 'ng-scope']} )
		last_ball = all_over_balls[0]
		current_over = last_ball.text
		print(current_over)
		all_commentaries = soup.find_all('p', {'class' : ['cb-com-ln', 'ng-binding', 'ng-scope', 'cb-col', 'cb-col-90']})
		last_ball_commentary = all_commentaries[0].text
		print(last_ball_commentary)
		current_status_div = soup.find_all('div', class_='cb-text-inprogress')
		current_status = current_status_div[0].text
		print(current_status)
		body_message = current_over + " " + last_ball_commentary
		CricApp(current_status, body_message)
		return last_ball

def main(): 
    try:
        lb = ''
        while True:
            lb = get_ball_status(id_, lb)
            time.sleep(900)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
	main()