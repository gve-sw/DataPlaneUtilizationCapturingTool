
# DataPlaneUtilizationCapturingTool
A python script to monitor and capture dataplane utilisation of organisation devices via SSH and storing the captured data in the form of log or csv or both.

The python "start_capture.py" script will establish remote shell via SSH protocol of the targeted device/devices from an different device.
the command will be executed periodically in interval of seconds and the output is captured in the form of log file or comma seperated value (csv) file.
The capturing will be terminated once the current session is completed or disconnected or terminated. Logs will be created based on the current date with following filenaming convention `device-alias-name`-`timestamp-in-yyyy-mm-dd`.`extension-either-log-or-csv` under the logs folder.

## Contacts:
* Raveesh Malyavantham V (rmalyava@cisco.com)

## Solution Components
* Python3
* Paramiko (ssh library)
* Monitored command `show platform hardware qfp active datapath utilization`

## Target device
* ISR4K series (ISR4351)

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

## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
