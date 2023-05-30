from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd

class BQ_Wrapper:
    def sanitize_field_name(self, field_name):
        sanitized_name = ''.join(c if c.isalnum() else '_' for c in field_name)
        
        if sanitized_name[0].isdigit():
            sanitized_name = 'f' + sanitized_name

        if len(sanitized_name) > 300:
            sanitized_name = sanitized_name[:300]
        
        return sanitized_name

    def __init__(self, data_path, dataset_name, table_name):

        self.data_path = data_path
        
        client = bigquery.Client()

        dataset_ref = client.dataset(dataset_name)
        try:
            client.get_dataset(dataset_ref)
        except NotFound:
            dataset = bigquery.Dataset(dataset_ref)
            dataset = client.create_dataset(dataset)

        # Create the table if it doesn't exist
        table_ref = dataset_ref.table(table_name)
        try:
            client.get_table(table_ref)
        except NotFound:
            df = pd.read_csv(data_path, nrows=1)
            schema = []
            
            for column_name, column_type in df.dtypes.iteritems():
                print(f"\nColumn Type: {column_type.name} Table: {table_name}")

                sanitized_name = self.sanitize_field_name(column_name)

                if column_type.name == 'object':
                    bq_field_type = 'STRING'
                else:
                    bq_field_type = bigquery.enums.SqlTypeNames[column_type.name.upper()]

                schema.append(bigquery.SchemaField(sanitized_name, bq_field_type))

            table = bigquery.Table(table_ref, schema=schema)
            table = client.create_table(table)


        
        with open(data_path, mode="rb") as file:
            job_config = bigquery.LoadJobConfig(skip_leading_rows=1)  

            job = client.load_table_from_file(file, table_ref, job_config=job_config)
            job.result()
            
            if job.state == "DONE":
                print(f"\n\nData uploaded to {dataset_name}.{table_name} successfully.\n\n")
            else:
                print("Data upload to BigQuery failed.")
                print(job.errors)

