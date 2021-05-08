import requests
import smtplib
from datetime import date,datetime
import time

# Function to send an email with the appointment details 'appt' as input. 

def send_mail(appt, email, apppassword):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(email, apppassword)   # Get 2FA and a app-specific password for Gmail
    
    subject = 'Vaccine Appointment available near you!'
    if "No Appointments found" in appt:
        body = appt + "\nHang in there buddy! I will notify you as soon as I find free slots : )"
    else:
        body = "Hey, Hurry Up! I found some vaccine appointments near you!\n\n"+appt
    
    msg = f"Subject : {subject} \n\n {body}"
    
    server.sendmail('vidhibansal004@gmail.com', email, msg)
    
    print(" Hey! E-Mail has been sent!")
    server.quit()
    
## Specify Pincode before running

def AppointmentCheck():
    pincode = input("Enter the PINCODE: ")
    email = input("Enter your Email-ID to receive notification: ")
    appPassword = input("Enter your App Password: ")

    today = date.today()
    current_date = today.strftime("%d-%m-%Y")   ##Gets todays Date

    now = datetime.now()
    current_time = now.strftime("%I:%M %p")  ##Gets Current time of checking

    ## CoWIN API
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="+pincode+"&date="+current_date
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print ("Error!")
    else:
        data = response.json()
        centers = data['centers']   #Gets all the vaccination centers and their corresponding details
        
        if len(centers) == 0:
            msg = "No Appointments found in the next 7 days from " + current_date + ": Last Checked: "+ current_time
            print(msg)
            send_mail(msg, email, appPassword)
        
        else:
            res = {}
            for center in centers:
                a = center['name'] + f" ({center['fee_type']})"
                b = []
                for session in center['sessions']:
                    b.append(str(f"{session['date']} // Age Limit :{session['min_age_limit']} // Capacity : {session['available_capacity']}"))
                    res[a] = b
            
            send = ''
            for center,data in res.items():
                send += ("\n"+center+"\n\n")
                for dates in data:
                    send += str(dates+"\n")

            # Sends email with the details
            send_mail(send, email, appPassword)
            
            print("Found Vaccination Dates! Exiting..")
            exit()


print("COVID-19 Vaccination Appointment Checker\n")
while(True):
    AppointmentCheck()
    time.sleep(60*30)()
