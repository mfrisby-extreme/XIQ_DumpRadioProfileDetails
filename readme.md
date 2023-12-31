# XIQ_DumpRadioProfileDetails
### DumpRadioProfileDetails.py
## Description
This script will pull all of the radio profiles that are configured in XIQ, including data which is stored in different API calls, and output the results to a CSV file


## Needed files
Download all of the files in the repository and place them into a folder somewhere on your PC.

The files located in the 'lib' folder are required for the execution of the main python script.  They contain the base XIQ python api library and the logging functions.


### Logging in

If you have an XIQ authorization bearer token, you may edit the `DumpRadioProfilesDetail.py` script and paste the token as the value for `XIQ_API_token` encapsulated in either single or double quotes.

For example:
```commandline
XIQ_API_token = '<insert_your_bearer_token_string_here>'
```

If no bearer token is present in the script, the script will prompt the user for XIQ credentials.
>Note: your password will not show on the screen as you type

## Running the script

Ensure you have the needed python libraries installed per the requirements.txt file.

if you use the git tool, you can install the needed libraries with the following command
```commandline
pip install -r requirements.txt
```

After ensuring that you have the required libraries, you can execute the script as follows

Open a terminal to the location of the script and run this command.
```
python DumpRadioProfileDetails.py
```

The script will execute and generate a csv file called (by default) "radio_profiles.csv" in the same directory adjacent to the script file.  See the Runtime Flags sections for information on how to change the resulting csv file name.

### Runtime Flags
There is an optional flag that can be added to the script when running.
```
--external
```
This flag will allow you to connect to additional external XIQ accounts that your username is part of. After logging in with your XIQ credentials the script will give you a numeric option of each of the XIQ instances you have access to. Choose the one you would like to use.
```
--csv_file
```
Use this flag to specify a 

You can add one or more of these flags when running the script.
```
python XIQ_CSV_onboard.py --external --csv_file mycsv.csv
```
## Requirements
There are additional modules that need to be installed in order for this script to function. They are listed in the requirements.txt file and can be installed with the command 'pip install -r requirements.txt' if using pip.