# Solar Irradience Prediction


This repository explores various machine learning techniques to predict solar irrandience **DHI** and **DNI** from a GHI reading and other metoerological parameters. Finally we propose a new deep learning method to predict DHI from a GHI and several weather parameters. DNI can be extracted mathematically from these two values. The deep neural network was shown to predict DHI with a Mean Absolute Error (MAE) of 4 (w/m^2) to 12 (w/m^2). Which 1%-3% of the maximum value of DHI values (which range from 0-400 in my training data sets)

This model is trained on synthetic historical data but uses open source, real time data measurements to make predictions. 

## Table of Contents

[1. Overview](#Overview)  
[2. Past Approaches and Literature Review](#Past-Approaches-and-Literature-Review)  
[3. Data ](#Data) 
[4. Approach](#Approach)
[5. Conclusions](#Conclusions)
[6. Future Work](#Future-Work) 
[7. References](#References)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Overview

With increased demand for solar energy, comes an increased need to ensure that solar energy plants are constructed in optimal locations, such as locations with a large amount of solar irradiance.

Solar Irradience is measured in several different ways:

**Global Horizontal Irradience (GHI)** is total amount of shortwave radiation received from above by a surface horizontal to the ground. This value is of particular interest to photovoltaic installations and includes both Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).

**Direct Normal Irradiance (DNI)** is the amount of solar radiation received per unit area by a surface that is always held perpendicular (or normal) to the rays that come in a straight line from the direction of the sun at its current position in the sky.

**Diffuse Horizontal Irradiance (DHI)** is the amount of radiation received per unit area by a surface (not subject to any shade or shadow) that does not arrive on a direct path from the sun, but has been scattered by molecules and particles in the atmosphere and comes equally from all directions


Ideally, solar energy plants would be built in areas with a large amount of DNI, because that provides the most amount of solar energy per area. However data is not usually avaliable for a DNI measurement because the sensors used to measure DNI are complex and expensive. GHI measurements, however, are far more readily avaliable. Therefore, **it is of particular importance for utilities and solar energy producers to be able to estimate DHI and DNI given a partcular GHI.**


Formally, GHI can be constructed with DHI and DNI as follows: 

**Global Horizontal (GHI) = Direct Normal (DNI) X cos(θ) + Diffuse Horizontal (DHI)**

![Alt text](ghi-dhi-dni-visual.png?raw=true "ghi-dhi-dni-visual")


For more information about GHI, DNI, and DHI, please visit [this link](https://firstgreenconsulting.wordpress.com/2012/04/26/differentiate-between-the-dni-dhi-and-ghi/#:~:text=Global%20Horizontal%20Irradiance%20(GHI)) 


## Past Approaches and Literature Review

This section briefly outlines a few approaches to predicting DHI and DNI from GHI. It is not an exhaustive literature review.

Previous approaches come in predominantly two categories: parametric and decomposition models.

Parametric models use meterological data of solar irradience, cloud cover, atmospheric turbidity, pressure, and others to estimate DNI. Parametric models tend to require lots of detailed data on weather information. Often times this extensive data is not readily avaliable.

Decomposition models rely on statistical relationships between GHI, DHI, and DNI to derive and predict DNI. Decomposition models (or Physical models) require far less data, typically only requiring GHI to make a prediction. 


Most of the past approaches consisted of predominantly decomposition models: such as Maxwell[6], Bristow[4], and Lee[3]. These papers also reference other decomposition models including Lee, Reindl-2, and Vignola and McDaniels. 

Newer approaches take a hybrid approach of parametric and decomposition models. These include Lou[1], a Quasi-Physical model in Lee[3], and modeling done in **this repository**.


### Decomposition models

Decomposition models have been quite popular for this problem. One of the most popular models is the DISC model formalized by Maxwell[6]. The DISC model is a quasi-physical model which is similair to Lee[3]. These will be discussed later in the Parametric models section. 

An example of a true decomposition models (or physical models) is the **Bristow[4]** model. The Bristow model proposes an equation to seperate total solar irradiation (GHI) into its direct and diffuse components. The model is based on physically determined coefficients based on total daily solar irradiance and the Gates equation for potential solar radiation. The model was tested in Washington State and Queensland, Australia. The model was shown to RMS deviations from the predicted values were less than 1.6 MJ/day no matter the weather conditions. During our tests, the model was shown not to have predictive power at the hourly interval or in the test locations we chose. 

Decomposition modelshave routinely been subject to compatability problems. A model that works well on some localized data tends not to work well on generalized data. Bindi[5] compares several models on different locations and found that there is large inter-site variability in prediction accuracy. This variation increases as the time resolution decreases.


### Parametric and Quasi-Physical Models


Quasi-decomposition (physical) models such as the Maxwell model[6] are built primarily on physical equations of irradience, but derived various coefficients from regression analysis of direct and global clearness indidces. The model was tested on several locations, with a RMSE not lower than 15% of actual DNI value. Additionally, the DISC model also measured monthly values. We desire higher resolution measurement and prediction. PVlib developed by NREL [has a good overview of and code for the DISC model](https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.disc.html)


An extension of the Maxwell[6] model is the Lee[3] model. The Lee[3] model builds upon the physical components of the Maxwell[6] model, but uses different step-wise regression techniques with local data from Daejon, South Korea to derive their model's coefficients. They found that the Maxwell[6] model had too large error and could not handle outliers well. They noted a 13.1% decrease in RMSE as compared to the Maxwell[6] model. The authors posit their model could be used for most East-Asian regions


A 'pure' parametric model is the Lou[1] model. The Lou[1] model used the clearness index, solar altitude, air temperature, cloud cover and visibility as predictors for DHI. They trained a logistic regression model on data from Hong Kong and Denver, CO from the years 2008-2013. They found that the Mean Absolute Error (MAE) for Hong Kong was less than 21.5 w/m^2 and for Denver was less than 30 w/m^2.


In the spirit of Lou's[1] Model, we seek to use machine learning techniques, polynomial non-linear regression and a deep neural network to predict DHI. From DHI, we will use the physical equation defined above to derive DNI.

We believe the sparse connections amongst features and the heteroscedastic property of GHI and DHI data make physical models difficult with too much variablity in error and too little generality. We seek to build a general model that can be used regardless of location on earth. Our general model will be trained on open source data, and will utilize public local weather data to generate predictions. 



## Data

Data was pulled from two sources, the [National Solar Radiation Database](https://nsrdb.nrel.gov/) and [darksky](https://darksky.net/dev). 


[National Solar Radiation Database](https://nsrdb.nrel.gov/) data is a collection of hourly [TMY](https://nsrdb.nrel.gov/about/tmy.html) datasets containing meteorological data and the three most common measurements of solar radiation: global horizontal, direct normal and diffuse horizontal irradiance. The data is synthetic in that GHI and DHI are modeled from the [REST2](https://www.solarconsultingservices.com/rest2.php) and FARMS models. 

NRSDB data sets include a qualitative measurement for cloud cover but not a numeric. Therefore, numeric cloud cover data as a percentage is fetched from [darksky](https://darksky.net/dev). 

The directory `Raw_Data` contains annual hourly raw psm (Physical Solar Model) data for a year for various locations. Locations involved with training have raw data for the years 2010-2018. A date pipeline called `data_munger.py` fetches from [darksky](https://darksky.net/dev) the numerical cloud cover readings, and inserts them at the correct time intervals into the raw data set. The raw data set is then transformed into the correct format for training and written into `Test_Data`. 

**Please Note**, not all of the data in `Test_Data` is used solely for testing. In the `statistical_irradience_modeling.ipynb` notebook, regression analysis is conducted on a single location for a single year, but tested on multiple locations for multiple years. Likewise in the neural network model, data from multiple locations for years 2010-2018 is used to train the model, but then other locations are used to test the model. 


Because data from the [NRSDB](https://nsrdb.nrel.gov/) is both synthetic and updated only annually, more recent data calls are required to make up to date, recent, or even real time predictions.

For production environments, GHI data from [U.S. Climate Reference Network (USCRN)](https://www.ncdc.noaa.gov/crn/) monitoring stations will be used. This is because the USCRN has real time measurements of GHI, which can be used to make real-time predictions of DHI. Much of the training data locations chosen to train the statistical models and the neural network were chosen based off of [U.S. Climate Reference Network (USCRN)](https://www.ncdc.noaa.gov/crn/) station locations. 
For real time meterological data, [darksky](https://darksky.net/dev) is again used. 


## Approach


### Statistical Approach


#### Fitting

**The full modeling approach is conducted and documented in 'statistical_irradience_modeling.ipynb'.**


Initially a statistical fitting of GHI vs. DHI was introduced. However due to heteroscedasticity, a second explanatory variable, Cloud Cover, was introduced to try and improve prediction power. To try and normalize the feature variable distributions, zero values for GHI (for example, readings during night time hours), were removed. To improve heteroscedasticity issues, the feature variables GHI and Cloud Cover were log-transformed. The following statistical models were fitted on PSM data from Reliance, South Dakota for the year of 2018. 



1. Polynomial fit on log transformation of DHI  
2. OLS fit on Log transformation of feature variables and log transformation of response variable  
3. OLS fit on a power transformation of all variables
4. OLS fit on sqrt transformation of all variables
5. OLS fit on logit transformation of cloud cover and log transformation of GHI
6. Genralized Least Squares model on log transformation of GHI values  
7. GLS model on log transformation of GHI and DHI
8. Weighted Least Squares model on log transformation of GHI and DHI. Cloud Cover is normal  
9. Polynomial fit on Log transformation of feature variables  
10. Polynomial fit on Log transformation of all variables  


#### Validation, testing, and results

The models were then validated on PSM data from Relaince, South Dakota for the year of 2017. The polynomial regression with log transformation of GHI and DHI ended up being the best fit. The model had an r-squared value of 0.72 and a mean absolute error of 48.3 w/m2. 

When tested on other locations in the usa for the years 2010-2018, the Polynomial model had a mean absolute percentage error of 30%-45%, when the predictions were exponentiated from log transformed space. 

Overall even though the model had a fairly good fit, the outliers and heteroscedasticity caused simply too high of an average error to be useful. It is was found to be very difficult for a statistical model to fit the complex data shape. 




### Neural Network

**The full approach and code for the neural network is in Neural_Net**

Enter the neural network. Because of sparse connections and the complex interactions of many different meterological parameters, a neural network was explored as an option to model and predict DHI. 


The deep neural network was trained on 5 locations for the years 2010-2018 from 5 locations in the usa. Various meterological parameters were selected as input features including air pressure, solar zenith, month and day (to capture seasonality), and GHI. All these weather parameters are avaliable from the NRSDB or darksky. 



#### Training

The deep neural network performed surprisingly well. After 100 epochs of training, the neural network had a training set Mean Absolute Error (mae) of around only 4.27 w/m^2, with a Root Mean Squared Error (rmse) of around 10.5 w/m^2. Considering DHI values range from 0-400, those readings represent a 1%-2.5% error off range of values. 

#### Validation and Testing

The model was validated on data from the Outer Banks, NC for the year 2018. The model performed with an mae of 7.122 w/m^2 with an rmse of 16.4 w/m^2. Considering that the location chosen for validation was not in the training set nor is it similair to any of the training sets in terms of lcoation, the model performs surprisingly well. 

The model was then tested on several other locations in the USA including Miami, Boulder, Lincoln, San Diego, Quinault, Oldtown, and Murphey for the 2018 year. With the exception of Miami and Boulder, the model had a mae of less than 8 w/m^2.

Model specific networks were trained on 10 years of Boulder, CO and Miami, FL data with improvements in accuracy. 

## Conclusions


Our results show that the neural network model outperforms physical, quasi physical, and decomposition models for multiple locations and years. 

Comparison with other models:

-Lee[3] RMSE of 63.37 w/m^2 of Daejon, South Korea  
-Lou[1] MAE of  <21.5 w/m^2 for HK and <30.0 w/m^2 for Denver over 5 years of data

My model: MAE of <10 w/m^2 and RMSE of <15 w/m^ for several locatins in the usa over 10 years of data from 2010-2018.
Several locations have slightly higher errors, but training location specific models can mitigate this issue. 

## Future Work

-Verifying model on real-time/empirical data, not simulated or modeled  
-Trying different network architectures to improve accuracy


## References

[1] Lou, S., Li, D. H. W., Lam, J. C., & Chan, W. W. H. (2016). Prediction of diffuse solar irradiance using machine learning and multivariable regression. Applied Energy, 181, 367–374. doi:10.1016/j.apenergy.2016.08.093 

https://www.sciencedirect.com/science/article/abs/pii/S0306261916311916

[2] Ridley, B., Boland, J., & Lauret, P. (2010). Modelling of diffuse solar fraction with multiple predictors. Renewable Energy, 35(2), 478–483. doi:10.1016/j.renene.2009.07.018 

https://www.sciencedirect.com/science/article/abs/pii/S0960148109003012

[3] Lee, H.-J., Kim, S.-Y., & Yun, C.-Y. (2017). Comparison of Solar Radiation Models to Estimate Direct Normal Irradiance for Korea. Energies, 10(5), 594. doi:10.3390/en10050594 

https://www.researchgate.net/publication/316639367_Comparison_of_Solar_Radiation_Models_to_Estimate_Direct_Normal_Irradiance_for_Korea

[4] BRISTOW, K., CAMPBELL, G., & SAXTON, K. (1985). An equation for separating daily solar irradiation into direct and diffuse components☆. Agricultural and Forest Meteorology, 35(1-4), 123–131. doi:10.1016/0168-1923(85)90079-6 

https://www.sciencedirect.com/science/article/pii/0168192385900796


[5] Bindi, M. & Miglietta, F. & Zipoli, Gaetano. (1992). Different methods for separating diffuse and direct components of solar radiation and their application in crop growth models. Climate Research - CLIMATE RES. 2. 47-54. 10.3354/cr002047. 

https://pdfs.semanticscholar.org/df09/12776bec14da57ae79752982df6274dd6e8b.pdf


[6] Maxwell, E. L., “A Quasi-Physical Model for Converting Hourly Global Horizontal to Direct Normal Insolation”, Technical Report No. SERI/TR-215-3087, Golden, CO: Solar Energy Research Institute, 1987.

https://www.nrel.gov/docs/legosti/old/3087.pdf





