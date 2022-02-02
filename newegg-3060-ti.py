import sys,requests, smtplib, config, smtpConfig
from email.mime.text import MIMEText
from notifypy import Notify
from playsound import playsound
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread
from datetime import datetime
from email.mime.multipart import MIMEMultipart


if len(sys.argv) == 2:
    try:
        priceLimit = int(sys.argv[1])
    except:
        sys.exit(f"\n🛑  Something went wrong. Correct usage is:\npython3 {sys.argv[0]} [integer price limit]\n")
elif len(sys.argv) == 1:
    priceLimit = 600
else:
    sys.exit("\n🛑  Incorrect usage. Correct usage is:\n'python3 {sys.argv[0]} [integer price limit]'\n")

print(f"\n🔵  Checking Newegg for RTX 3060 Ti graphics cards with a price limit of ${priceLimit}.\n  Press CTRL + C to exit.\n")

numLoops = 0
numDealsSeen = 0
url = 'https://www.newegg.com/p/pl?N=100007709%204131%20601359415&PageSize=96&Order=1'

def getItems():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    containers = soup.find_all("div", class_="item-container")
    return containers

def checkPrices(items):
    deals = []
    for item in items:
        try:
            stringPrice = item.find("li", class_="price-current").find("strong").text
            intPrice = stringPrice.replace(",", "")
            intPrice = int(intPrice)
            if(intPrice <= priceLimit):
                nameTag = item.find("div", class_="item-info").find("a", class_="item-title")
                itemName = nameTag.text
                itemLink = nameTag.get("href")
                dealItem = {
                    "price": "$" + stringPrice,
                    "name": itemName,
                    "href": itemLink
                }
                deals.append(dealItem)
        except:
            pass
    return deals

def notify():
    notification = Notify()
    notification.title = "Found 3060 Ti in stock!"
    notification.message = "Check your terminal!"
    notification.send()
    playsound(config.notificationSoundFile)

def sendEmail(subject, msg):
    message = MIMEMultipart("alternative")
    message["To"] = smtpConfig.recipientEmail
    message["From"] = smtpConfig.senderEmail
    message["Subject"] = subject

    htmlMsg = f' <html> <body> {msg} </body> </html> '

    message.attach(MIMEText(msg, 'plain'))
    message.attach(MIMEText(htmlMsg, 'html'))

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(smtpConfig.senderEmail, smtpConfig.senderPassword)
    smtp.sendmail(smtpConfig.senderEmail, smtpConfig.recipientEmail, message.as_string())
    smtp.quit()

while True:
    try:
        items = getItems()
        deals = checkPrices(items)

        if len(deals) > 0:
            date = datetime.now()
            timestamp = date.strftime("%d-%b-%Y (%H:%M:%S)")
            consoleMessage = f"🕑  {timestamp}\n\n"
            msg = f"<h1>Found something for you!</h1><h3>{timestamp}</h3>"
            numDealsSeen += len(deals)
            for deal in deals:
                consoleMessage += f"💵  {deal['price']}  (shipping not incl.)\n🎮  {deal['name'][:75]}\n🔗  {deal['href']}\n\n"
                msg += f"💵 <strong>Price:</strong>  {deal['price']}  (shipping not incl.)<br>🎮 <strong>Product</strong>:  {deal['name'][:75]}<br>🔗 <strong>Link</strong>:  {deal['href']}<br><br>"
            msg += f"<hr> <p>This email was generated and sent by a script. Visit <a href='https://github.com/rosspayn3/newegg-tracker'>https://github.com/rosspayn3/newegg-tracker</a> for more information.</p>"
            print(consoleMessage)
            notifyThread = Thread(target=notify, daemon=True)
            notifyThread.start()
            emailThread = Thread(target=sendEmail("Found a deal!", msg), daemon=True)
            emailThread.start()

        numLoops += 1
        print(f"\n============ Total checks: {numLoops}  |  Total 3060 Ti deals seen: {numDealsSeen} ============")
        print(f"                         Press CTRL + C to exit.")
        sleep(config.sleepDuration)
    except KeyboardInterrupt:
        sys.exit("\n🛑 Price checker killed.")
