#!/usr/bin/env python
# coding: utf-8

# # Analyzing wildfire activities in Australia

# ## __Table of Contents__
# 
# <ol>
#     <li><a href="#Objectives">Objectives</a></li>
#     <li>
#         <a href="#Setup">Setup</a>
#         <ol>
#             <li><a href="#Installing-Required-Libraries">Installing Required Libraries</a></li>
#             <li><a href="#Importing-Required-Libraries">Importing Required Libraries</a></li>
#     </li>
#     <li>
#         <a href="#Dataset">Dataset</a>
#     </li>
#     <li><a href="#Importing Dataset">Importing Dataset</a></li>
#     <li><a href="#Practice Tasks">Practice Tasks</a></li>
#    
# 

# ## Objectives
# 
# After completing this lab you will be able to:
# 
#  - Use visualization libraries such as Matplotlib, Pandas, Seaborn and Folium to create informative plots and charts
# 

# ### Installing Required Libraries

# In[19]:


get_ipython().run_line_magic('pip', 'install seaborn')
get_ipython().run_line_magic('pip', 'install folium')


# ### Importing Required Libraries
# 
# 

# In[20]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
get_ipython().run_line_magic('matplotlib', 'inline')


# ---
# 

# # Dataset
# 
# **Historical Wildfires**
# 
# This wildfire dataset contains data on fire activities in Australia starting from 2005. Additional information can be found [here](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/c6-mcd14dl).
# 
# Variables
# 
# - Region: the 7 regions
# - Date: in UTC and provide the data for 24 hours ahead
# - Estimated_fire_area: daily sum of estimated fire area for presumed vegetation fires with a confidence > 75% for a each region in km2
# - Mean_estimated_fire_brightness: daily mean (by flagged fire pixels(=count)) of estimated fire brightness for presumed vegetation fires with a confidence level > 75% in Kelvin
# - Mean_estimated_fire_radiative_power: daily mean of estimated radiative power for presumed vegetation fires with a confidence level > 75% for a given region in megawatts
# - Mean_confidence: daily mean of confidence for presumed vegetation fires with a confidence level > 75%
# - Std_confidence: standard deviation of estimated fire radiative power in megawatts
# - Var_confidence: Variance of estimated fire radiative power in megawatts
# - Count: daily numbers of pixels for presumed vegetation fires with a confidence level of larger than 75% for a given region
# - Replaced: Indicates with an Y whether the data has been replaced with standard quality data when they are available (usually with a 2-3 month lag). Replaced data has a slightly higher quality in terms of locations
# 

# ---
# 

# ### Importing Data
# 

# In[21]:


import requests
from io import BytesIO

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
response = requests.get(URL)

if response.status_code == 200:
    # Use BytesIO to create a file-like object from the response content
    text = BytesIO(response.content)

    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(text)

    print('Data read into a pandas dataframe!')
else:
    print(f"Failed to retrieve the data. Status code: {response.status_code}")


# Let's look at some samples rows from the dataset we loaded:
# 

# In[22]:


df.head()


# ---
# 

# Let's verify the column names and the data type of each variable
# 

# In[23]:


#Column names
df.columns


# In[24]:


#data type
df.dtypes


# Notice the type of 'Date' is object, let's convert it to 'datatime' type and also let's extract 'Year' and 'Month' from date and include in the dataframe as separate columns
# 

# In[25]:


import datetime as dt

df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Month'] = pd.to_datetime(df['Date']).dt.month


# **Verify the columns again**
# 

# In[26]:


df.dtypes


# ---
# 

# #### Let's try to understand the change in average estimated fire area over time <br>(use pandas to plot)
# 

# In[27]:


plt.figure(figsize=(12, 6))
df_new=df.groupby('Year')['Estimated_fire_area'].mean()
df_new.plot(x=df_new.index, y=df_new.values)
plt.xlabel('Year')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()


# ---
# 

# #### You can notice the peak in the plot between 2010 to 2013. Let's narrow down our finding, by plotting the estimated fire area for year grouped together with month.
# 

# In[28]:


df_new=df.groupby(['Year','Month'])['Estimated_fire_area'].mean()
df_new.plot(x=df_new.index, y=df_new.values)
plt.xlabel('Year, Month')
plt.ylabel('Average Estimated Fire Area (km²)')
plt.title('Estimated Fire Area over Time')
plt.show()


# This plot represents that the estimated fire area was on its peak after 2011, April and before 2012. You can verify on google/news, this was the time of maximum wildfire hit in Austrailia
# 

# ---
# 

# #### Let's have an insight on the distribution of mean estimated fire brightness across the regions<br> use the functionality of seaborn to develop a barplot
# 

