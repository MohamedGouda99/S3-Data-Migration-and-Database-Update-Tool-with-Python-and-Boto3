# Legacy to Production Data Transfer

This Python script is designed to help transfer data from a legacy AWS S3 bucket to a production AWS S3 bucket, while also managing PostgreSQL database records of the transferred files. The script utilizes the Boto3 library for AWS S3 operations and the Psycopg2 library for PostgreSQL database interactions.

## Prerequisites

Before using this script, make sure you have the following prerequisites in place:

AWS Credentials: Ensure that you have valid AWS credentials configured on your system to access both the legacy and production S3 buckets.

AWS S3 Buckets: Create two AWS S3 buckets - one for legacy data (legacys3-2023) and one for production data (prods3-2023).

PostgreSQL Database: Set up a PostgreSQL database and obtain the following details:

Host (DB_HOST)

Port (DB_PORT)

Database name (DB_NAME)

Username (DB_USER)

Password (DB_PASSWORD)



## Psycopg2: Install the Psycopg2 library to enable database connectivity. You can install it using pip:

```bash
pip install psycopg2

```


# Usage
Configure AWS Credentials: Ensure your AWS credentials are properly configured. You can do this by setting environment variables or using the AWS CLI aws configure command.

Set Environment Variables: Set the necessary environment variables for your PostgreSQL database connection. You can export these variables or set them in a .env file:
foobar.pluralize('goose')

```bash
export DB_HOST=<your_db_host>
export DB_PORT=<your_db_port>
export DB_USER=<your_db_user>
export DB_NAME=<your_db_name>
export DB_PASSWORD=<your_db_password>

```

# Run the Script: Execute the script using Python:

```
python script_name.py
```
The script will perform the following actions:

List objects in the legacy AWS S3 bucket (legacys3-2023).
Copy each object from the legacy bucket to the production AWS S3 bucket (prods3-2023), organizing them into a specific folder structure (e.g., avatar).
Optionally, update the file paths in the PostgreSQL database. You can add your own logic for database updates as needed.
Load the file paths from both S3 buckets into the PostgreSQL database.

## Note

This script is designed as a starting point and may require modifications to suit your specific use case.

Ensure that your AWS IAM user or role has the necessary permissions to perform S3 operations on the specified buckets.

Customize the folder structure and database update logic to match your requirements.

Handle any exceptions or errors as needed to ensure the reliability of the data transfer and database updates.