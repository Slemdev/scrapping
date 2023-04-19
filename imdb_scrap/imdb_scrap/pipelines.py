# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from dotenv import load_dotenv
import os
load_dotenv()
ATLAS_KEY=os.getenv('ATLAS_KEY')

class ImdbScrapPipeline(object) :
    def __init__ (self):
        self.conn=pymongo.MongoClient(ATLAS_KEY)
        db=self.conn['top_250']
        self.collection =db['top_250_movies_test']
        
    def process_item(self,item,spider):
        self.collection.insert_one(dict(item))
        return item
    
