
# 🎯 Edge-Based Predictive Caching System with Federated Learning  
## *(Hybrid PySpark + Redis Edition)*

This project simulates a smarter version of Netflix that can guess what you want to watch — and gets it ready before you even click. It’s built step-by-step using open-source tools and explained in a way that even a 10-year-old can understand.

---

## 🧠 What Are We Building?

A system that:
- Pretends to be Netflix
- Learns from fake user behavior
- Predicts what content people will watch next
- Stores that content in a fast memory (cache)
- Shows dashboards of how well the system is performing

---

## 📦 Tech Stack (All Open Source)

| Component           | Tool                  |
|---------------------|------------------------|
| Data Simulation      | Python, Faker          |
| Prediction Engine    | PySpark                |
| Caching              | Redis                  |
| Monitoring           | Prometheus + Grafana   |
| Development Environment | VS Code             |

---

## 🛠 Step-by-Step Instructions

### 🧰 Step 1: Set Up Your Environment (Windows or Mac)

```bash
# Install Python (3.9+)
# Install pip if not included

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt
```

---

### 📦 Step 2: Install Redis and Apache Spark

- **Redis**: https://redis.io/docs/getting-started/installation/
- **Apache Spark**: https://spark.apache.org/downloads.html

Or use Docker:

```bash
# Start Redis with Docker
docker run -p 6379:6379 redis
```

---

### 📝 Step 3: Simulate Fake Netflix Users

Create synthetic user logs using Python:

```bash
python data/generate_user_logs_spark.py
```

This generates logs like:

```json
{
  "user_id": "U001",
  "device": "TV",
  "content_id": "C456",
  "duration": 42,
  "timestamp": "2025-04-12 22:30:00"
}
```

---

### 🔎 Step 4: Analyze & Predict with PySpark

Use PySpark to load the logs and run SQL queries to:
- Group by user
- Count watch frequency
- Predict next most likely content

Run:

```bash
spark-submit prediction_engine/features_spark.py
```

---

### 💾 Step 5: Cache Predictions in Redis

Use Python to cache predictions:

```python
import redis
r = redis.Redis()
r.set("user:U001", "C456")
```

Retrieve cached recommendation:

```python
r.get("user:U001")
```

---

### 🚚 Step 6: Make Content Delivery Decisions (Live Flow)

In real-time:
1. Check if the predicted content exists in Redis
2. If yes → deliver from cache
3. If no → compute prediction and update Redis

---

### 📊 Step 7: Monitor Performance

Use Prometheus + Grafana to track:
- Cache hits/misses
- Prediction time
- User activity metrics

Example metric:

```python
from prometheus_client import Counter, start_http_server
hit_counter = Counter("cache_hits", "Redis Cache Hits")
hit_counter.inc()
```

Start a basic metrics server:

```bash
python monitoring/start_metrics_server.py
```

Access Grafana at: `http://localhost:3000`

---

## 🚀 You Did It!

You’ve just built a simplified but powerful Netflix-style predictive engine with:
- Fake users
- Predictive intelligence
- Redis caching
- SQL + Spark processing
- Real-time dashboards

All with free tools, running locally. 💪

---

## 💡 What’s Next?

Start by running the fake user generator and checking the output.  
Then move on to Spark SQL-based prediction.

I'll be right here if you need help writing or debugging anything. 🚀
