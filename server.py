import http.server
import json
import socketserver
import analyzer  # Import our pure python logic

PORT = 5000

class AnalysisHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle analysis requests."""
        if self.path == '/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                raw_text = data.get('text', '')
                
                # --- Step-by-Step Logic using Python Concepts ---
                # 1. Clean the text using string concepts
                cleaned = analyzer.clean_text(raw_text)
                
                # 2. Split into list of words
                words = cleaned.split() if cleaned else []
                word_count = len(words)
                char_count = len(raw_text)
                
                # 3. Analyze word frequency (Dictionary concept)
                freq = analyzer.get_word_frequency(words)
                
                # 4. Find top words (Sorting/List concepts)
                top = analyzer.get_top_words(freq, 5)
                
                # 5. Detect repeated characters (Regex/String concepts)
                spam = analyzer.get_repeated_characters(raw_text)
                
                # 6. Detect tone (Set concepts)
                tone = analyzer.detect_tone(words)
                
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
                self.send_header('Access-Control-Allow-Origin', '*') # CORS
                self.end_headers()
                self.wfile.write(json.dumps(response_payload).encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(("", PORT), AnalysisHandler) as httpd:
    print(f"Social Media Text Analyzer - Pure Python Server running on port {PORT}")
    print("Zero dependencies used (No Flask, No FastAPI)")
    httpd.serve_forever()
