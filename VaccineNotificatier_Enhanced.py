# COVID-19 Vaccination Appointment Tracker (03/05/2021)
# A Python script that tracks vaccination appoints for the next 7 days for a specific pincode using the CoWin API
# Most of the libraries are inbuilt but the user needs to install the 'requests' library

# with <3 by Adarsh Parameswaran, Kozhikode,Kerala

import requests
import smtplib
from datetime import date,datetime
import time

# Function to send an email with the appointment details 'appt' as input. 

pin = input("Enter pin Code: ")
email = input("Enter Email: ")
passcode = input("Enter Passcode: ")


def send_mail_vidhi(appt):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(email, passcode)   # Get 2FA and a app-specific password for Gmail
    
    subject = 'Vaccine Appointment available near you!'
    if "No Appointments found" in appt:
        body = "Hey! I coudn't find any appointments near you!\n"+appt
    else:
        body = "Hey! I found some vaccine appointments near you!\n"+appt
    
    msg = f"Subject : {subject} \n\n {body}"
    
    server.sendmail(email, email, msg)
    
    print(" Hey! E-Mail has been sent!")
    server.quit()


def send_mail_papa(appt):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('dhirajragrawal@gmail.com','rakmtihoppepskct')   # Get 2FA and a app-specific password for Gmail
    
    subject = 'Vaccine Appointment available near you!'
    if "No Appointments found" in appt:
        body = "Hey! I coudn't find any appointments near you!\n"+appt
    else:
        body = "Hey! I found some vaccine appointments near you!\n"+appt
    
    msg = f"Subject : {subject} \n\n {body}"
    
    server.sendmail('vidhibansal004@gmail.com','dhirajragrawal@gmail.com',msg)
    
    print(" Hey! E-Mail has been sent!")
    server.quit() 
## Specify Pincode before running

def AppointmentCheck():

    today = date.today()
    current_date = today.strftime("%d-%m-%Y")   ##Gets todays Date

    now = datetime.now()
    current_time = now.strftime("%I:%M %p")  ##Gets Current time of checking

    ## CoWIN API
    # pincode = input("Enter. your Pin Code: ")
    # email = input("Enter your Email-ID to receive notification: ")
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pin+"&date="+current_date
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print ("Error!")
    else:
        data = response.json()
        centers = data['centers']   #Gets all the vaccination centers and their corresponding details
        
        if len(centers) == 0:
            print("No Appointments found in the next 7 days from {} : Last Check {}".format(current_date, current_time))
            # send_mail("No Appointments found in the next 7 days from " + current_date + ": Last Checked: "+ current_time)
        
        else:
            res = {}
            capacity = 0
            for center in centers:
                a = center['name'] + f" ({center['fee_type']})"
                b = []
                for session in center['sessions']:
                    
                    b.append(str(f"{session['date']} // Age Limit :{session['min_age_limit']} // Capacity : {session['available_capacity']}"))
                    capacity = session['available_capacity']
                    res[a] = b
            
            a = ''
            for center,data in res.items():
                a += ("\n"+center+"\n\n")
                for dates in data:
                    a += str(dates+"\n")

            #Sends the appointment details via telegram
            # requests.get(f"https://api.telegram.org/YOUR_TELEGRAM_BOT_ID/sendMessage?chat_id=YOUR_CHAT_ID&text={a}")
            
            # Sends email with the details
            print(a)
            if capacity > 0:
                print("Found Vaccination Dates!")
                send_mail_vidhi(a)
                send_mail_papa(a)
            
            # exit()


print("COVID-19 Vaccination Appointment Checker\n")
while(True):
    AppointmentCheck()
    time.sleep(60)
