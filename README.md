
# Stream Processing of Amazon Products Information to Identify Trends and Patterns 

# Introduction & Goals
- The objective of this project is to build a data processing pipeline that could utillize the modern tech stack for data engineering.  
  The tech stack platform comprises of:
    * API connecting to the data source.
    * Buffer, to persist the data temporarily until they are ready to be processed
    * Processing framework, a distributed system for parallel data processing and fault tolerance
    * Storage, to store the processed data
    * Vizualization tool, to create interactive reports where stakeholders can explore data, drill down into details, and gain insights by interacting with the visualizations
  

- To achieve the objective, Amazon dataset is taken from the open source platform Kaggle. The dataset comprises of two files, amazon categories and products.
  Together, these files provide information regarding the sales, ratings, prices of the products based on their categories.
  The goal of using this dataset is to:
    * Analyse the distribution of price levels for products sold
    * Analyse the distribution of categories for products sold
    * Analyse the average price for each category

 - In order to process that data and provide the reports for analysis, following tools are used:
   * [API-Ingest](#connect)
   * [Kafka](#buffer)
   * [Spark](#processing)
   * [Mongodb](#storage)
   * [Streamlit](#visualization) 
  
- Write this like an executive summary
  - With what data are you working
  - What tools are you using
  - What are you doing with these tools
  - Once you are finished add the conclusion here as well

# Contents

- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Client](#client)
  - [Connect](#connect)
  - [Buffer](#buffer)
  - [Processing](#processing)
  - [Storage](#storage)
  - [Visualization](#visualization)
- [Pipelines](#pipelines)
  - [Stream Processing](#stream-processing)
    - [Storing Data Stream](#storing-data-stream)
    - [Processing Data Stream](#processing-data-stream)
  - [Batch Processing](#batch-processing)
  - [Visualizations](#visualizations)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Follow Me On](#follow-me-on)
- [Appendix](#appendix)


# The Data Set
- The dataset is taken from the Kaggle. It includes the sales data for Amazon taken from Sept 2023.
   Dataset can be found [here](https://www.kaggle.com/datasets/asaniczka/amazon-products-dataset-2023-1-4m-products/data?select=amazon_products.csv)  
    The Amazon dataset was chosen for the following factors:
    * The dataset appears to be substantial, with over 1.4 million products.
    * The dataset contains information about Amazon products, making it a real-world dataset with diverse attributes.
       Working with real-world data can help ensure that the data pipeline is robust and can handle the complexities and variations present in actual business datasets. 

# Used Tools
- Explain which tools do you use and why
- Below is the platform design capturing the various tools that build the data pipeline:
 ![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/platform_design.png)
- How do they work (don't go too deep into details, but add links)
- Why did you choose them
- How did you set them up

## Client  
Client functionality includes the .csv files downloaded from the Kaggle and placed in the repository folder */dataset/input*.    
The python script */client/transformer.py* transforms the csv data into JSON format.  
The JSON data is then posted to the API endpoint using the python script */client/api-client.py*

## Connect 
API-Ingest, the connect functionality, upon recieving the data from the client, triggers a kafka producer module to stream the data to the buffer.

## Buffer  
Kafka, is used as the buffer for queuing the data.  
Kafka recieives the data from the files, product and category, every time it is posted to the API.  
Two ingestion topics are created for the two JSON files, *ingest-product*, and *ingest-category*.

## Processing    
Spark Jupyter notebooks are using for stream processiong.  
The processing notebook */ApacheSpark/stream-src-kafka-dst-mongodb.ipynb* reads the stream from the ingestion topics and writes the transformed data to the Mongodb document store.  

## Storage
## Visualization

# Pipelines
- Explain the pipelines for processing that you are building
- Go through your development and add your source code

## Stream Processing
### Storing Data Stream
### Processing Data Stream
## Batch Processing
## Visualizations

# Demo
- You could add a demo video here
- Or link to your presentation video of the project

# Conclusion
Write a comprehensive conclusion.
- How did this project turn out
- What major things have you learned
- What were the biggest challenges

# Follow Me On
Add the link to your LinkedIn Profile

# Appendix

[Markdown Cheat Sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
