# You need this to use FastAPI, work with statuses and be able to end HTTPExceptions
from fastapi import FastAPI, status, HTTPException
 
# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Needed for json.dumps
import json

# Both used for BaseModel
from pydantic import BaseModel

from datetime import datetime
from kafka import KafkaProducer, producer



# Create class (schema) for the JSON
# Date get's ingested as string and then before writing validated
class Category(BaseModel):
    id: int
    category_name: str

class AmazonProduct(BaseModel):
     asin: str
     title: str
     imgUrl: str
     productURL: str
     stars: float
     reviews: int
     price: float
     listPrice: float
     category_id: int
     isBestSeller: bool
     boughtInLastMonth: int
     date: str



# This is important for general execution and the docker later
app = FastAPI()

# Base URL
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/Category")
async def post_categories_item(item: Category):
     print("Message received")
     try:
          json_of_item = jsonable_encoder(item)
          # Dump the json out as string
          json_as_string = json.dumps(json_of_item)
          print(json_as_string)
          produce_kafka_string(json_as_string, 'category')
          return JSONResponse(content=json_of_item, status_code=201)
     except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)

# Add a new Amazon Product
@app.post("/AmazonProduct")
async def post_products_item(item: AmazonProduct): #body awaits a json with invoice item information
    print("Message received")
    try:
        # Evaluate the timestamp and parse it to datetime object you can work with
        date = datetime.strptime(item.date, "%d/%m/%Y %H:%M")

        print('Found a timestamp: ', date)

        # Replace strange date with new datetime
        # Use strftime to parse the string in the right format (replace / with - and add seconds)
        item.date = date.strftime("%d-%m-%Y %H:%M:%S")
        print("New item date:", item.date)
        
        # Parse item back to json
        json_of_item = jsonable_encoder(item)
        
        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)
        print(json_as_string)
        
        # Produce the string
        produce_kafka_string(json_as_string, 'product')

        # Encode the created customer item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)
    
    # Will be thrown by datetime if the date does not fit
    # All other value errors are automatically taken care of because of the InvoiceItem Class
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)
        

def produce_kafka_string(json_as_string, type):
    # Create producer
        producer = KafkaProducer(bootstrap_servers='localhost:9093',acks=1)
        
        # Write the string as bytes because Kafka needs it this way
        if type == 'product':
             producer.send('ingest-product', bytes(json_as_string, 'utf-8'))
        elif type == 'category':
             producer.send('ingest-category', bytes(json_as_string, 'utf-8'))
        producer.flush() 