
# coding: utf-8

# In[1]:

import requests
import json
import numpy as np
import pandas as pd
import pprint
import math
import datetime
pd.options.display.max_columns = 999
# np.set_printoptions(suppress=True)
# pd.set_option('display.float_format', lambda x: '%.3f' % x)
shopify_data = pd.read_csv("forecasting/pcsg_shopify_20180531.csv", low_memory=False, dtype={'Lineitem sku': 'str'})

def try_float(x):
    try:
        return str(format(float(x), '.0f'))
    except ValueError as e:
        return x

shopify_data['Name'] = shopify_data['Name'].apply(try_float)
sku_master = pd.read_excel("C:/Users/limzi/OneDrive/Forecasting & Reporting/PCSG Master List.xlsx", sheet_name='SKU List' )
bundle_master = pd.read_excel("C:/Users/limzi/OneDrive/Forecasting & Reporting/PCSG Master List.xlsx",
                              sheet_name='Bundles' ).rename(columns = {'Parent SKU': "parent_sku",
                                                                      'Parent Name': 'parent_name',
                                                                      'Quantity': 'child_quantity',
                                                                      'Child SKU': "child_sku",
                                                                      'Child Name': 'child_name'}).astype({'child_sku': 'str',
                                                                                                           'parent_sku': 'str'})


# In[168]:

shopify_data_merge = pd.merge(shopify_data, bundle_master, left_on="Lineitem sku", right_on = 'parent_sku', how='left')
shopify_data_merge#[shopify_data_merge['Lineitem sku'] == '4707']


# In[82]:

shopify_data_merge['parent_sku'].fillna(shopify_data_merge['Lineitem sku'], inplace=True)
shopify_data_merge['child_sku'].fillna(shopify_data_merge['Lineitem sku'], inplace=True)
shopify_data_merge['child_quantity'].fillna(shopify_data_merge['Lineitem quantity'], inplace=True)
shopify_data_merge['Discount Unit Price'].fillna(shopify_data_merge['Lineitem price'], inplace=True)
# shopify_data_merge['Unit Price'].fillna(shopify_data_merge['Lineitem compare at price'], inplace=True)
# shopify_data_merge['total_quantity'].fillna(shopify_data_merge['Lineitem quantity'], inplace = True)
shopify_data_merge['child_subtotal_quantity'] =  shopify_data_merge['child_quantity'] * shopify_data_merge['Lineitem quantity']
shopify_data_merge['child_subtotal'] =  shopify_data_merge['child_subtotal_quantity'] * shopify_data_merge['Discount Unit Price']
shopify_data_final = shopify_data_merge.copy()


# In[83]:

# shopify_data_final.to_excel('formatted_shopify_data.xlsx')
shopify_data_final


# In[85]:

shopify_data_final.groupby(['Name'])['child_subtotal'].sum()
