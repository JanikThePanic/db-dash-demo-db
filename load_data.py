import kagglehub
import pandas as pd
import weaviate
from weaviate.classes.config import Property, DataType

# --- 1. Download Iris dataset from Kaggle ---
print("Downloading Iris dataset...")
path = kagglehub.dataset_download("uciml/iris")

# The downloaded folder contains iris.data or iris.csv
iris_file = f"{path}/Iris.csv"
df = pd.read_csv(iris_file)
print(f"Loaded {len(df)} rows")

# --- 2. Connect to local Weaviate ---
client = weaviate.connect_to_local(host="localhost", port=3131)

# --- 3. Define schema if not exists ---
if not client.collections.exists("Iris"):
    client.collections.create(
        name="Iris",
        properties=[
            Property(name="sepal_length", data_type=DataType.NUMBER),
            Property(name="sepal_width", data_type=DataType.NUMBER),
            Property(name="petal_length", data_type=DataType.NUMBER),
            Property(name="petal_width", data_type=DataType.NUMBER),
            Property(name="species", data_type=DataType.TEXT),
        ],
        description="Iris flower dataset entries",
    )
    print("Created collection 'Iris'")
else:
    print("Collection 'Iris' already exists")

# --- 4. Insert data into Weaviate ---
collection = client.collections.get("Iris")

with collection.batch.dynamic() as batch:
    for _, row in df.iterrows():
        batch.add_object(
            properties={
                "sepal_length": float(row["SepalLengthCm"]),
                "sepal_width": float(row["SepalWidthCm"]),
                "petal_length": float(row["PetalLengthCm"]),
                "petal_width": float(row["PetalWidthCm"]),
                "species": row["Species"],
            }
        )

print(f"Inserted {len(df)} objects into Weaviate")

# --- 5. Close client ---
client.close()
print("Done!")
