
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
  - [Visualizations](#visualizations)
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
Kafka is used as the buffer for queuing the data.  
Kafka recieives the data from the files, product and category, every time it is posted to the API.  
Two ingestion topics are created for the two JSON files, *ingest-product*, and *ingest-category*.

## Processing    
Spark Jupyter notebooks are using for stream processiong.  
The processing notebook */ApacheSpark/stream-src-kafka-dst-mongodb.ipynb* reads the stream from the ingestion topics and writes the transformed data to the Mongodb document store.  

## Storage  
Mongodb is used as the choice of store for storing the JSON data. Two collections are created for the two input data files, category and product.

## Visualization  
Streamlit is used for visualizing the reports.  
It is an open-source Python library that supports several different charting libraries. 

# Pipelines
- Explain the pipelines for processing that you are building
- Go through your development and add your source code

## Stream Processing  
The detailed stages of the stream processing are demonstrated in the image below:  
![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/stream_process.png)  

### Data Preparation  
- The Kaggle csv files in */dataset/input/* are transformed into JSON files using the script */client/transformer.py* and placed under */dataset/output/*

### API Creation  
  * Setup API
    - FastAPI is used to create the API.
    - Implementation is contained in the file */API_ingest/app/main.py*
        * It creates the schema for the the two JSON files, Category and AmazonProduct
        * Initializes the app and adds the routes for posting the data to API endpoints, /Category and /AmazonProduct
    - Test the app by running the command `uvicorn main:app --reload` from the folder */API-ingest/app/*
    - Upon successful running, the broswer should show a message `Hello World`
    ![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/start_app.PNG)
    ![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/start_app_browser.PNG)
  * Test API
    - Postman is used to send the JSON data records to the API endpoints
    - Test Product:
      ![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/postman_product.PNG)  
    - Test Category:
      ![alt text](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/postman_category.PNG)
    

### Buffer Data Stream  
- Setup Docker for Kafka
    * Kafka container is run by executing the command `docker-compose -f docker-compose-kafka.yml up`
- Create Topics for Kafka
    * Connect to the kafka shell. Using VSCode, you can use the docker blade to attach termial to shell
      ![attach_shell_image](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/attach_shell_to_kafka.png)
    * Navigate to the folder /op/bitnami/kafka/bin
    * Check if any topics exist by using `./kafka-topics.sh --list --bootstrap-server localhost:9092`
    * Create new topics for ingesting product and customer data streams using commands:
        * `./kafka-topics.sh --create --topic ingest-product --bootstrap-server localhost:9092`
        * `./kafka-topics.sh --create --topic ingest-category --bootstrap-server localhost:9092`
        ![kafka topics_created](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/kafka_topics_created.PNG)
- Test Kafka
    * Setup local consumer by running the command from kafka shell `./kafka-console-consumer.sh --topic ingest-product --bootstrap-server localhost:9092`
    *  While the consumer is waiting, go to file [main.py](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/API-Ingest/app/main.py) and make sure line 85 is un-commented
    *  Make sure that boostrap server is pointing to *localhost:9093* in line 98, `producer = KafkaProducer(bootstrap_servers='localhost:9093',acks=1)`
    *  Use the postman to post a JSON record of product and check if the consumer recieves it
      ![kafka_consumer_test](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/kafka_consumer_test.PNG)

### Deploy API_ingest to Docker  
- Add the files, [dockerfile](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/API-Ingest/dockerfile), and [requirements.txt](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/API-Ingest/requirements.txt), to instruct the build process of the dependencies to be installed and directories to be copied to docker container
- Make sure that boostrap server in file [main.py](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/API-Ingest/app/main.py) is pointing to *kafka:9092* in line 98, `producer = KafkaProducer(bootstrap_servers='kafka:9092',acks=1)`.  
  As this is required for the API-Ingest is moving from local windows client to the Docker network
- Create docker image for API_ingest by running command, `docker build -t api-ingest .`
- Once completed, use command `docker images` to see if the image is added to the list of docker images
- Start the kafka container
- Check the network for the Kafka container (in my case it's amazon-products-streaming_default)
  ![kafka_network](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/kafka_network.png)  
- Open a new terminal and execute, `docker run --rm --network amazon-products-streaming_default --name my-api-ingest -p 80:80 api-ingest`
- Once the API, API-Ingest is started in docker, test the kafka and API as was done in step __Buffer Data Stream__ . Make sure to change the port from *8000* to *80* in Postman.
    
### Processing Data Stream  
- Setup Spark and Jupter for Docker
    * Spark container is added to docker by running the command `docker-compose -f docker-compose-kafka-spark.yml up`
    * Once the container is running, go to view logs to get the token
    ![jupyter notebook token](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/jupyter_notebook_token.PNG)
    * Go to `localhost:8888` and input the token when asked for it. It should display two notebooks already present


### Storing Data Stream  
- Setup Mongodb in docker
    * Run `docker-compose -f docker-compose-kafka-spark-mongodb.yml up`
    * Go to `localhost:8081` and enter the admin and password as configured in yml file, under mongo-express
    * Create a Database called docstreaming and create a collection for category and product to store all the records from Spark streaming
      ![mongodb_collection](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/mongodb_database_collection.png)
- Connect Spark to MongoDB
    * Go to [stream-src-kafka-dst-mongodb.ipynb](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/ApacheSpark/stream-src-kafka-dst-mongodb.ipynb)
    * Note code block 8 adds a dataframe transformation to set the output table in MongoDB
    * Execute the notebook then go to Postman and post a record. Check to see that it appeared in the MongoDB collection properly
      ![mongodb doc added](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/mongodb_coll_doc_added.PNG)
- API Client Data Write
    * Clean up MongoDB table if you sent test record earlier
    * Use [api-client.py](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/client/api-client.py) to send the most recent trending video records
    * Multiple batches with all the records are stored in MongoDB
      ![multiple batches](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/message_batches.PNG)
      ![product docs complete](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/mongodb_product_docs.PNG)
## Visualizations  
- Setup Streamlit
    * Once the records are successfully loaded in the database, it's time to build a dashboard for end users
    * Run `pip install streamlit`, `pip install pymongo`
    * Run [streamlitapp.py](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/Streamlit/streamlit_app.py), copy the [ARGUMENTS] it provides and run it, then you will get the url if the browser didn't pop up automatically
    ![streamlit run](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/streamlit_run.PNG)
    * The reports will be rendered once streamlit successfully runs on browser
    ![streamlit visual](https://github.com/FaisalQ07/amazon_products_streaming/blob/main/images/streamlit.PNG)

# Conclusion
Write a comprehensive conclusion.
- How did this project turn out
- What major things have you learned
- What were the biggest challenges

# Follow Me On
Add the link to your LinkedIn Profile

# Appendix

[Markdown Cheat Sheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

***

Inspired by <a href="https://github.com/team-data-science/document-streaming" target="_blank">document streaming project</a>, if you have any comments or questions, feel free to reach out
