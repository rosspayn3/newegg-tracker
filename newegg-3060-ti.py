import sys
import requests, lxml
from notifypy import Notify
from playsound import playsound
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread
import config


if len(sys.argv) == 2:
    try:
        priceLimit = int(sys.argv[1])
    except:
        sys.exit(f"\n🛑 Something went wrong. Correct usage is:\npython3 {sys.argv[0]} [integer price limit]\n")
elif len(sys.argv) == 1:
    priceLimit = 600
else:
    sys.exit("\n🛑 Incorrect usage. Correct usage is:\n'python3 {sys.argv[0]} [integer price limit]'\n")

print(f"\n🔵 Checking Newegg for RTX 3060 Ti graphics cards with a price limit of ${priceLimit}.\nPress CTRL + C to exit.\n")

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
        # get price from item
        stringPrice = item.find("li", class_="price-current").find("strong").text
        # remove comma
        intPrice = stringPrice.replace(",", "")
        intPrice = int(intPrice)
        # check if price less than limit
        if(intPrice <= priceLimit):
            # add custom item to deals found
            nameTag = item.find("div", class_="item-info").find("a", class_="item-title")
            itemName = nameTag.text
            itemLink = nameTag.get("href")
            dealItem = {
                "price": "$" + stringPrice,
                "name": itemName,
                "href": itemLink
            }
            deals.append(dealItem)
    return deals

def notify():
    notification = Notify()
    notification.title = "Found 3060 Ti in stock!"
    notification.message = "Check your terminal!"
    notification.send()
    playsound(config.notificationSoundFile)

while True:
    try:
        items = getItems()
        deals = checkPrices(items)
        if len(deals) > 0:
            numDealsSeen += len(deals)
            for deal in deals:
                print("💵 " + deal["price"] + " (shipping not incl.)")
                # title of product up to 70 chars
                print("🎮 " + deal["name"][:75] )
                print("🔗 " + deal["href"] + "\n")
            thread = Thread(target=notify, daemon=True)
            thread.start()
        numLoops += 1
        print(f"\n============ Total checks: {numLoops}  |  Total 3060 Ti deals seen: {numDealsSeen} ============")
        print(f"                         Press CTRL + C to exit.")
        sleep(config.sleepDuration)
    except KeyboardInterrupt:
        sys.exit("\n🛑 Price checker killed.")