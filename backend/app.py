from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
CORS(app)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Cache setup
CACHE_FILE = "youtube_cache.json"
CACHE_DURATION = 24 * 60 * 60

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache_data):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
    except:
        pass

cache = load_cache()

# ============================================
# 🔥 CAREER DATABASE (with websites)
# ============================================
career_data = {
    "AI Engineer / Software Developer": {
        "description": "AI Engineers build intelligent systems that can simulate human intelligence.",
        "roadmap": ["Learn Python", "Learn DSA", "Web Development", "Machine Learning", "Build Projects", "Apply for Jobs"],
        "websites": [
            {"name": "GeeksforGeeks", "link": "https://www.geeksforgeeks.org"},
            {"name": "LeetCode", "link": "https://leetcode.com"},
            {"name": "W3Schools", "link": "https://www.w3schools.com"},
            {"name": "Coursera", "link": "https://www.coursera.org"},
        ]
    },
    "Product Manager / Business Analyst": {
        "description": "Product Managers define product vision and strategy.",
        "roadmap": ["Learn Business Fundamentals", "Learn SQL & Excel", "Product Lifecycle", "Communication", "Agile & Scrum"],
        "websites": [
            {"name": "Product School", "link": "https://productschool.com"},
            {"name": "Coursera", "link": "https://www.coursera.org"},
            {"name": "Udemy", "link": "https://www.udemy.com"},
            {"name": "PMI", "link": "https://www.pmi.org"}
        ]
    },
    "Government / PSU / Administrative Roles": {
        "description": "Government jobs offer stability, security, and prestige.",
        "roadmap": ["Aptitude", "Current Affairs", "Mock Tests", "Interview Preparation"],
        "websites": [
            {"name": "Testbook", "link": "https://testbook.com"},
            {"name": "SSC Official", "link": "https://ssc.gov.in/"},
            {"name": "UPSC", "link": "https://upsc.gov.in/"},
            {"name": "Oliveboard", "link": "https://www.oliveboard.in/"}
        ]
    },
    "UI/UX Designer / Creative Technologist": {
        "description": "UI/UX Designers create user-friendly interfaces.",
        "roadmap": ["Learn Figma", "UI Principles", "User Research", "Build Portfolio"],
        "websites": [
            {"name": "Dribbble", "link": "https://dribbble.com"},
            {"name": "Behance", "link": "https://www.behance.net"},
            {"name": "Figma", "link": "https://www.figma.com"},
            {"name": "Adobe XD", "link": "https://www.adobe.com/in/products/xd.html"}
        ]
    },
    "Digital Marketing / HR / Entrepreneurship": {
        "description": "Digital Marketing promotes brands online. HR manages people.",
        "roadmap": ["Learn SEO", "Social Media Marketing", "Content Creation", "Brand Building"],
        "websites": [
            {"name": "HubSpot", "link": "https://www.hubspot.com"},
            {"name": "Google Digital Garage", "link": "https://learndigital.withgoogle.com"},
            {"name": "Neil Patel Blog", "link": "https://neilpatel.com"},
            {"name": "Moz", "link": "https://moz.com"}
        ]
    }
}
# ============================================
# 🔹 PREDICT API
# ============================================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    interest = sum(data["interest"])
    skills = sum(data["skills"])
    aptitude = sum(data["aptitude"])
    personality = sum(data["personality"])
    work = sum(data["work"])

    if skills >= 20 and aptitude >= 20:
        career = "AI Engineer / Software Developer"
    elif interest >= 18 and personality >= 18:
        career = "Product Manager / Business Analyst"
    elif work >= 20 and personality >= 20:
        career = "Government / PSU / Administrative Roles"
    elif interest >= 18 and skills >= 15:
        career = "UI/UX Designer / Creative Technologist"
    else:
        career = "Digital Marketing / HR / Entrepreneurship"

    result = career_data[career]

    return jsonify({
        "career": career,
        "description": result["description"],
        "roadmap": result["roadmap"]
    })



