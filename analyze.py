from http.server import BaseHTTPRequestHandler
import json
import re

def clean_text(text):
    if not text:
        return ""
    cleaned = re.sub(r'[^\w\s]', '', text)
    return cleaned.lower()

def get_word_frequency(words):
    if not words:
        return {}
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def get_top_words(frequency_dict, n=5):
    sorted_items = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_items[:n]
    return [{"word": item[0], "count": item[1]} for item in top_n]

def get_repeated_characters(text):
    if not text:
        return []
    results = []
    matches = re.finditer(r'([A-Za-z])\1{2,}', text)
    seen_patterns = set()
    for match in matches:
        pattern = match.group(0)
        char = match.group(1)
        count = len(pattern)
        if pattern not in seen_patterns:
            seen_patterns.add(pattern)
            results.append({
                "pattern": pattern,
                "character": char,
                "count": count,
                "insight": f"'{char}' used {count} times for emphasis"
            })
    return results

def detect_tone(words):
    positive = {"love", "awesome", "great", "good", "amazing", "best", "brilliant", "yay"}
    negative = {"hate", "bad", "terrible", "worst", "awful", "trash", "no", "never"}
    urgent = {"now", "quick", "asap", "hurry", "urgent", "fast"}
    word_set = set(words)
    if word_set.intersection(positive):
        return "Positive & Enthusiastic"
    elif word_set.intersection(negative):
        return "Negative or Critical"
    elif word_set.intersection(urgent):
        return "High Urgency / CTA"
    elif len(words) > 0:
        return "Neutral / Informative"
    return "Unknown"

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length_str = self.headers.get('Content-Length', '0')
            content_length = int(content_length_str) if content_length_str else 0
            
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
            
            raw_text = data.get('text', '')
            
            cleaned = clean_text(raw_text)
            words = cleaned.split() if cleaned else []
            word_count = len(words)
            char_count = len(raw_text)
            freq = get_word_frequency(words)
            top = get_top_words(freq, 5)
            spam = get_repeated_characters(raw_text)
            tone = detect_tone(words)
            
            response_payload = {
                "status": "success",
                "stats": {
                    "word_count": word_count,
                    "char_count": char_count
                },
                "frequency": freq,
                "common": top,
                "repeated": spam,
                "tone": tone
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
