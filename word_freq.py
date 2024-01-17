import nltk
from nltk.corpus import brown
from nltk import FreqDist, ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Ensure NLTK datasets are downloaded
nltk.download('brown')
nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
    """Tokenize and lowercase."""
    lowercased = text.lower()
    tokens = word_tokenize(lowercased)
    tokens = [t for t in tokens if t not in string.punctuation]
    return tokens

def calculate_frequencies(tokens, n=1):
    """Calculate normalized word or n-gram frequencies in the tokens."""
    if n > 1:
        tokens = list(ngrams(tokens, n))
    freq_dist = FreqDist(tokens)
    total_items = len(tokens)
    normalized_freq = {item: (count / total_items) * 1000 for item, count in freq_dist.items()}  # Per 1000 items
    return normalized_freq

def compare_frequencies(custom_freq, reference_freq):
    """Compare item frequencies between two sets of tokens."""
    comparison = {}
    for item in custom_freq:
        custom_rate = custom_freq[item]
        reference_rate = reference_freq.get(item, 0)
        comparison[item] = custom_rate - reference_rate
    return comparison

def run_analysis(our_text: str, dist: list):
    """Output a list of n-gram more and less used where dist is a list of n."""
    # Preprocess our text and the Brown corpus
    our_tokens = preprocess(our_text)
    brown_tokens = preprocess(' '.join(brown.words()))
    
    #initialize output
    final_output = []
    
    for n in dist:
        # Calculate frequencies for n-grams
        our_ngram_freq = calculate_frequencies(our_tokens, n=n)
        brown_ngram_freq = calculate_frequencies(brown_tokens, n=n)
    
        # Compare frequencies
        frequency_comparison = compare_frequencies(our_ngram_freq, brown_ngram_freq)
    
        # 4-grams used more or less in our text compared to average English
        more_used = {gram: diff for gram, diff in frequency_comparison.items() if diff > 0}
        less_used = {gram: diff for gram, diff in frequency_comparison.items() if diff < 0}
    
        n_output = {n: {'more': more_used, 'less': less_used}}
        final_output.append(n_output)
        
    return final_output

# Replace this with our text
our_text = "Yo dude it's just Cole Gordon from ClosersIO how ya'll doing today"
dist = [1,2,3]

test = run_analysis(our_text, dist)
print(test)
