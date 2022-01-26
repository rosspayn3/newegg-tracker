# newegg-tracker
Scripts that use BeautifulSoup to scrape Newegg for a given product that's in stock and below a price threshold. Developed on an Ubuntu-based Linux distro, not sure if this works on Windows.

## Dependencies

### Linux (and MacOS?)

`pip3 install lxml beautifulsoup4 notify-py playsound`

### Windows

The newer versions of the playsound library don't play well with Windows using `\` instead of `/` as a path separator, so an older version must be used for these scripts to run on Windows.

`pip3 install lxml beautifulsoup4 notify-py playsound==1.2.2`

## Usage
Modify `config.py` as you want. It contains two variables: 
- (integer) `sleepDuration` : The number of seconds to wait between checks. Setting this to a higher number may reduce the chance you get flagged (and possibly IP banned).
- (string) `notificationSoundFile` : An absolute path to an audio file to be played when the script finds a product. (included is `Discovery.mp3` which is the file I used)

#### For `newegg-generic.py`
1. Create a new filtered search on Newegg for your desired product *. Copy this URL to be passed to the script.
2. Start the script and pass a price limit and the filtered URL ***in quotations*** as command line arguments.

`python3 newegg-generic.py 600 "https://www.newegg.com/p/pl?N=100007709%204131%20601359415&PageSize=96&Order=1"`

**Note: if a price filter is set on the Newegg URL, it must be higher than the amount passed to the script or no results will ever be returned.*

#### For specific trackers:
1. Start the script and pass an optional price limit as a command line argument. The scripts contain "reasonable" defaults by today's market values.

`python3 newegg-3060-ti.py [999]`
