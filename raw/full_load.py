# %%
import boto3
import pandas as pd
import sqlalchemy
from tqdm import tqdm


# %%
def save_s3(table, db_con, s3_client):
    df = pd.read_sql(table, db_con)
    filename = f"../data/{table}.csv"
    df.to_csv(filename)
    s3_client.upload_file(
        filename,
        "gc-bricks",
        f"raw/gc/full-load/{table}/full_load.csv",
    )
    return True


# %%
con = sqlalchemy.create_engine("sqlite:///../data/gc.db")
inspector = sqlalchemy.inspect(con)
tables = inspector.get_table_names()
s3_client = boto3.client("s3")


# %%
for t in tqdm(tables):
    save_s3(t, con, s3_client)
