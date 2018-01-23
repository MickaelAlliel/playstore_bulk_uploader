# Play Store Bulk APK Uploader

**Written by:** Mickael Alliel
**Last Edit:** 21/02/2017
**License:** MIT License


## HOW TO USE:

**THIS SCRIPT WORKS WITH PYTHON 3.6 ! PLEASE MAKE SURE THE CORRECT VERSION IS INSTALLED !**

## Requirements
* google-api-python-client

## Usage
```
python bulkupdate.py
python bulkupdate.py -c path_to_csv
```

By default the CSV should be called "bulkupdate.csv" and in the same directory as the script

If you want to organize the files in folders, in the csv you'll need to use relative path, ie: "/apks/com.android.test/app_v1.0.apk"

In order to make use of the API you need a JSON file with the private key to the ServiceAccount authorized to upload
You can configure everything you need here :
https://console.developers.google.com/projectselector/apis/credentials
"""

**For more info, look at the commented code in the script**