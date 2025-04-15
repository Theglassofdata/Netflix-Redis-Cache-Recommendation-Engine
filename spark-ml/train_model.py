from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.recommendation import ALS
import redis
from prometheus_client import start_http_server

# Start Prometheus metrics server
start_http_server(8001)

# Step 1: Start Spark Session
spark = SparkSession.builder \
    .appName("NetflixRecommendationTrainer") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Step 2: Load Data
file_path = "/home/jovyan/data/synthetic_streaming_data.csv"
df = spark.read.option("header", True).csv(file_path)

# Step 3: Prepare Data for ALS
# Create indexed user and content tables
user_indexed = df.select("user_id").distinct().rdd.zipWithIndex().toDF(["user_struct", "user_index"])
content_indexed = df.select("content_id").distinct().rdd.zipWithIndex().toDF(["content_struct", "content_index"])

# Extract ID from struct (zipWithIndex wraps it in a struct)
from pyspark.sql.functions import col as F_col
user_indexed = user_indexed.withColumn("user_id", F_col("user_struct.user_id")).drop("user_struct")
content_indexed = content_indexed.withColumn("content_id", F_col("content_struct.content_id")).drop("content_struct")

# Join original data with indexed IDs
df = df.join(user_indexed, on="user_id").join(content_indexed, on="content_id")

# Use duration_minutes as watch_count proxy
df = df.withColumn("watch_count", col("duration_minutes").cast("int"))

# Step 4: Train ALS Model
als = ALS(userCol="user_index", itemCol="content_index", ratingCol="watch_count", coldStartStrategy="drop")
model = als.fit(df)

# Step 5: Generate Top-N Recommendations
user_recs = model.recommendForAllUsers(1)

# Step 6: Map back to original user/content IDs
user_reverse = user_indexed.selectExpr("user_id as original_user", "user_index")
content_reverse = content_indexed.selectExpr("content_id as original_content", "content_index")

final_recs = user_recs.select("user_index", "recommendations.content_index")
final_recs = final_recs.withColumn("content_index", final_recs["content_index"].getItem(0))
final_recs = final_recs.join(user_reverse, on="user_index").join(content_reverse, on="content_index")

# Step 7: Cache in Redis
r = redis.Redis(host="redis", port=6379, decode_responses=True)
for row in final_recs.select("original_user", "original_content").collect():
    r.set(f"user:{row['original_user']}", row['original_content'])
    print(f"✅ Cached for {row['original_user']}: {row['original_content']}")

# Step 8: Stop Spark
spark.stop()
