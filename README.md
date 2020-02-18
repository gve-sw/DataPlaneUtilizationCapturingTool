# DataPlaneUtilizationCapturingTool
Script to monitor dataplane utilisation of organisation devices via SSH and capture the utilization in the log file.

#### Setting up Virtual Environment
creating an new python virtual environment
```sh
$ python3 -m venv venv
```

Activating the Environment
```sh
$ source venv/bin/activate
```

Installing the required or dependent modules
```sh
$ pip install -r requirements.txt
```

#### Adding device information for capturing the dataplane utilization

Open `devices.py` and update the `DEVICE_LIST` to add device information for monitoring. Its a list of dictionary that contains device information

``` python
[
...
{
	"alias": "<device alternative name for logging>",
    "host": "<ip-address/hostname>",
    "username": "<username>",
    "password": "<password>",
    "interval" : "<seconds in interval for monitoring>"
},
...
]
```

run the `start_capture.py` script to start monitoring the devices. The captured log will be stored in the logs directory.
``` sh
$ python start_capture.py
```

To stop the script from capturing the utilization, press `^c` or `control + c` buttons.