import requests
import telegram.ext
import datetime as dt
from bs4 import BeautifulSoup


url = ''
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
my_token = ''
userID = ''


def send(msg, chat_id, token=my_token):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)


parent = soup.find('table', {'class': 'tg'}).find_all('tr')
today = parent[1].find_all('td')

date = dt.datetime.strptime(today[0].text, '%m/%d/%Y')
date = date + dt.timedelta(days=1)
date = date.strftime("%m/%d/%Y")
change = today[1].text
value = today[2].text
middle = change[0]

if middle == '-':
    middle = 'will drop {} to {}'.format(change[1:], value)
elif middle == '+':
    middle = 'will rise {} to {}'.format(change[1:], value)
else:
    middle = 'wont change and stay at {}'.format(value)

msg = 'The price of gas on {} {}'.format(date, middle)
send(msg, userID)
