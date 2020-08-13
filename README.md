# ase-apis
Sample scripts (python) to work with the AppScan Enterprise (ASE) APIs.

The heart of the project is commonLib.py and aseLib.py.  
Common.py is responsible for parsing the command line arguments or for processing the config.json file.

#### aseLib.py
This module exports the `ASELib` object which is a convenient wrapper for generating `get` and `post` requests.  
It will automatically log into ASE and will relogin if the response is "unauthorzied".  
It sets the correct session ID and avoid the need to mess around with the `asc_xsrf_token` header.

## Dependencies
This project depends on [Requests](https://requests.readthedocs.io/en/master/)
Make sure it is installed before running the scripts

## API Keys
The recommended method of generating REST calls is to use API Keys rather than actual user name and password.  
In ASE, however, the generation of API Keys is done via REST APIs. To generate those run this command:
```
> py aseApiKey.py Username=<username> Password=<password>

>{'keyId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'keySecret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'createdAt': '9999-99-99 99:99:99.9999'}
```
You can then set the KeyId and KeySecret into the config.json file:
>{  
>&nbsp;&nbsp;"ase" : {  
>&nbsp;&nbsp;&nbsp;&nbsp;"Username":"",  
>&nbsp;&nbsp;&nbsp;&nbsp;"Password":"",  
>&nbsp;&nbsp;&nbsp;&nbsp;"KeyId":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  
>&nbsp;&nbsp;&nbsp;&nbsp;"KeySecret":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  
>&nbsp;&nbsp;},  
>&nbsp;&nbsp;"host":"https://<ase_host_name>:<ase_host_port>"  
>}


If you prefer, you can set the user name and password directly into the config file, however this is not recommneded.  
While you're at it, go ahead and add the host name and port of your ASE instance into the config file.
