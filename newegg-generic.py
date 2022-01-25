import sys
import requests, lxml
from notifypy import Notify
from playsound import playsound
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread
import config

if len(sys.argv) == 3:
    try:
        priceLimit = int(sys.argv[1])
        url = sys.argv[2]
    except:
        sys.exit(f"\n🛑 Something went wrong. Correct usage is:\npython3 {sys.argv[0]} [integer price limit] [string Newegg URL]\n")
elif len(sys.argv) == 2:
    try:
        priceLimit = int(sys.argv[1])
    except:
        sys.exit(f"\n🛑 Something went wrong. Correct usage is:\npython3 {sys.argv[0]} [integer price limit]\n")
else:
    sys.exit("\n🛑 Incorrect usage. Correct usage is:\n'python3 {sys.argv[0]} [integer price limit] [filtered Newegg URL]'\n")

print(f"\n🔵 Checking Newegg for products with a price limit of ${priceLimit}...\n   Press CTRL + C to exit.\n")

numLoops = 0
numDealsSeen = 0

def getItems():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    containers = soup.find_all("div", class_="item-container")
    return containers

def checkPrices(items):
    deals = []
    for item in items:
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
    return deals

def notify():
    notification = Notify()
    notification.title = "Found product in stock!"
    notification.message = "Check your terminal!"
    notification.send()
    playsound(config.notificationSoundFile)

if __name__ == "__main__":
    while True:
        try:
            items = getItems()
            deals = checkPrices(items)
            if len(deals) > 0:
                numDealsSeen += len(deals)
                for deal in deals:
                    print("💵 " + deal["price"])
                    # title of product up to 75 chars
                    print("🎮 " + deal["name"][:75] )
                    print("🔗 " + deal["href"] + "\n")
                thread = Thread(target=notify, daemon=True)
                thread.start()
            numLoops += 1
            print(f"\n============ Total checks: {numLoops}  |  Total product deals seen: {numDealsSeen} ============")
            print(f"                          Press CTRL + C to exit.\n")
            sleep(config.sleepDuration)
        except KeyboardInterrupt:
            sys.exit("\n🛑 Price checker killed.")
