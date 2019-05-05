# Cooperative City Network

## Getting the CHMI data from the [Golemio API](https://golemio.docs.apiary.io/#reference/0/meteostanice-chmi/airquality-report-from-to-v2)

```sh
cd data-chmi
./get
./merge
```

## Plotting the CHMI data as function of space and time

You can choose the number of the pollutant from the following:

  1. "NO2": [Video](NO2/2D-Pollution-video.gif)
  2. "O3" 
  3. "PM10"
  4. "PM10_24"
  5. "PM2_5"
  6. "SO2"

```sh
cd data-chmi
python plotPollutionMaps.py
./buildVideo.sh
```

Example of video is given here: 

## Upload data to [HERE Maps XYZ Studio](https://xyz.here.com/studio/)

```sh
# Install dependencies
yarn

# Setup your HERE Maps credentials from https://account.here.com/
yarn here configure

# Create a data space
yarn here xyz create --title "CHMI Prague" --message "Show CHMI data from Golemio API"

# Upload data (use ID of the space created in the previous step)
yarn here xyz upload -f data-chmi/merge.csv --ptag DateToUTC [spaceID]

```
