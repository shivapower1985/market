from datetime import datetime
import pandas as pd
from azure.storage.blob import BlobServiceClient
import logging

def processdf(df, market_no):
    #print(df.columns)
    #print(df.head())
    # Rename specific columns and apply directly
    df.rename(columns={
        "Time Stamp": "date_time",
        "Name": "settlement_point",
        "PTID": "p_node",
        "LBMP ($/MWHr)": "lmp",
        "Marginal Cost Losses ($/MWHr)": "mlc",
        "Marginal Cost Congestion ($/MWHr)": "mcc"
    }, inplace=True)

    #print(df.head())

    # Convert column to datetime
    df["date_time"] = pd.to_datetime(df["date_time"], format="%m/%d/%Y %H:%M")
    df["date_time"] = df["date_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["market_id"] = market_no

    #print(df.head())

    single_dt=df["date_time"].iloc[0]
    dat = datetime.strptime(single_dt, "%Y-%m-%d %H:%M:%S")
    filename=f"{dat.strftime("%Y-%m-%d")}.parquet"
    #print(filename)

    # Save DataFrame to Parquet file
    df.to_parquet(filename, engine="pyarrow", index=False)

    # Connect to ADLS (Blob Storage)
    connection_string = "paste your storage connection string here"   # from Azure portal
    container_name = "your container name"
    blob_name = f"{market_no}/day={dat.strftime("%Y-%m-%d")}/{filename}"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    # 3. Upload file
    with open(filename, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)

    logging.info("upload successful")
    result="SUCCESS"
    return result