@app.route("/get-resources", methods=["POST"])
def get_resources():
    global cache
    
    data = request.json
    career = data["career"]
    
    current_time = time.time()
    
    if career in cache:
        age = current_time - cache[career]["timestamp"]
        if age < CACHE_DURATION:
            return jsonify(cache[career]["data"])
        else:
            del cache[career]
    
    videos = []
    try:
        query = career.split()[0] + " full course"
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&maxResults=6&type=video"
        response = requests.get(url)
        yt_data = response.json()
        if "error" not in yt_data:
            for item in yt_data.get("items", []):
                videos.append({
                    "title": item["snippet"]["title"],
                    "videoId": item["id"]["videoId"]
                })
    except:
        videos = [{"title": "Career Guidance", "videoId": "nU-IIXBWlS4"}]
    
    # 🔥 YAHAN SE WEBSITES ADD KARO
    result = career_data.get(career, {})
    websites = result.get("websites", [])   # Ab websites properly aayengi
    
    final_result = {
        "videos": videos[:6],
        "websites": websites   # 🔥 websites add karna mat bhoolna
    }
    
    cache[career] = {"data": final_result, "timestamp": current_time}
    save_cache(cache)
    
    return jsonify(final_result)

# ============================================
# 🔹 REDIRECT TO SPECIFIC CAREER HTML PAGE
# ============================================
@app.route("/career/<path:career_name>")
def career_page(career_name):
    # URL decode karo
    from urllib.parse import unquote
    career_name = unquote(career_name)
    
    # Career name to filename mapping
    career_files = {
        "AI Engineer / Software Developer": "career_ai_engineer.html",
        "Product Manager / Business Analyst": "career_product_manager.html",
        "Government / PSU / Administrative Roles": "career_government.html",
        "UI/UX Designer / Creative Technologist": "career_ui_ux.html",
        "Digital Marketing / HR / Entrepreneurship": "career_digital_marketing.html"
    }
    
    # Find matching file
    filename = None
    for key, file in career_files.items():
        if key.lower() == career_name.lower():
            filename = file
            break
    
    if filename:
        return send_from_directory('../frontend', filename)
    
    return f"Career page not found for: {career_name}", 404

# ============================================
# 🔹 MAIN ROUTES
# ============================================
@app.route("/")
def home():
    return send_from_directory('../frontend', 'index.html')

@app.route("/quiz")
def quiz_page():
    return send_from_directory('../frontend', 'quiz.html')

@app.route("/result")
def result_page():
    return send_from_directory('../frontend', 'result.html')

@app.route("/admin")
def admin_panel():
    return send_from_directory('../frontend', 'admin.html')

@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)

# ============================================
# 🔹 ADMIN APIs
# ============================================
@app.route("/admin/refresh-cache", methods=["POST"])
def refresh_all_cache():
    global cache
    cache = {}
    save_cache(cache)
    return jsonify({"success": True, "message": "All cache cleared!"})

@app.route("/admin/refresh-cache/<path:career>", methods=["POST"])
def refresh_one_cache(career):
    global cache
    if career in cache:
        del cache[career]
        save_cache(cache)
        return jsonify({"success": True, "message": f"Cache cleared for {career}"})
    return jsonify({"success": False, "message": "No cache found"}), 404

@app.route("/admin/cache-status", methods=["GET"])
def cache_status():
    status = {}
    for career, data in cache.items():
        age = time.time() - data["timestamp"]
        status[career] = {
            "age_hours": round(age / 3600, 1),
            "expires_in_hours": round((CACHE_DURATION - age) / 3600, 1),
            "videos_count": len(data["data"].get("videos", []))
        }
    return jsonify({
        "cache_size": len(cache),
        "cache_duration_hours": CACHE_DURATION / 3600,
        "items": status
    })

# ============================================
# 🔹 RUN
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print(" Server Starting...")
    print(f" Cache file: {CACHE_FILE}")
    print(f" Cache duration: {CACHE_DURATION // 3600} hours")
    print(f" Loaded {len(cache)} items from cache")
    print(f" Server running on: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)