
# coding: utf-8

# **Heroes of Pymoli Data Analysis**

# ** Observed Trend 1:** There are more male players than female

# **Observerd Trend 2:** Males spent more on buying items

# ** Observed Trend 3:** 20-24 age group purchased the most items

# In[1]:


import os
import pandas as pd
import numpy as np


# In[649]:


df=pd.read_json("purchase_data.json")
df


# **Player Count**

# In[109]:


# unique player count
number_of_players = df['SN'].nunique()
number_of_players


# In[372]:


pd.DataFrame([number_of_players], columns=['Number of Players'])


# **Purchasing Analysis (Total)**

# In[274]:


# number of unique items
number_of_unique_items = df['Item ID'].nunique()
number_of_unique_items


# In[140]:


# average purchase price
average_purchase_price = df['Price'].mean()
average_purchase_price = str(round( average_purchase_price, 2))
average_purchase_price


# In[374]:


# total number of purchases 
total_number_of_purchases = df.shape[0]
total_number_of_purchases


# In[373]:


# total revenue
total_revenue = df['Price'].sum()
total_revenue = '$' + str(round(total_revenue, 2))
total_revenue


# In[179]:


data = {'Number of Unique Items': number_of_unique_items,
       'Average Price': average_purchase_price,
       'Number of Purchases': total_number_of_purchases,
       'Total Revenue': total_revenue}


# In[184]:


pd.DataFrame([data])


# **Gender Demographics**

# In[641]:


# unique player counts
counts = df.groupby('Gender').nunique()['SN']
counts

# total player count ( unique )
total_count = counts.sum()
total_count


# In[640]:


male = counts[1]
female = counts[0]
other = counts[2]
percentage_male = ( male/total_count) * 100
percentage_female = ( female/total_count) * 100
percentage_other = ( other/total_count) * 100


# In[368]:


#gender_counts = {male:percentage_male, female: percentage_female, other: percentage_other}
gender_counts
labels = ['Percentage of Players', 'Total Count']
gender_counts = [(percentage_male, male), 
                 (percentage_female, female), 
                 (percentage_other, other)]


# In[369]:


pd.DataFrame.from_records(gender_counts, columns=labels, index=['male', 'female', 'other'])


# **Purchasing Analysis (Gender)**
# 

# In[646]:


# purchase count 
purchase_count = df['Gender'].value_counts()
purchase_count


# In[376]:


# average purchase by gender
avg_purchase_by_gender = df.groupby('Gender')['Price'].mean()
avg_purchase_by_gender


# In[377]:


# total purchase value
total_purchase_value = df.groupby('Gender')['Price'].sum()
total_purchase_value


# In[287]:


pd.DataFrame({'Purchase Count': purchase_count, 
              'Average Purchase Price': avg_purchase_by_gender,
              'Total Purchase Value': total_purchase_value
             })


# **Age Demographics**

# In[378]:


# bins for each age group
bins = [ 1, 9, 10, 14, 15, 19, 20, 24, 25, 29, 30, 34, 35, 39, 40]


# In[306]:


# purchase count
groups = df.groupby( pd.cut( df['Age'], bins) )
age_pur_count = groups.Price.count()


# In[309]:


# average purchase value
age_avg_price = groups.Price.mean()
age_avg_price


# In[379]:


# total purchase value
age_total_purchase = groups.Price.sum()


# In[311]:


pd.DataFrame( { 'Purchase Count': age_pur_count,
                'Average Purchase Price': age_avg_price,
                'Total Purchase': age_total_purchase
              })


# **Top Spenders**

# In[424]:


# top spenders
top_spenders = df.groupby("SN")
purchase_count = top_spenders['SN'].count()


# In[423]:


average_pur_price = top_spenders['Price'].mean()


# In[422]:


total_purchase = top_spenders['Price'].sum()


# In[425]:


top = pd.DataFrame( { "Purchase Count": purchase_count,
               "Average Purchase Price": average_pur_price,
               "Total Purchase Value": total_purchase })


# In[426]:


top.head()


# In[431]:


# Sort in descending order
top_five = top.sort_values("Total Purchase Value", ascending=False)
top_five.head()


# ** Most Popular Items **

# In[468]:


purchase_count = df.groupby('Item ID')['Item ID'].count()


# In[456]:


total_purchase_value = df.groupby('Item ID')['Price'].sum()



# In[648]:


item_price = df.groupby('Item ID')['Price'].mean()


# In[470]:


popular = pd.DataFrame( { "Purchase Count": purchase_count,
                "Item Price": item_price,
                "Total Purchase Value": total_purchase_value })


# In[471]:


popular.head()


# In[474]:


# top five popular items
popular.sort_values("Purchase Count", ascending=False).head()


# ** Most Profitable Items **

# In[585]:


purchase_count = df.groupby('Item ID')['Item ID'].count()


# In[586]:


total_purchase_value = df.groupby('Item ID')['Price'].sum()


# In[590]:


item_price = df.groupby('Item ID')['Price'].mean()


# In[632]:


profit = pd.DataFrame( { "Purchase Count": purchase_count,
                "Item Price": item_price,
                "Total Purchase Value": total_purchase_value })


# In[647]:


profit.head()


# In[634]:


profit.sort_values("Total Purchase Value", ascending=False).head()

