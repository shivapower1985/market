In this project day ahead locational marginal pricing (LMPs) data for NYISO (NewYork ISO) is scrapped from 
"https://mis.nyiso.com/public/csv/damlbmp/{date}damlbmp_zone.csv"
Sample url usage: "https://mis.nyiso.com/public/csv/damlbmp/20260315damlbmp_zone.csv"

The data is fetched from the source on daily basis and it is processed and pushed into the Azure storage location as ".Parquet".

The processed data is partitioned as day.

The code was developed using Python 3.12 and deployed to azure function scheduled triggers where the function will be cron triggered every day at 9AM UTC.

Some basic headsup to do it, 
1. Make sure you do pip to install , azure-functions, azure-storage-blob and other additional packages

2. Initialize your project using
func init MyFunctionProj --worker-runtime node

3. create a new function using time trigger using 
func new --name MyCronFunction --template "TimerTrigger"

4. use "func start --verbose" for local testing and use local.settings.json for local testing. 
Make sure a storage emulator is enabled or set the "AzureWebJobsStorage" option with your storage connection string information in local.settings.json.

5. Deploy the Azure function: Before deploying make sure you have logged in az login in your terminal. 

az functionapp create
  --resource-group <provide resource group name here>
  --consumption-plan-location <provide location here>
  --runtime python
  --runtime-version 3.12
  --functions-version 4
  --name <provide your function name here>
  --storage-account <provide storage account to hold your artifacts information here>
  --os-type Linux

