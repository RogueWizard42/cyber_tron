# file analyzer

from collections import Counter

def analyze_file(log_file):
    word_count = []
    with open(log_file, "r") as file:
        content = file.read()
        words = content.split("space")
        
        for word in words:
            clean_word = word.strip().replace("\n", "")
            if len(clean_word) > 0:
                word_count.append(clean_word)
        
    freq = Counter(word_count)
    
    for word, count in freq.most_common():
        print(f"{word}: {count}")
        
if __name__ == "__main__":
    analyze_file(".logd")
    
    