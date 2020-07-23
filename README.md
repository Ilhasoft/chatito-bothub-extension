# Chatito bothub extension <img src="https://push.al/wp-content/uploads/2020/02/avatar4.png" width="25">
> An automated use of the [bothub API](https://api.bothub.it/) by python coding.

[![Python Version](https://img.shields.io/badge/python-v3.8-blue)](https://www.python.org/)
[![License GPL-3.0](https://img.shields.io/badge/license-%20GPL--3.0-yellow.svg)](https://github.com/Ilhasoft/bothub-engine/blob/master/LICENSE)

Dependencies
---
- [Python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- [Python requests](https://pypi.org/project/requests/)

Installation
-------
First of all, clone this repository using the following command:

    $ git clone https://github.com/Ilhasoft/chatito-bothub-extension.git
    $ cd chatito-bothub-extension

Create a virtual environment using python:

	$ python -m venv env
    $ source env/bin/activate

Install the dependences

	$ pip install -r requirements.txt

### Basic virtual environment commands:
To enter in the virtual environment:

	$ source env/bin/activate

To exit from the virtual environment:

	$ deactivate

Usage
---
First, go to .env file and fill the variables with the respective values:

| Variable | Example value | Explanation |
| --- | --- | --- |
| BOTHUB_API_URL | https://api.bothub.it/v2 | Base url of the bothub api version that you gonna use. |
| REPOSITORY_UUID | d68da147-9aff-42b7-8062-b16f8a543ac2 | The repository UUID.  You can get it in your network browser log. |
| REPOSITORY_VERSION_ID | 373 | The repository version id.  You can get it in your network browser log. |
| ACCOUNT_API_TOKEN | ab245d24bcv845c7a73e34d17f9843e6346058c9 | Your account api token that created when you create a bothub account. You can get it in your network browser log. |

After filling the environment variables you must to enter in the virtual environment...

	$ source env/bin/activate

And call the [main.py](/main.py) code to use the [functions](/tutorial.md).

Contributing
---
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Copyright
---
See the [LICENSE](/LICENSE) for details.
