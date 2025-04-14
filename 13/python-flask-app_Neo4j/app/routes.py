from flask import Blueprint, request, jsonify
from app.extensions import neo4j

main = Blueprint('main', __name__)

@main.route('/api/hashtags', methods=['POST'])
def add_hashtags():
    data = request.json
    post_id = data.get('post_id')
    hashtags = data.get('hashtags', [])
    
    if not post_id or not hashtags:
        return jsonify({"error": "post_id and hashtags are required"}), 400
    
    neo4j.add_hashtags(post_id, hashtags)
    return jsonify({"status": "success"})

@main.route('/api/hashtags/trending', methods=['GET'])
def trending_hashtags():
    hours = int(request.args.get('hours', 24))
    limit = int(request.args.get('limit', 10))
    
    trending = neo4j.get_trending_hashtags(hours, limit)
    return jsonify({
        "time_period_hours": hours,
        "trending_hashtags": trending
    })