import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import os
import pickle

# Define activities globally so they are accessible to all functions.
activities = [
    ('sports', 'sports'),
    ('tvsports', 'watching sports on TV'),
    ('exercise', 'exercise'),
    ('dining', 'dining out'),
    ('museums', 'museums'),
    ('hiking', 'hiking'),
    ('gaming', 'gaming'),
    ('clubbing', 'clubbing'),
    ('reading', 'reading'),
    ('tv', 'watching TV'),
    ('theater', 'theater'),
    ('movies', 'movies'),
    ('music', 'music'),
    ('shopping', 'shopping')
]

# Define the race mapping (for user and candidate)
race_mapping = {
    1: "Asian/Pacific Islander/Asian-American",
    2: "European/Caucasian-American",
    3: "Latino/Hispanic American",
    4: "Black/African American",
    5: "Other"
}

def get_user_input():
    """Get all required input values from the user."""
    print("\nPlease enter your information (1-10 scale for preferences):")
    
    user_data = {}
    user_data['age'] = int(input("Enter your age: "))
    user_data['funny'] = int(input("Rate your sense of humor (1-10): "))
    
    # Updated race input: now only display options 1 to 5.
    print("\nSelect your race from the following options:")
    print("  1: Asian/Pacific Islander/Asian-American")
    print("  2: European/Caucasian-American")
    print("  3: Latino/Hispanic American")
    print("  4: Black/African American")
    print("  5: Other")
    race_input = int(input("Enter your race (1-5): "))
    user_data['race'] = race_input

    user_data['ambition'] = int(input("Rate your ambition level (1-10): "))
    
    print("\nRate your interest in the following activities (1-10):")
    for key, desc in activities:
        user_data[key] = int(input(f"Rate your interest in {desc}: "))
    
    return user_data

def calculate_features(user_data, sample_row):
    """Calculate all required features for the ML model."""
    features = {}
    
    # Base features
    features['age'] = user_data['age']
    features['age_o'] = sample_row['age']
    features['d_age'] = abs(features['age'] - features['age_o'])
    
    features['race'] = user_data['race']
    features['race_o'] = sample_row['race']
    features['samerace'] = 1 if features['race'] == features['race_o'] else 0
    
    features['funny'] = user_data['funny']
    features['funny_o'] = sample_row['funny']
    
    features['ambition'] = user_data['ambition']
    features['d_ambitous_o'] = abs(features['ambition'] - sample_row['ambition'])
    
    # Calculate differences and multiplied values for each activity
    for act, _ in activities:
        # Original interest values from user_data and sample_row
        features[act] = float(user_data[act])
        # Difference between user and candidate interest levels
        features[f'd_{act}'] = abs(float(user_data[act]) - float(sample_row[act]))
        # Multiplied value to capture joint interest
        features[f'{act}_multiplied'] = float(user_data[act]) * float(sample_row[act])
    
    return features

def prepare_input_vector(features):
    """Prepare the input vector in the correct order for the ML model."""
    # Base features must match exactly what was used in training
    base_features = ['age', 'age_o', 'd_age', 'samerace', 'funny_o', 'funny',
                     'ambition', 'd_ambitous_o', 'race', 'race_o']

    activity_pairs = [
        ('sports', 'd_sports'),
        ('tvsports', 'd_tvsports'),
        ('exercise', 'd_exercise'),
        ('dining', 'd_dining'),
        ('museums', 'd_museums'),
        ('hiking', 'd_hiking'),
        ('gaming', 'd_gaming'),
        ('clubbing', 'd_clubbing'),
        ('reading', 'd_reading'),
        ('tv', 'd_tv'),
        ('theater', 'd_theater'),
        ('movies', 'd_movies'),
        ('music', 'd_music'),
        ('shopping', 'd_shopping')
    ]
    
    # Create final feature list in the same order as used for training.
    final_features = base_features.copy()
    for act, _ in activity_pairs:
        final_features.append(f'{act}_multiplied')
    
    # Convert the vector to a DataFrame with the correct column names.
    vector = [features[feat] for feat in final_features]
    input_df = pd.DataFrame([vector], columns=final_features)
    return input_df

def main():
    # Load the trained model saved as a pickle (.pkl) file.
    try:
        with open('trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Loaded trained model successfully!")
    except FileNotFoundError:
        print("Error: Could not find trained model file 'trained_model.pkl'")
        print("Please run model_v3_fix.py first to train and save the model.")
        return
    
    # Get user input
    user_data = get_user_input()
    
    # Load sample data
    sample_data = pd.read_csv('Sample Data Inputs.csv', skipinitialspace=True)
    
    # Clean column names by stripping whitespace
    sample_data.columns = sample_data.columns.str.strip()
    
    # Map candidate race values from string (if needed) to their numeric codes.
    if sample_data['race'].dtype == object:
        # Map from dataset race values (strings) to our numeric codes.
        race_reverse = {
            "Asian/Pacific Islander/Asian-American": 1,
            "European/Caucasian-American": 2,
            "Latino/Hispanic American": 3,
            "Black/African American": 4,
            "Other": 5
        }
        sample_data['race'] = sample_data['race'].map(race_reverse)
    
    # Convert all columns to numeric.
    for col in sample_data.columns:
        sample_data[col] = pd.to_numeric(sample_data[col].astype(str).str.strip(), errors='coerce')
    
    # Process each sample row and calculate the candidate match probabilities.
    candidates = []
    print("\nDebug: First few rows of sample data:")
    print(sample_data.head())
    print("\nDebug: Data types of columns:")
    print(sample_data.dtypes)
    
    for idx, sample_row in sample_data.iterrows():
        # Optional debug print for first row
        if idx == 0:
            print("\nDebug: First row values:")
            print(sample_row)
            
        features = calculate_features(user_data, sample_row)
        input_vector = prepare_input_vector(features)
        probability = model.predict_proba(input_vector)[0][1]
        
        candidates.append({
            'row_number': idx + 2,  
            'age': sample_row['age'],
            'race': sample_row['race'],
            'probability': probability
        })
    
    # Sort the candidates by probability (highest first) and select the top 10
    top_candidates = sorted(candidates, key=lambda x: x['probability'], reverse=True)[:10]
    
    # Display top 10 filtering candidates using race (mapped from numeric) instead of row numbers.
    if top_candidates:
        print("\nTop 10 Highest Filter Candidates (Row #, Race, Age, Match Probability):")
        for candidate in top_candidates:
            candidate_race = race_mapping.get(candidate['race'], "Unknown")
            print(f"ID: {candidate['row_number']}: Race: {candidate_race}, Age: {candidate['age']}, Probability: {candidate['probability']:.2%}")
    else:
        print("\nNo candidates found based on the current criteria.")

if __name__ == "__main__":
    main() 