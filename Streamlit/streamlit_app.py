from numpy import double
import streamlit as st
import pandas as pd
# from pandas import DataFrame, cut, to_numeric, concat

import numpy as np

import pymongo


#data = pd.read_csv("data.csv")
myclient = pymongo.MongoClient("mongodb://localhost:27017/",username='root',password='example')
mydb = myclient["docstreaming"]
category_col = mydb["category"]
product_col = mydb['product'] 

# read in the category and product documents as pandas dataframes
product_df = pd.DataFrame(list(product_col.find({})))
category_df = pd.DataFrame(list(category_col.find({})))

# merge dataframes to include categories in product dataframe
df = product_df.merge(category_df, 
                      left_on="category_id", 
                      right_on="id", 
                      how="left"
                      ).drop(columns=['_id_x', '_id_y'])

df['price'] = pd.to_numeric(df['price'])

# create price bucket bins
df_price_group = pd.DataFrame(pd.cut(df["price"], bins=range(0, 300, 5))
                           .apply(lambda x: "{}-{}".format(x.left, x.right))
                           ).rename(columns={'price':'price_bucket'})

df_combined = pd.concat([df, df_price_group], axis=1)
df_combined["isBestSeller"] = np.where(df_combined["isBestSeller"]==True, 1, 0)

group_price_bucket = (df_combined
                      .groupby("price_bucket")                     
                      )
group_category = df_combined.groupby("category_name")

# Distribution of Price Levels
df_price_count = pd.DataFrame(group_price_bucket["id"].count())
df_price_count.columns = ["item_count"]

st.header('Price Bucket Vs Item Count for Amazon Products')
st.bar_chart(df_price_count, y="item_count")


# Distribution of categories
df_category_count = pd.DataFrame(group_category["id"].count())
df_category_count.columns = ["item_count"]
df_category_count = df_category_count.sort_values(by="item_count", ascending=True)
print(df_category_count.head())

st.header('Category Bucket Vs Item Count for Amazon Products')
st.bar_chart(df_category_count)

# Below the price bucket chart add a input field for the ProductID
product_id = st.sidebar.text_input("ProductID:")
# #st.text(product_id)  # Use this to print out the content of the input field

# # if enter has been used on the input field 
if product_id:

    myquery = {"asin": product_id}
    # only includes or excludes
    mydoc = product_col.find( myquery , { "_id":0, "boughtInLastMonth": 0, "isBestSeller": 0, "imgUrl": 0, "reviews": 0})

    # create dataframe from resulting document
    df = pd.DataFrame(mydoc)

    # Add the table with a headline
    st.header("Output Product Details")
    table2 = st.dataframe(data=df) 
    

# # Below the fist chart add a input field for the CategoryNo
category_no = st.sidebar.text_input("CategoryNo:")
# #st.text(category_no)  # Use this to print out the content of the input field

# # if enter has been used on the input field 
if category_no:    
    myquery = {"id": category_no}
    mydoc = category_col.find( myquery)

    # create the dataframe
    df = pd.DataFrame(mydoc)

    # Add the table with a headline
    st.header("Output by CategoryNo")
    table2 = st.dataframe(data=df) 




