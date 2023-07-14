
## Project Overview

The focal point of this project resides within the realm of urban planning and transportation, specifically forecasting cyclist traffic in Munich. Stemming from the city's open data initiative and the need to better understand and manage cyclist traffic based on various influencing factors, we will use machine learning to predict the expected number of cyclists on any given day. We will be considering weather forecasts and historical data for our prediction model.

The fundamental dataset for this project is derived from the Munich Bicycle Counting Stations. Established in 2008, these stations serve the purpose of monitoring the incrementing bicycle traffic in Munich on a continuous basis. Additional data sources have been categorized and stored in individual folders within the 'datasources' directory. Each of these folders not only contains the data but also detailed documentation and scripts or Jupyter notebooks to facilitate data download and preprocessing. For more specific details on the main dataset and its structure, please refer to the README in the respective dataset folder.

### Problem Statement

The task at hand is to develop a model that can predict the number of cyclists in Munich for a given day with reasonable accuracy. We aim to accomplish this by incorporating weather forecast data and historical cyclist count data. The end solution is expected to be a model that takes these inputs and outputs the predicted cyclist count. Such a model can assist the city's urban planning department in better understanding, managing, and making informed decisions about cyclist infrastructure and safety.

### Metrics

The primary performance metric for our model will be the Weighted Absolute Percentage Error (WAPE). The WAPE is a measure of prediction accuracy that specifically accounts for different levels of demand, which is ideal for our case due to the potentially fluctuating nature of cyclist counts.

The use of WAPE provides an intuitive and interpretable understanding of accuracy. It gives a clear representation of the average error rate, providing an easy-to-understand percentage error that can be communicated to stakeholders and used to guide decision-making.

