from flask import Flask, request, jsonify
import redis
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# Prometheus metrics
cache_hits = Counter("cache_hits", "Total number of cache hits")
cache_misses = Counter("cache_misses", "Total number of cache misses")
fallbacks = Counter("fallbacks_used", "Fallbacks triggered due to no prediction")

# Health check route
@app.route('/health')
def health():
    return 'OK', 200

# Simulate user watching a show
@app.route('/watched', methods=['POST'])
def watched():
    data = request.json
    user_id = data.get("user_id")
    content_id = data.get("content_id")

    # ✅ Simple prediction rule
    def predict(content_id):
        if content_id == "C1010":
            return "C1045"  # e.g. Cobra Kai
        return "C000"

    predicted = predict(content_id)
    r.set(f"user:{user_id}", predicted)
    return jsonify({
        "user_id": user_id,
        "watched": content_id,
        "predicted_next": predicted
    })

# Get recommendation for a user
@app.route('/recommend/<user_id>', methods=['GET'])
def recommend(user_id):
    key = f"user:{user_id}"
    result = r.get(key)

    if result:
        cache_hits.inc()
        return jsonify({
            "user_id": user_id,
            "recommendation": result,
            "cache_hit": True
        })
    else:
        fallback = "C000"
        r.set(key, fallback)
        cache_misses.inc()
        fallbacks.inc()
        return jsonify({
            "user_id": user_id,
            "recommendation": fallback,
            "cache_hit": False,
            "fallback_used": True
        })

# Prometheus metrics endpoint
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
