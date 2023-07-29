import requests
import config

url = "https://api-football-v1.p.rapidapi.com/v3/odds"

querystring = {"date": "2023-07-23","league":"479","season":"2023"}

headers = {
	"X-RapidAPI-Key": config.API_KEY,
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.request("GET",url, headers=headers, params=querystring).json()

home_odds = response['response'][0]['bookmakers'][0]['bets'][0]['values'][0]['odd']
away_odds = response['response'][0]['bookmakers'][0]['bets'][0]['values'][2]['odd']

print("Home team odds: " + home_odds)



## mls = 253 - 479
## US = USA 
## querystring = {"league":"253","season":"2023","date":"2023-07-15"}

## start with some EURO leauges and MLS Canadian soccer too 
## have it show the daily games show just the win lose draw odds 
## to do that you have to figure out how many games there are a day 
## then figure out when they start
## work on just making one or two of the games show up first then work on updating with current games 
## if we are not past the starting time and we can get odds on the game it will show up as available 
## probably need to touch up on for loops to help that run as well as figure out how to have the website update when i click it "update odds"
