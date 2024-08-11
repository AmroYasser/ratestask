# Ratestask Application

This repository contains the Ratestask application which consists of a Flask API and a PostgreSQL database, containerized using Docker and orchestrated with Docker Compose.

## Prerequisites

Before you begin, ensure you have installed the following on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/AmroYasser/ratestask.git
cd ratestask
```

### Build and run

Build and run docker-compose using the following command:

```bash
docker-compose up --build -d
```

### Run tests

Use the following command to run tests:

```bash
docker exec -it ratestask-web-1 python test_app.py
```

## Accessing the API endpoint

The Flask application provides a RESTful API that can be accessed via HTTP requests. Below are the details on how to interact with the available endpoint:

- **Get Rates:**
    - Description: Retrieve shipping rates based on date range, origin, and destination.
    - URL: /rates
    - Method: GET
    - Query Parameters:
        - date_from: Start date for the rate query (format: YYYY-MM-DD)
        - date_to: End date for the rate query (format: YYYY-MM-DD)
        - origin: Origin port code or region slug
        - destination: Destination port code or region slug
    - Example request:
        ```bash
        curl "http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NLRTM"
        ```
    - Response:
        ```json
        [
            {
                "average_price": "882.0000000000000000",
                "day": "Fri, 01 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "882.0000000000000000",
                "day": "Sat, 02 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "882.0000000000000000",
                "day": "Tue, 05 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "882.0000000000000000",
                "day": "Wed, 06 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "882.0000000000000000",
                "day": "Thu, 07 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "832.0000000000000000",
                "day": "Fri, 08 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "832.0000000000000000",
                "day": "Sat, 09 Jan 2016 00:00:00 GMT"
            },
            {
                "average_price": "832.0000000000000000",
                "day": "Sun, 10 Jan 2016 00:00:00 GMT"
            }
        ]
        ```


## Notes
- This task took me 2.5 hours to complete