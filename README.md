# newegg-tracker
Scripts that use BeautifulSoup to scrape Newegg for a given product that's in stock and below a price threshold.

## Usage
Create a file called `config.py` in the same directory as the tracking script that contains two variables: 
- `sleepDuration`: The number of seconds (integer) to wait between checks. Setting this to a higher number may reduce the chance you get flagged (and possibly IP banned).
- `notificationSoundFile`: An absolute path to an audio file to be played when the script finds a product. 

#### For `newegg-generic.py`
1. Create a new filtered search on Newegg for your desired product *. Copy this URL to be passed to the script.
2. Start the script and pass a price limit and the filtered URL ***in quotations*** as command line arguments.

`python3 newegg-generic.py 500 "https://www.newegg.com/p/pl?N=100007709%204131%20601359415&PageSize=96&Order=1"`

**Note: if a price filter is set on the Newegg URL, it must be higher than the amount passed to the script or no results will ever be returned.*