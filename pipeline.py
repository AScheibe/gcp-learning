import apache_beam as beam 
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.runners.runner import PipelineState

def run_pipeline_from_query(source, out):
    pipeline_options = PipelineOptions(
        runner="DataflowRunner",
        project="gcp-testing-387914",
        region="us-central1",
        stagingLocation="gs://test-staging-bucket-0101011010",
        tempLocation="gs://test-temp-bucket-0101011010",
    )

    pipeline = beam.Pipeline(options=pipeline_options)

    input_data = (pipeline | "Read from BigQuery" >> beam.io.Read(beam.io.BigQuerySource(query=source, use_standard_sql=True)) 
                  | "Remove Duplicates" >> beam.Distinct() 
                  | "Write to GCS" >> beam.io.WriteToText(out, file_name_suffix=".csv"))

    pipeline.run()


