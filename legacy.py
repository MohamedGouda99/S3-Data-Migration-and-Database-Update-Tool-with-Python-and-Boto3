import boto3
import psycopg2
import os
from botocore.exceptions import NoCredentialsError


# AWS S3 bucket names
legacy_bucket_name = 'legacys3-2023'
production_bucket_name = 'prods3-2023'



# Initialize AWS S3 client
s3 = boto3.client('s3')



def move_legacy_to_production():
    try:
        # List objects in the legacy bucket
        response = s3.list_objects_v2(Bucket=legacy_bucket_name)
        if 'Contents' in response:
            legacy_objects = response['Contents']

            for legacy_object in legacy_objects:
                # Get the object key (path)
                legacy_object_key = legacy_object['Key']

                # Extract the folder and filename from the object key
                folder, filename = legacy_object_key.split('/')

                # Define the new folder name in the production bucket (e.g., "avatar")
                new_folder_name = 'avatar'

                # Construct the destination object key in the production bucket
                production_object_key = f"{new_folder_name}/{filename}"

                # Copy the object from legacy to production S3
                s3.copy_object(
                    CopySource={'Bucket': legacy_bucket_name, 'Key': legacy_object_key},
                    Bucket=production_bucket_name,
                    Key=production_object_key
                )

                # Update the path in the "proddatabase" database (if needed)
                # You can add your database update logic here

                print(f"Transfer successful: {legacy_object_key} to {production_object_key}")

    except NoCredentialsError:
        print("AWS credentials not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def load_s3_paths(s3_bucket_name, cursor):
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')

        # List objects in the specified S3 bucket
        s3_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name)

        # Extract S3 file paths
        s3_paths = [obj['Key'] for obj in s3_objects['Contents']]

        # Insert S3 paths into the PostgreSQL table
        for s3_path in s3_paths:
            cursor.execute("INSERT INTO s3_paths (s3_path) VALUES (%s)", (s3_path,))
        
        # Commit the changes
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error loading S3 paths from {s3_bucket_name}: {e}")



    

if __name__ == "__main__":
    move_legacy_to_production()
    prod_bucket_name = 'prods3-2023'
    legacy_bucket_name = 'legacys3-2023'

    # PostgreSQL RDS credentials
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_user = os.environ.get('DB_USER')
    db_name = os.environ.get('DB_NAME')
    db_password = os.environ.get('DB_PASSWORD')

    # Establish a connection to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor
        cursor = conn.cursor()

        # Load paths from 'prods3-2023'
        load_s3_paths(prod_bucket_name, cursor)

        # Load paths from 'legacys3-2023'
        load_s3_paths(legacy_bucket_name, cursor)

        # Query the database to fetch and print the data
        cursor.execute("SELECT * FROM s3_paths")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        # Close the database connection
        cursor.close()
        conn.close()

   
