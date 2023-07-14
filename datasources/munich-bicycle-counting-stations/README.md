# Data from the permanent bicycle counting stations in Munich

## Details about the dataset

https://opendata.muenchen.de/dataset/raddauerzaehlstellen-muenchen

Bicycle counting station: Traffic counts from recent years have shown a significant increase in bicycle traffic in Munich. However, since the data is largely only collected on individual days as a "snapshot", so that random influences, e.g., due to varying weather conditions, could not be excluded when making comparisons, permanent bicycle counting stations were first established for bicycle traffic in Munich in 2008. With these counting stations, the development of bicycle traffic volume can be continuously monitored.

Currently, there are six permanent bicycle counting stations scattered across the city (map):

![](documentation/counting-stations-map.png)

- Arnulfstr. 9 - 11 South Side (the counts from the Arnulfstraße counting station were heavily influenced by a local construction site from the beginning of 2021 to March 2022 - additionally, there was a failure from May - July 2019. The Arnulfstraße counting station is currently the only one in the city that is not on a two-way bike path. Therefore, direction 2 records bicycles going against the direction of travel).
- Bad-Kreuther-Str. (Joseph-Hörwick-Weg) (The counting station was out of service from May - November 2013 - the permanent counting station was widened after the cycle path was reconstructed in April 2020)
- Erhardtstr. (Deutsches Museum)
- Hirsch HLP (Birketweg)
- Margaretenstr. (Harras)
- Olympia Park (Rudolf-Harbig-Weg) (The counting station in the Olympic Park was out of service from mid-June 2022 until the end of August 2022)

A sensor installed under the road surface detects the number of cyclists. The count results are stored with the respective current local weather data and can be retrieved as daily, hourly, or fifteen-minute values.

By counting over a longer period, it is also possible to determine a reliable factor for extrapolating from the results of the usual short-term counts (2 x 4 hours) to the daily values (24 hours) important for planning. Such an extrapolation procedure has been used for motor vehicles for years; one for bicycle traffic is to be developed.

Please note that while the provided data set is complete, further influences (failure of the sensors, weather, construction sites in the vicinity, changes in the cycle path routing, etc.) are not apparent from this data. Since the data is limited to six locations, it is also not possible to make precise statements about how bicycle traffic is developing in the rest of the urban area. This limitation of the data's meaningfulness should be taken into account when using the data.

**Available Data**

Each month (from 2017) or year (from 2008), there are

- 15-minute values of all 6 counting stations (approximately 18,000 rows each) and
- Weather data and daily values for all 6 counting stations
- Also, the list of counting stations with coordinates.

All can be accessed via the keyword Permanent Bicycle Counting Stations:

https://opendata.muenchen.de/dataset?tags=Raddauerzählstellen

or via the API:

https://opendata.muenchen.de/api/3/action/package_search?q=Raddauerzählstellen&rows=100

**Literature**

"On the Bike – Ready? – Go!" Results of the Permanent Bicycle Counting Stations in Munich 2017 and 2018 (PDF) in: Munich Statistics, 3rd Quarterly Edition, 2019

**Contact**

Mobility Department - Traffic and Behavior Data

verkehrsdaten.mor@muenchen.de

## Download full dataset

First we download the full dataset from the opendata portal of the city of Munich.

```
cd raw
python3 download_raw.py
```

## Clean the data

A jupyter notebook is provided to clean the data and save it in a more convenient format.

```
munich-bicycle-counting-stations-daily-data-cleaning.ipynb
```

The cleaned data is saved in the `cleaned` folder.