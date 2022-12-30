import requests
import datetime
import time
import smtplib

def check_location():
    my_latitude = "YOUR_LATITUE"
    my_longitude = "YOUR_LONGTITUDE"
    
    iss_location = requests.get(url='http://api.open-notify.org/iss-now.json').json()['iss_position']
    iss_lat = float(iss_location['latitude'])
    iss_lgn = float(iss_location['longitude'])
    
    if my_latitude -5 <= iss_lat <= my_latitude + 5 and my_longitude -5 <= iss_lgn <= my_longitude +5:
        print('You are currently in a good location to see ISS!')
        return True
    else:
        print('You are out of scope.')
        return False
    
def check_time():
    my_latitude = 42.126339
    my_longitude = -70.916420
    
    parameters = {
    'lat':my_latitude,
    'lng':my_longitude,
    'formatted': 0
    }
    
    response = requests.get(url='https://api.sunrise-sunset.org/json',params=parameters)
    response.status_code
    
    # time here is based on UTC. You need to convert it to your local time.
    sunrise_time = response.json()['results']['sunrise'].split('T')[1].split(':')[0]
    sunset_time = response.json()['results']['sunset'].split('T')[1].split(':')[0]
    
    time_now = datetime.datetime.now()
    
    print(f"Sunrise time is {int(sunrise_time)-5}")
    print(f"Sunset time is {int(sunset_time)-5}")
    print(f"Current time is {time_now.hour}")
    
    if int(time_now.hour)< int(sunrise_time)-5 or int(time_now.hour) > int(sunset_time)-5:
        print("It's dark right now.")
        return True
    else:
        print("It's daytime now.")
        return False

# If the ISS is close to my current location and it is currently dark, 
# then send me an email to tell me to look up
# Bonus: run the code every 60 seconds

while True:
    if check_location() and check_time():
        print("It's the right time and location to look up!")
        connection = smtplib.SMTP("YOUR_EMAIL_SMTP_ADDRESS")
        connection.starttls()
        connection.login("YOUR_EMAIL_ADDRESS","YOUR_EMAIL_PASSWORD")
        connection.sendmail(
            from_addr = "XXX",
            to_addr = "XXX",
            msg = "Subject: Look Up\n\nThe ISS is above you in the sky."
        )
    else:
        print("ISS is out of scope or time!")
    
    time.sleep(60)
