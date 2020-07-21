# Solar Irradience Predictor


This repository explores various machine learning techniques to predict solar irrandience **DHI** and **DNI** from a GHI reading and other metoerological parameters.

## Table of Contents

[1. Overview](#Overview)  
[2. Data ](#Data)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>




## Overview

Solar Irradience is measured in several different ways. 

**Global Horizontal Irradience (GHI)** is total amount of shortwave radiation received from above by a surface horizontal to the ground. This value is of particular interest to photovoltaic installations and includes both Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).

**Direct Normal Irradiance (DNI)** is the amount of solar radiation received per unit area by a surface that is always held perpendicular (or normal) to the rays that come in a straight line from the direction of the sun at its current position in the sky.


**Diffuse Horizontal Irradiance (DHI)** is the amount of radiation received per unit area by a surface (not subject to any shade or shadow) that does not arrive on a direct path from the sun, but has been scattered by molecules and particles in the atmosphere and comes equally from all directions

Formally, GHI can be constructed with DHI and DNI as follows: 

**Global Horizontal (GHI) = Direct Normal (DNI) X cos(θ) + Diffuse Horizontal (DHI)**

**It is of particular importance for utilities and solar energy producers to be able to estimate DHI given a partcular GHI.**

While previous approaches (see [pvlib](https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.disc.html)) have tried to derive mathematical models of being able to estimate DHI given GHI, cloud cover, and other various parameters, this repo intends to use statistical and machine learning techniques to estimate DHI with open source data and APIs. 

This technique allows for a more generalized model with minimal parameters, which reduces technical overhead. 

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

## Links




