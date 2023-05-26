import pandas as pd
from bq_wrapper import BQ_Wrapper

def main():
    path = "data/Report Definitions - IHS MARKIT VIO REPORT.xlsx"
    meta = pd.read_excel(path, sheet_name="Example All Fleets All States", nrows=7)
    data = pd.read_excel(path, sheet_name="Example All Fleets All States", skiprows=10)

    meta_csv = meta.to_csv()
    data_csv = data.to_csv()

    bq_meta = BQ_Wrapper(meta, "IHS", "meta data")
    bq_data = BQ_Wrapper(meta, "IHS", "data")



if __name__ == "__main__":
    main()