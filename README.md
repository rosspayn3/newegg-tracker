# newegg-tracker
Scripts that use BeautifulSoup to scrape Newegg for a given product that's in stock and below a price threshold. Developed on an Ubuntu-based Linux distro, not sure if this works on Windows.

## Dependencies

`pip3 install playsound lxml beautifulsoup4 notify-py`

## Usage
Modify `config.py` as you want. It contains two variables: 
- `sleepDuration` (integer): The number of seconds to wait between checks. Setting this to a higher number may reduce the chance you get flagged (and possibly IP banned).
- `notificationSoundFile` (string): An absolute path to an audio file to be played when the script finds a product. (included is `Discovery.ogg`, which is the file I used)

#### For `newegg-generic.py`
1. Create a new filtered search on Newegg for your desired product *. Copy this URL to be passed to the script.
2. Start the script and pass a price limit and the filtered URL ***in quotations*** as command line arguments.

`python3 newegg-generic.py 500 "https://www.newegg.com/p/pl?N=100007709%204131%20601359415&PageSize=96&Order=1"`

**Note: if a price filter is set on the Newegg URL, it must be higher than the amount passed to the script or no results will ever be returned.*