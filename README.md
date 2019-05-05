# Cooperative City Network

## Getting the CHMI data from the [Golemio API](https://golemio.docs.apiary.io/#reference/0/meteostanice-chmi/airquality-report-from-to-v2)

```
cd data-chmi
./get
./merge
```

## Plotting the CHMI data as function of space and time

```
cd data-chmi
python plotPollutionMap.py
```

> Note: It is not ready yet. However, the plot2dHeatMap script should work on the new data.
