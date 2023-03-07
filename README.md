# Weather API

In this repository, we are building a Data Engineering pipeline. This includes the following steps:

* Data Ingestion: We will read weather data and crop yield from multiple files

* Data Analysis: We will compute the averages on max and min temperature and sum of precipitation

* Data Storage: The raw data, along with the processed analysis results, will be stored in a relational DB such that it can be queried for use in downstream tasks

* REST API: We will build an API in Django with endpoints for users to run queries on and get the results in JSON

## Installation

### Python Environment Setup

A Python virtual environment can be created using the following commands:

```Python
python3 -m venv env_name
source env_name/bin/activate
```

In this environment, required dependencies can be installed using the `requirements.txt` file as follows

```
pip3 install install -r requirements.txt
```

### Data Ingestion Pipeline

Once the requirements are installed, the data ingestion, computation and storage pipeline can be run

```
python3 utilities/ingest_data.py --weather weather_data_directory --crop crop_data_directory
```

`--weather` flag will allow users to enter the location of weather data and `--crop` flag will allow users to enter the location of crop yield data. At least one of the two flags are required to run this phase successfully.

### Django Server and API Endpoints

The Django server can then be run using

```
python3 src/manage.py runserver
```

Once the server runs successfully, the API endpoints can be accessed at

```
localhost:8000/api/weather
localhost:8000/api/weather/stats
localhost:8000/api/crops
```

Details of the API endpoints (created using Swagger) can be found at

```
localhost:8000/api/schema
localhost:8000/api/schema/docs
```

### Data Filter

Filters on the weather data include:

`station_id` (string) to get a specific station
`date` (numeric) to filter for specific date

Filters on weather stats include:

`station_id` (string) to get a specific station
`year` (string) to filter for a specific year

```
localhost:8000/api/weather?station_id='USC00110072'&date=19850101
```

## Testing

Unit test cases can be run with the following command

```
python3 src/manage.py test
```

## Logs

The data ingestion process also uses logs, which can be found in the `logs` directory, to highlight time taken to complete each step. Errors can also be traced here.

## Next Steps

This system can be deployed on the cloud to make it scalable and robust. One way to do this is:

* AWS Relation Database, which provides SQL server, for a relational DB to store ingested data and analysis results

* Django application can be deployed to Elastic Beanstalk, which enables hosting a Python environment

* Regular data ingestion pipeline can be scheduled using AWS Lambda or on an Elastic Compute Cloud

* With Elastic Load Balancer and Cloud Watch, we can scale our application without any hassle and keep track of the processes to make it more resistant to failure.

## License

[MIT](https://choosealicense.com/licenses/mit/)