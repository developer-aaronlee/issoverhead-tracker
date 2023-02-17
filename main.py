import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 38.846226 # Your latitude
MY_LONG = -77.306374 # Your longitude

#Your position is within +5 or -5 degrees of the ISS position.

def iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if abs(MY_LAT - iss_latitude) < 5 and abs(MY_LONG - iss_longitude) < 5:
        return True
    else:
        return False

def in_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    current_hour = time_now.hour

    if sunset <= current_hour <= sunrise:
        return True
    else:
        return False


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

my_email = "pythonautomationapp@gmail.com"
password = "dxabiogqxlleamrw"

while True:
    time.sleep(60)
    if iss_above() and in_dark():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="automation.python@yahoo.com",
                                msg="Subject: Look Up\n\nISS is above in the sky.")

