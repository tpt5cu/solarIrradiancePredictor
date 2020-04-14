# Solar Irradience Predictor

## Overview

Solar Irradience is measured in several different ways. 

**Global Horizontal Irradience (GHI)** is total amount of shortwave radiation received from above by a surface horizontal to the ground. This value is of particular interest to photovoltaic installations and includes both Direct Normal Irradiance (DNI) and Diffuse Horizontal Irradiance (DHI).

**Direct Normal Irradiance (DNI)** is the amount of solar radiation received per unit area by a surface that is always held perpendicular (or normal) to the rays that come in a straight line from the direction of the sun at its current position in the sky.


**Diffuse Horizontal Irradiance (DHI)** is the amount of radiation received per unit area by a surface (not subject to any shade or shadow) that does not arrive on a direct path from the sun, but has been scattered by molecules and particles in the atmosphere and comes equally from all directions

Formally, GHI can be constructed with DHI and DNI as follows: 

**Global Horizontal (GHI) = Direct Normal (DNI) X cos(θ) + Diffuse Horizontal (DHI)**

**It is of particular importance for utilities and solar energy producers to be able to estimate DHI given a partcular GHI.**

While previous approaches (see pvlib) have tried to derive mathematical models of being able to estimate DHI given GHI, cloud cover, and other various parameters, this repo intends to use statistical and machine learning techniques to estimate DHI with open source data and APIs. 

This technique allows for a more generalized model with minimal parameters, which reduces technical overhead. 

## Data

## Approach

## Conclusions

## Future Work

## Links




