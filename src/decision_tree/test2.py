from math import log2
from collections import Counter

def entropy(data):
    """Berechnet die Entropie der gegebenen Daten."""
    total = len(data)
    counts = Counter([label for _, label in data])
    return sum((-count/total) * log2(count/total) for count in counts.values())

def split_data(data, split_point):
    """Teilt die Daten an einem gegebenen Schnittpunkt."""
    left = [d for d in data if d[0] <= split_point]
    right = [d for d in data if d[0] > split_point]
    return left, right

def gain_ratio(data, split_point):
    """Berechnet den Gain Ratio für einen gegebenen Schnittpunkt."""
    total_entropy = entropy(data)
    left, right = split_data(data, split_point)
    split_entropy = (len(left) / len(data)) * entropy(left) + (len(right) / len(data)) * entropy(right)
    gain = total_entropy - split_entropy
    
    # Berechnung der Split Information
    split_info = -((len(left)/len(data)) * log2(len(left)/len(data) + 1e-10) + (len(right)/len(data)) * log2(len(right)/len(data) + 1e-10))
    return gain / split_info if split_info != 0 else 0

def find_best_split_point(data):
    """Findet den besten Schnittpunkt für die gegebenen Daten."""
    data_sorted = sorted(data, key=lambda x: x[0])
    best_gain_ratio = -1
    best_split_point = None
    
    for i in range(1, len(data_sorted)):
        current_point, _ = data_sorted[i]
        previous_point, _ = data_sorted[i-1]
        if current_point != previous_point:  # Vermeidung von identischen Punkten
            split_point = (current_point + previous_point) / 2
            current_gain_ratio = gain_ratio(data, split_point)
            if current_gain_ratio > best_gain_ratio:
                best_gain_ratio = current_gain_ratio
                best_split_point = split_point
                
    return best_split_point, best_gain_ratio

# Beispiel der Nutzung:
data = [(2.0, 'A'), (3.5, 'B'), (1.0, 'A'), (4.5, 'B')]
best_split_point, best_gain_ratio = find_best_split_point(data)
print(f"Best Split Point: {best_split_point}, Gain Ratio: {best_gain_ratio}")