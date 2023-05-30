import pandas as pd
from bq_wrapper import BQ_Wrapper
import pipeline

def main():
    path = "data/Report Definitions - IHS MARKIT VIO REPORT.xlsx"

   ## meta = pd.read_excel(path, sheet_name="Example All Fleets All States", nrows=1)
    data = pd.read_excel(path, sheet_name="Example All Fleets All States", skiprows=10)

   ## meta_csv_path = path.replace(".xlsx", "-meta.csv")
    data_csv_path = path.replace(".xlsx", "-data.csv")

   ## meta_csv = meta.to_csv(meta_csv_path, index=False)
    data_csv = data.to_csv(data_csv_path, index=False)

   ## bq_meta = BQ_Wrapper(meta_csv_path, "IHS", "meta data")
    bq_data = BQ_Wrapper(data_csv_path, "IHS", "data")

    pipeline.run_pipeline_from_query("SELECT * FROM gcp-testing-387914.IHS.data", "gs//:test-out-bucket-0101011010")


if __name__ == "__main__":
    main()