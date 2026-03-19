import requests
import pandas as pd
from io import StringIO


def download(parsed_url):
    df=None
    response=requests.get(parsed_url, verify=False)
    if response.status_code==200:
        # Convert bytes → string
        csv_text = response.content.decode("utf-8")
        # Wrap string in StringIO so pandas can read it like a file
        df = pd.read_csv(StringIO(csv_text))
        return response.status_code,df
    else:
        print(f'The status code is {response.status_code}')
        return response.status_code, df

    
    #return response