# before starting with the plot, why not know the regions mentioned in the dataset?. <br>Make use of unique() to identify the regions in the dataset (apply it on series only)
# 

# In[29]:


df['Region'].unique()


# <details>
#     <summary>Click here for a Hint</summary>
# you need to plot reions on x-axis and the 'Mean_estimated_fire_brightness' on y-axis.<br>Title it as 'Distribution of Mean Estimated Fire Brightness across Regions'
# </details>
# 

# In[30]:


plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Region', y='Mean_estimated_fire_brightness')
plt.xlabel('Region')
plt.ylabel('Mean Estimated Fire Brightness (Kelvin)')
plt.title('Distribution of Mean Estimated Fire Brightness across Regions')
plt.show()


# ---
# 

# #### Let's find the portion of count of pixels for presumed vegetation fires vary across regions<br> we will develop a pie chart for this
# 

# <details>
#     <summary>Click here for a Hint</summary>
# First you will  be required to group the data on region and find the sum of count
# </details>
# 

# In[31]:


plt.figure(figsize=(10, 6))
region_counts = df.groupby('Region')['Count'].sum()
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%')
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.axis('equal')
plt.show()


# #### See the percentage on the pie is not looking so good as it is overlaped for Region SA, TA, VI
# 
# remove the autopct fromm pie function and pass the following to plt.legend() after plt.title() <br>
# `[(i,round(k/region_counts.sum()*100,2)) for i,k in zip(region_counts.index, region_counts)]`
# 

# In[32]:


plt.figure(figsize=(10, 6))
region_counts = df.groupby('Region')['Count'].sum()
plt.pie(region_counts, labels=region_counts.index)
plt.title('Percentage of Pixels for Presumed Vegetation Fires by Region')
plt.legend(labels=[f"{i} ({round(k/region_counts.sum()*100, 2)}%)" for i, k in zip(region_counts.index, region_counts)], loc='best')
plt.axis('equal')
plt.show()


# ---
# 

# #### Let's try to develop a histogram of the mean estimated fire brightness<br> Using Matplotlib to create the histogram
# 

# <details>
#     <summary>Click here for a Hint</summary>
#     Call plt.hist() and pass df['Mean_estimated_fire_brightness'] as x
# </details>
# 

# In[33]:


plt.figure(figsize=(10, 6))
plt.hist(x=df['Mean_estimated_fire_brightness'], bins=20)
plt.xlabel('Mean Estimated Fire Brightness (Kelvin)')
plt.ylabel('Count')
plt.title('Histogram of Mean Estimated Fire Brightness')
plt.show()


# #### What if we need to understand the distribution of estimated fire brightness across regions? Let's use the functionality of seaborn and  pass region as hue
# 

# In[34]:


sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region')
plt.show()


# ### looks better!, now include the parameter `multiple='stack'` in the histplot() and see the difference. Include labels and titles as well
# 

# In[35]:


sns.histplot(data=df, x='Mean_estimated_fire_brightness', hue='Region', multiple='stack')
plt.show()


# ---
# 

# #### Let's try to find if there is any correlation between mean estimated fire radiative power and mean confidence level?
# 

# <details>
#     <summary>Click here for a Hint</summary>
#     Call plt.scatter() <br> or use the sns.scatterplot()
# </details>
# 

# In[36]:


plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='Mean_confidence', y='Mean_estimated_fire_radiative_power')
plt.xlabel('Mean Estimated Fire Radiative Power (MW)')
plt.ylabel('Mean Confidence')
plt.title('Mean Estimated Fire Radiative Power vs. Mean Confidence')
plt.show()


# ---
# 

# #### Let's mark these seven regions on the Map of Australia using Folium
# <br> we have created a dataframe for you containing the regions, their latitudes and longitudes. <br> For australia use [-25, 135] as location to create the map
# 

# In[37]:


region_data = {'region':['NSW','QL','SA','TA','VI','WA','NT'], 'Lat':[-31.8759835,-22.1646782,-30.5343665,-42.035067,-36.5986096,-25.2303005,-19.491411],
               'Lon':[147.2869493,144.5844903,135.6301212,146.6366887,144.6780052,121.0187246,132.550964]}
reg=pd.DataFrame(region_data)
reg


# In[38]:


# instantiate a feature group
aus_reg = folium.map.FeatureGroup()

# Create a Folium map centered on Australia
Aus_map = folium.Map(location=[-25, 135], zoom_start=4)

# loop through the region and add to feature group
for lat, lng, lab in zip(reg.Lat, reg.Lon, reg.region):
    aus_reg.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            popup=lab,
            radius=5, # define how big you want the circle markers to be
            color='red',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )

# add incidents to map
Aus_map.add_child(aus_reg)


# ---
# 
