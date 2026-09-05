from app import app, db, Manga
import pandas as pd
import json

df = pd.read_pickle("notebooks/manga_clean.pkl")

def to_json(val):
    if isinstance(val, list):
        return json.dumps(val)
    else:
        return '[]'

list_columns = ["genres", "tags", "authors"]
for col in list_columns:
    df[col] = df[col].apply(to_json)

print(df[["genres", "tags", "authors"]].map(type).value_counts())


with app.app_context():
    df.to_sql(name='manga', con=db.engine, if_exists='append', index=False, chunksize=1000, method='multi')

print("Done!")