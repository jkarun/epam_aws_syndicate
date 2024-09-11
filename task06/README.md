# The Goal Of This Task is...

To deploy a Lambda function triggered by a DynamoDB Stream on the 'Configuration' table. The Lambda function should track changes made to configuration items and store audit entries in the 'Audit' table.

The 'Configuration' data is the following:

```json
{
    "key": // string, key of the configuration item
    "value": // int
}
```


Example 1: no items stored in 'Configuration' table.
The following item has been created:
```json
{
    "key": "CACHE_TTL_SEC",
    "value": 3600
}
```
After the configuration item is saved to the table the following audit item
has been created in the 'Audit' table:
```json
{
   "id": // string, uuidv4
   "itemKey": "CACHE_TTL_SEC",
   "modificationTime": // string, ISO8601 formatted string
   "newValue": {
       "key": "CACHE_TTL_SEC",
       "value": 3600
   },
} 
```

Example 2: the following item has been stored in the 'Configuration' table:
```json
{
    "key": "CACHE_TTL_SEC",
    "value": 3600
} 
```
After the value of this configuration item has been changed
from 3600 to 1800, the audit item has been created
in the 'Audit' table with the following content:
```json
{
   "id": // string, uuidv4
   "itemKey": "CACHE_TTL_SEC",
   "modificationTime": // string, ISO8601 formatted string
   "updatedAttribute": "value",
   "oldValue": 3600,
   "newValue": 1800
} 
```


# Configuration trigger event request:

```json 
{
   "Records":[
      {
         "eventID":"97f346f54443196d55233e83d8b8f944",
         "eventName":"INSERT",
         "eventVersion":"1.1",
         "eventSource":"aws:dynamodb",
         "awsRegion":"eu-central-1",
         "dynamodb":{
            "ApproximateCreationDateTime":1726045348.0,
            "Keys":{
               "key":{
                  "S":"CACHE_TTL_SEC"
               }
            },
            "NewImage":{
               "value":{
                  "N":"3600"
               },
               "key":{
                  "S":"CACHE_TTL_SEC"
               }
            },
            "SequenceNumber":"9700002673137973216305",
            "SizeBytes":39,
            "StreamViewType":"NEW_AND_OLD_IMAGES"
         },
         "eventSourceARN":"arn:aws:dynamodb:eu-central-1:905418349556:table/cmtr-134cb1e3-Configuration-test/stream/2024-09-11T09:00:17.927"
      }
   ]
}```