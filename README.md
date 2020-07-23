# Solar Irradience Prediction


This repository explores various machine learning techniques to predict solar irrandience **DHI** and **DNI** from a GHI reading and other metoerological parameters. Finally we propose a new deep learning method to predict DHI from a GHI and several weather parameters. DNI can be extracted mathematically from these two values. The deep neural network was shown to predict DHI with a Mean Absolute Error (MAE) of 4 (w/m^2) to 12 (w/m^2). Which 1%-3% of the maximum value of DHI values (which range from 0-400 in my training data sets)

## Table of Contents

[1. Overview](#Overview)  
[2. Past Approaches and Literature Review](#Past-Approaches-and-Literature-Review)  
[3. Data ](#Data)  
[8. References](#References)

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


A 'pure' parametric model is the Lou[1] model. The Lou[1] model used the clearness index, solar altitude, air temperature, cloud cover and visibility as predictors for DHI. They trained a logistic regression model on data from Hong Kong and Denver, CO from the years 2008-2013. They found that the Mean Average Error (MAE) for Hong Kong was less than 21.5 w/m^2 and for Denver was less than 30 w/m^2.


In the spirit of Lou's[1] Model, we seek to use machine learning techniques, polynomial non-linear regression and a deep neural network to predict DHI. From DHI, we will use the physical equation defined above to derive DNI.

We believe the sparse connections amongst features and the heteroscedastic property of GHI and DHI data make physical models difficult with too much variablity in error and too little generality. We seek to build a general model that can be used regardless of location on earth. Our general model will be trained on open source data, and will utilize public local weather data to generate predictions. 



## Data

Data was pulled from two sources. 

Solar Irradience data was pulled from the [National Solar Radiation Database](https://nsrdb.nrel.gov/). Pointwise GHI, DHI, and DNI data is returned hourly for an entire calendar year. All irradience values are recorded in w/m^2. Location is for a latitude longitude coordinate pair. Coordinates were chosen based on the locations of [U.S. Climate Reference Network (USCRN)](https://www.ncdc.noaa.gov/crn/) monitoring stations. This is because the USCRN has real time measurements of GHI, which can be used to make real-time predictions of DHI. The NRSDB is not updated so frequently. 

In addition to solar irradience data, this project uses other weather data such as cloud cover, air pressure, and season data to try and model the relationship between GHI and DHI. For that, this project pulls data from [darksky](https://darksky.net/dev).

## Approach

The full modeling approach is conducted and documented in 'statistical_irradience_modeling.ipynb'. 

To summarize, the notebook pulls in 'base case' data, and tries to initially fit a robust model from that. In this case, the 'base case' is psm data from South Dakota in 2018. 2018 was chosen as a base year because for nearly all locations sampled, 2018 had a much higher resolution and much more accurate sample of cloud cover data (from darksky) for each hour of the year. For example, darksky cloud cover data appears to be bucketed in pre-2018 years, whereas 2018 onwards cloud cover is more continuous. Absolute zero values of GHI were removed because a reading of absolute 0 typically would mean a nighttime reading. Night time values combined with a cloud cover reading would skew the model. 

An intial plot of DHI vs. GHI, shows the data to be quite heteroscedastic. GHI and DHI data is definetly skewed towards lower values. Cloud cover appears to be two tailed.

Because of heteroscedasticity, data transformations were necessary.

## Conclusions

## Future Work

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





