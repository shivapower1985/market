import azure.functions as func
import datetime
import json
from datetime import date, timedelta
import os
from internal.parse import parser
from helpers.requesthelper import download 
from processor.process import processdf
import logging


app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 9 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def MyCronFunction(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    logging.info('Timer function triggered')
    market_no="1000"
    try:
        # Define the path to your internal folder
        config_path = os.path.join("internal", "config.json")
        
        # Open and load json file
        with open(config_path, "r") as f:
            config = json.load(f)
        
        #raw url from config
        url=config[market_no]['url']
        
        #get date
        yestarday=date.today()-timedelta(days=1)

        #initialize class to parse url
        p=parser(yestarday.strftime("%Y%m%d"), url)
        parsed_url=p.parse_url()
        
        #download source data and return dataframe
        status_code, dataframe=download(parsed_url)
        if status_code==200:
            #print(dataframe.head())
            result=processdf(dataframe, market_no)
        else:
            logging.info("No response from URL, check URL")
            
    except Exception as e:
        logging.error(f"Exception occurred: {e}")