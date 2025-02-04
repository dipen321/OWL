Database Schema Design
----------------------

All data from the CSV is stored in a single table named `stock_data`. Each row in the table represents one record from the CSV file.

**Table: stock_data**

-   **id**: Integer, Primary Key, Auto-increment
-   **name**: String\
    *Example*: `"Amazon Com"`, `"Alphabet Class C"`
-   **asof**: Date\
    *Example*: `"2017-10-04"`
-   **volume**: Integer\
    *Example*: `50547040`
-   **close_usd**: Float\
    *Example*: `48.272498`
-   **sector_level1**: String\
    *Example*: `"CONSUMER CYCLICALS"`, `"Technology"`
-   **sector_level2**: String\
    *Example*: `"Retailers"`, `"Software & IT Services"`

All columns directly mirror the fields in the CSV file. This design keeps both static asset information (name, sectors) and dynamic daily data (asof, volume, close_usd) in one place.

* * * * *

Setup and Running Instructions
------------------------------

### Prerequisites

-   **Python 3.11+** (or a compatible version)
-   **SQLite** (bundled with Python)
-   **pip** (for installing dependencies)

### Installation Steps

1.  **Clone or Download the Repository**

    Ensure your project directory contains the following files:

    -   `models.py` (ORM model definition)
    -   `etl.py` (ETL pipeline)
    -   `api.py` (Flask API)
    -   `stock_data.csv` (CSV file with the raw stock data)
    -   `README.md` (this documentation)
    -   `requirements.txt` (dependencies list)

2.  **Install Dependencies**

    Ensure your `requirements.txt` file includes the following:

    `Flask==2.2.2
    SQLAlchemy==1.4.46`

    Then run:

    `pip install -r requirements.txt`

3.  **Run the ETL Pipeline**

    This script reads the CSV data and loads it into the SQLite database.

    `python etl.py`

    You should see:

    `ETL completed successfully.`

4.  **Start the API Server**

    Run the Flask API:

    `python api.py`

    The terminal should display a message similar to:


    `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

* * * * *

API Endpoints
-------------

The API is built with Flask and uses SQLAlchemy to access the `stock_data` table.

### 1\. GET All Stock Data with Optional Filtering

**Endpoint:**

`GET /stocks`

**Description:**\
Retrieves all stock data from the `stock_data` table. You can optionally filter by:

-   **name:** Returns only records where the asset name contains the given substring.
-   **sector_level1:** Returns only records matching the primary sector.
-   **sector_level2:** Returns only records matching the secondary sector.

**Examples:**

-   **Get All Stock Data:**


    `curl "http://127.0.0.1:5000/stocks"`

-   **Filter by Name (e.g., "Amazon"):**


    `curl "http://127.0.0.1:5000/stocks?name=Amazon"`

-   **Filter by Sector (e.g., Primary Sector "Technology"):**


    `curl "http://127.0.0.1:5000/stocks?sector_level1=Technology"`

### 2\. GET All Records for a Specific Asset

**Endpoint:**


`GET /stocks/<asset_name>`

**Description:**\
Retrieves all daily records (ordered by date) for the specified asset name. The asset name must match exactly.

**Example:**

-   **Get Data for "Amazon Com":**


    `curl "http://127.0.0.1:5000/stocks/Amazon%20Com"`

    *(Note: URL-encode spaces as `%20`.)*

### 3\. GET Cumulative Returns for a Specific Asset

**Endpoint:**


`GET /stocks/<asset_name>/cumulative_returns?start=YYYY-MM-DD&end=YYYY-MM-DD`

**Description:**\
Calculates the cumulative return for the specified asset between the given start and end dates. 
**Required Query Parameters:**

-   **start:** Start date in `YYYY-MM-DD` format.
-   **end:** End date in `YYYY-MM-DD` format.

**Example:**

-   **Calculate Cumulative Returns for "Amazon Com" from 2017-10-01 to 2017-10-31:**


    `curl "http://127.0.0.1:5000/stocks/Amazon%20Com/cumulative_returns?start=2017-10-01&end=2017-10-31`


----------------------


**1\. How might the solution scale with increasing data volume?**

-   **Database Upgrade:**\
    As data grows, switching from SQLite to a more scalable database system like PostgreSQL or MySQL would help handle larger datasets and higher query loads.

-   **Caching:**\
    Implementing caching for frequently requested queries (using a tool like Redis) can reduce database load and improve response times.


**2\. What might you do with more time?**

-   **Testing:**\
    Build unit and integration tests to ensure the reliability and correctness of both the ETL pipeline and the API endpoints.

-   **Error Handling and Logging:**\
    Implement more detailed error handling and logging to debug and monitor in a production environment.

-   **Deployment Improvements:**\
    Consider using Docker and using Kubernetes to streamline deployment and scaling