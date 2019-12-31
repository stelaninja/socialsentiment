import pandas as pd
import sqlite3
import os
import sys

# set chdir to current dir
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))

input_key = "sverige"

conn = sqlite3.connect("twitter.db")
c = conn.cursor()

df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000",
                 conn, params=("%" + input_key + "%",))
df.sort_values("unix", inplace=True)
df["date"] = pd.to_datetime(df["unix"], unit="ms")
df.set_index("date", inplace=True)
df["smoothed_sentiment"] = df["sentiment"].rolling(
    int(len(df)/5)).mean()
df.dropna(inplace=True)

print(df.head())
print(df.describe())
