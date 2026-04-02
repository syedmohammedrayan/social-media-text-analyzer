import re
from collections import Counter

# --- Pure NLP Utility Functions (No Flask or API bindings) ---

def clean_text(text):
    """
    Step 1 & 2: Take input and clean text.
    Removes punctuation and normalizes to lowercase.
    """
    if not text:
        return ""
    # Replace anything that isn't a word character or whitespace with empty string
    cleaned = re.sub(r'[^\w\s]', '', text)
    return cleaned.lower()

def get_word_frequency(words):
    """
    Step 3 & 4: Split words and count frequency.
    Uses Python's built-in dictionary/collections.Counter.
    """
    if not words:
        return {}
    
    # Standard dictionary approach to show fundamental Python concepts
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

def get_top_words(frequency_dict, n=5):
    """
    Step 5: Find the top N words.
    Sorts the dictionary by values in descending order.
    """
    # Sorting a dictionary by its values
    sorted_items = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Return a list of tuples formatted properly
    top_n = sorted_items[:n]
    return [{"word": item[0], "count": item[1]} for item in top_n]

def get_repeated_characters(text):
    """
    Step 6: Detect repeated characters (spam/emphasis patterns).
    Looks for 3 or more of the same character in a row.
    Majorly uses Python string loops, sets, and basic logic.
    """
    if not text:
        return []

    results = []
    # Match any character (\w) followed by the same character 2 or more times
    matches = re.finditer(r'([A-Za-z])\1{2,}', text)
    
    # Set to avoid duplicate reports if the same spam word appears multiple times
    seen_patterns = set()

    for match in matches:
        pattern = match.group(0) # e.g., "soooo"
        char = match.group(1)    # e.g., "o"
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
    """
    Bonus: Detect general tone based on simple keyword sets.
    """
    # Simple sets for tone detection
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


# Example Usage Console Block
if __name__ == "__main__":
    sample_text = "Wait this is SOOOooo amazing and great!!! Hurry now!"
    print(f"Original Text: {sample_text}")
    print("-" * 30)
    
    clean = clean_text(sample_text)
    words = clean.split()
    
    freq = get_word_frequency(words)
    print(f"Top Words: {get_top_words(freq, 3)}")
    print(f"Tone: {detect_tone(words)}")
    print(f"Spam Patterns: {get_repeated_characters(sample_text)}")
