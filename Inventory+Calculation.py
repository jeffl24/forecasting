


import numpy as np
import pandas as pd


lockins = pd.read_excel('C:/Users/limzi/OneDrive/Forecasting & Reporting/IBP/inventory_data_for_python.xlsx', sheet_name='Unit Demand Actual').rename(columns = {'Sku': 'SKU'})
lockins_f = lockins.melt(id_vars=['SKU', 'Product Name'], var_name='Date', value_name='Quantity').drop('Product Name', axis =1)
print('lockins_f \n', lockins_f.head())


sales_data = pd.read_excel('C:/Users/limzi/OneDrive/Forecasting & Reporting/IBP/inventory_data_for_python.xlsx', sheet_name='SalesQtyETS')
sales_data_f = sales_data.melt(id_vars=['SKU', 'Description'], var_name='Date', value_name='Quantity').drop('Description', axis =1).dropna()
print('sales_data_f \n', sales_data_f.head())

end_of_month = pd.read_excel('C:/Users/limzi/OneDrive/Forecasting & Reporting/IBP/inventory_data_for_python.xlsx', sheet_name='EOM1').rename(columns = {'SKU #': 'SKU'})
end_of_month_f = end_of_month.melt(id_vars=['SKU', 'Product Name'], var_name='Date', value_name='Quantity').drop('Product Name', axis =1)
print('end_of_month_f \n', end_of_month_f.head())

merge_table = end_of_month_f.merge(sales_data_f, how = 'left', on = ['SKU', 'Date'], suffixes=['EOM', 'Sales'])
merge_table = merge_table.merge(lockins_f, how = 'left', on = ['SKU', 'Date']).rename(columns = {'Quantity': 'LockIns'})
merge_table = merge_table.astype({'LockIns':'float64'})
merge_table = merge_table.sort_values(['SKU', 'Date'])
merge_table_small = merge_table[(merge_table['SKU'] == 7770) | (merge_table['SKU'] == 2010) | (merge_table['SKU'] == 7870)]

merge_table_small['Remainder'] = merge_table_small.groupby(by=['SKU', 'Date'])['QuantityEOM', 'QuantitySales', 'LockIns'].sum().apply(lambda x: x['QuantityEOM'].values[0] - x['QuantitySales'].cumsum() + x['LockIns'])


# Try to force lambda to obtain only the FIRST VALUE (occuring at the earliest date) of each SKU
test_output = merge_table_small.copy()
test_output = pd.merge(test_output, pd.DataFrame(series_test_merge), on='SKU' )
test_output['eom_quantity'] = test_output.groupby(['SKU']).sum().apply(lambda x: x['first_qty']*10.55 - x['QuantitySales'].cumsum() +  x['LockIns'].cumsum())

test_2 = merge_table_small.copy()
test_2.groupby(['SKU']).sum()
test_2.groupby(['SKU']).sum().apply(lambda s: s.cumsum(), axis = 1)

series_test_merge = test_output.groupby(by=['SKU']).nth(0)['QuantitySales']
series_test_merge = pd.DataFrame(series_test_merge).reset_index().rename(columns={'QuantitySales': 'first_qty'})

# Attempt to merge the 3 SKU quantities to master dataframe
# test_output.apply(map(test_output.groupby(by=['SKU']).first()['QuantityEOM']))

test_output.groupby(by=['SKU']).nth(0)


test_output


merge_table.loc[0,'projected_eom'] = merge_table.loc[0, 'QuantityEOM'] - merge_table.loc[0, 'QuantitySales'] + merge_table.loc[0, 'LockIns']


# In[107]:

merge_groupby = merge_table.groupby(['SKU', 'Date']).sum()
merge_groupby.apply(lambda x: x.QuantityEOM[0] - x.QuantitySales.cumsum() + x.LockIns)


# In[110]:

# merge_groupby.loc[1000, 'QuantityEOM']
merge_groupby_2 = merge_table.groupby(['SKU'])['QuantityEOM', 'QuantitySales', 'LockIns'].sum()
merge_groupby_2


# In[67]:

merge_groupby.loc[0,'projected_eom'] = merge_groupby.loc[0, 'QuantityEOM'] - merge_groupby.loc[0, 'QuantitySales'] + merge_groupby.loc[0, 'LockIns']
merge_groupby


# In[ ]:

def rolling_apply(group):
