# Cooperative City Network

## Getting the CHMI data from the [Golemio API](https://golemio.docs.apiary.io/#reference/0/meteostanice-chmi/airquality-report-from-to-v2)

```
cd data-chmi
./get
./merge
```

## Plotting the CHMI data as function of space and time

You can choose the number of the pollutant in the followings. 
1: "NO2"
2: "O3"
3: "PM10"
4: "PM10_24"
5: "PM2_5"
6: "SO2"
```
cd data-chmi
python plotPollutionMap.py
./buildVideo.sh
```

