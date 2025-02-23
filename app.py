import streamlit as st
import pandas as pd
from match_predictor import get_user_input, calculate_features, prepare_input_vector, race_mapping, activities
import pickle
import random
import time
import os

def common_style():
    return """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Apply custom styles to entire app */
        .stApp {
            font-family: 'Open Sans', sans-serif;
            background: linear-gradient(135deg, #D8BFD8, #ADD8E6, #FFB6C1);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* Fade-in animation */
        .fade-in {
            opacity: 0;
            animation: fadeIn 1s forwards;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Main title styling */
        .title, .st-emotion-cache-10trblm {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 3.2rem !important;
            margin-bottom: 2rem !important;
            color: #000000 !important;
            text-align: center !important;
        }
        
        /* Section headers */
        .section-header {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 1.8rem !important;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
            color: #000000 !important;
            border-bottom: 2px solid #1E88E5;
            padding-bottom: 0.5rem;
        }
        
        /* Question text styling */
        .question-text, .st-emotion-cache-1629p8f {
            font-family: 'Open Sans', sans-serif !important;
            font-weight: 500 !important;
            font-size: 1.2rem !important;
            color: #000000 !important;
            margin-bottom: 0.8rem !important;
            line-height: 1.5 !important;
        }
        
        /* Slider styling */
        .stSlider {
            width: 300px !important;
            margin-bottom: 1rem !important;
        }
        
        .stSlider > div > div > div {
            height: 0.6rem !important;
        }
        
        /* Thicker sliders for the second section */
        .stSlider.second-section > div > div > div {
            height: 1rem !important;
        }
        
        /* Show the start and end labels of the slider */
        .stSlider > div > div > div > div {
            display: block !important;
        }
        
        /* Button styling */
        .stButton>button {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.2rem !important;
            background-color: #FFB6C1 !important; /* Light pink */
            color: #000000 !important; /* Black text */
            padding: 0.8rem 3rem !important;
            border-radius: 30px;
            transition: all 0.3s ease;
            margin: 1rem auto !important;
            display: block !important;
            border: none !important;
        }
        
        .stButton>button:hover {
            background-color: #FFC0CB !important; /* Slightly different pink on hover */
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 182, 193, 0.3) !important; /* Light pink shadow */
        }
        
        /* Selectbox styling */
        .stSelectbox {
            font-family: 'Open Sans', sans-serif;
            font-size: 1.1rem !important;
            color: #000000 !important;
        }
        
        /* Number input styling */
        .stNumberInput {
            font-family: 'Open Sans', sans-serif;
            font-size: 1.1rem !important;
            color: #000000 !important;
        }
        
        /* Add spacing between sections */
        .stMarkdown {
            margin-bottom: 1rem;
        }
        
        /* Make all text inputs and labels larger */
        .st-bw {
            font-size: 1.1rem !important;
            color: #000000 !important;
        }
        
        /* Style the slider labels */
        .stSlider label {
            font-size: 1.1rem !important;
            color: #000000 !important;
        }
        </style>
    """

def welcome_page():
    # Add the common style with additional styles
    st.markdown(common_style() + """
        <style>
        .welcome-container {
            text-align: center;
            padding: 2rem;
        }
        
        .welcome-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* Add some spacing between elements */
        .welcome-content .question-text {
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Use custom styled title and centered text
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-content">
                <p class="title">Welcome to MadLuv</p>
                <p class="question-text">Find your perfect match in campus today!</p>
                <p class="question-text">Click below to start your journey.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start", key="start_button"):
        st.session_state.page = "input"
        st.rerun()

def user_input_page():
    # Add the common style
    st.markdown(common_style(), unsafe_allow_html=True)
    
    # Main title with custom styling
    st.markdown("""
        <div class="fade-in" style="text-align: center;">
            <p class="title">Your Perfect Match is Waiting.</p>
            <p class="question-text" style="margin-bottom: 2rem;">Enter your information below to find your soulmate!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Basic Information Section
    st.markdown("""
        <div class="fade-in" style="text-align: center;">
            <p class="section-header">Basic Information</p>
        </div>
    """, unsafe_allow_html=True)
    
    user_data = {}
    
    # Basic inputs with styled labels and unique keys
    st.markdown('<p class="question-text fade-in">Enter your age:</p>', unsafe_allow_html=True)
    user_data['age'] = st.number_input("", min_value=18, max_value=100, value=25, 
                                     label_visibility="collapsed", 
                                     key="age_input")
    
    st.markdown('<p class="question-text fade-in">Rate your sense of humor:</p>', unsafe_allow_html=True)
    user_data['funny'] = st.slider("", 1, 10, 5, 
                                 label_visibility="collapsed", 
                                 key="humor_slider")
    
    # Race selection
    st.markdown('<p class="question-text fade-in">Select your race:</p>', unsafe_allow_html=True)
    race_options = {v: k for k, v in race_mapping.items()}
    selected_race = st.selectbox("", options=list(race_options.keys()), 
                               label_visibility="collapsed", 
                               key="race_select")
    user_data['race'] = race_options[selected_race]
    
    st.markdown('<p class="question-text fade-in">How focused are you towards your goals and career?:</p>', unsafe_allow_html=True)
    user_data['ambition'] = st.slider("", 1, 10, 5, 
                                    label_visibility="collapsed", 
                                    key="ambition_slider")
    
    # Activities Section
    st.markdown("""
        <div class="fade-in" style="text-align: center;">
            <p class="section-header">Interest and Hobbies</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="fade-in" style="text-align: center;">
            <p class="question-text">Rate your interest in the following activities (1-10):</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for activities
    col1, col2 = st.columns(2)
    
    # Split activities into two columns
    half = len(activities) // 2
    
    # First column of activities
    with col1:
        for key, desc in activities[:half]:
            st.markdown(f'<p class="question-text fade-in">{desc}:</p>', unsafe_allow_html=True)
            user_data[key] = st.slider("", 1, 10, 5, 
                                     key=f"slider_{key}", 
                                     label_visibility="collapsed")
    
    # Second column of activities
    with col2:
        for key, desc in activities[half:]:
            st.markdown(f'<p class="question-text fade-in">{desc}:</p>', unsafe_allow_html=True)
            user_data[key] = st.slider("", 1, 10, 5, 
                                     key=f"slider_{key}", 
                                     label_visibility="collapsed")
    
    # Add some spacing before the button
    st.write("")
    st.write("")
    
    if st.button("Find Matches", key="find_matches_button"):
        st.session_state.user_data = user_data
        st.session_state.page = "results"
        st.rerun()

def find_file(filename):
    for root, dirs, files in os.walk('.'):
        if filename in files:
            return os.path.join(root, filename)
    raise FileNotFoundError(f"{filename} not found")

def get_activity_recommendations(user_data, candidate_row_number=None):
    """
    Generate activity recommendations based on user preferences and optionally a candidate's preferences
    Returns a dictionary containing recommended sites and their URLs
    """
    # Find the file paths dynamically
    attraction_path = find_file('Refined_Categorized_Attractions.csv')
    sample_data_path = find_file('Sample Data Inputs.csv')
    
    # Load attraction data
    attraction = pd.read_csv(attraction_path)
    
    # Strip whitespace from column names
    attraction.columns = attraction.columns.str.strip()
    
    # Print column names for debugging
    print(attraction.columns.tolist())
    
    # Define columns for analysis (matching the features in attractions.csv)
    activity_mapping = {
        'sports': 'sports',
        'tvsports': 'tvsports',
        'exercise': 'exercise',
        'dining': 'dining',
        'museums': 'museums',
        'hiking': 'hiking',
        'gaming': 'gaming',
        'clubbing': 'clubbing',
        'reading': 'reading',
        'tv': 'tv',
        'theater': 'theater',
        'movies': 'movies',
        'music': 'music',
        'shopping': 'shopping'
    }
    
    recommendations = {}
    
    # Get candidate recommendations if row number provided
    if candidate_row_number is not None:
        cand = pd.read_csv(sample_data_path)
        cand_prefs = cand.iloc[candidate_row_number]
        
        # Find highest rated activity
        max_activity = max(activity_mapping.keys(), key=lambda x: cand_prefs[x] if x in cand_prefs else 0)
        feature_to_search = activity_mapping[max_activity]
        
        # Find matching attractions
        matching_attractions = attraction[attraction['features'].str.contains(feature_to_search, na=False)]
        
        if not matching_attractions.empty:
            selected_attraction = matching_attractions.sample(n=1).iloc[0]
            recommendations['candidate_recommendation'] = {
                'site': selected_attraction['site'],
                'url': selected_attraction['url'],
                'based_on': feature_to_search
            }
    
    # Get user recommendations
    user_prefs = {k: user_data.get(k, 5) for k in activity_mapping.keys()}
    max_activity = max(user_prefs.items(), key=lambda x: x[1])[0]
    feature_to_search = activity_mapping[max_activity]
    
    # Find matching attractions for user
    matching_attractions = attraction[attraction['features'].str.contains(feature_to_search, na=False)]
    
    if not matching_attractions.empty:
        selected_attraction = matching_attractions.sample(n=1).iloc[0]
        recommendations['user_recommendation'] = {
            'site': selected_attraction['site'],
            'url': selected_attraction['url'],
            'based_on': feature_to_search
        }
    
    # Add a random recommendation
    random_attraction = attraction.sample(n=1).iloc[0]
    recommendations['random_recommendation'] = {
        'site': random_attraction['site'],
        'url': random_attraction['url']
    }
    
    return recommendations

def results_page():
    # Add the common style with additional scroll control
    st.markdown(common_style() + """
        <style>
        /* Force the page to start from top */
        html {
            scroll-behavior: smooth !important;
        }
        
        /* Results page specific styling */
        .results-title {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 2.8rem !important;
            color: #000000 !important;
            text-align: center !important;
            margin-bottom: 2rem !important;
        }
        
        .section-subtitle {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.8rem !important;
            color: #000000 !important;
            text-align: center !important;
            margin: 2rem 0 1rem 0 !important;
        }
        
        .match-card {
            background-color: #f8f9fa; /* Default light grey (offwhite) */
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border-left: 4px solid #1E88E5;
            text-align: center;
        }
        
        .match-card.top1 {
            background-color: #FFD700; /* Bright yellow for Top 1 */
            animation: shake 0.5s infinite; /* Add shaking animation */
        }
        
        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }
        
        .match-card.top2 {
            background-color: #C0C0C0; /* Silver for Top 2 */
        }
        
        .match-card.top3 {
            background-color: #D2B48C; /* Light brown for Top 3 */
        }
        
        .recommendation-section {
            margin-top: 2rem;
            padding: 1.5rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        }
        
        .recommendation-text {
            font-family: 'Open Sans', sans-serif !important;
            font-size: 1.1rem !important;
            color: #34495E !important;
            margin: 1rem 0 !important;
            text-align: center !important;
        }
        
        .site-link {
            color: #1E88E5 !important;
            text-decoration: none !important;
            font-weight: 500 !important;
        }
        
        .site-link:hover {
            text-decoration: underline !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Wait for 2 seconds before showing the fanfare effect
    time.sleep(2)
    
    # Implement the fanfare effect
    st.balloons()  # You can also use st.snow() for a snow effect
    
    # Main title
    st.markdown('<p class="results-title">Your Matches!</p>', unsafe_allow_html=True)
    
    try:
        # Load the trained model
        with open('trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load sample data
        sample_data = pd.read_csv('Sample Data Inputs.csv', skipinitialspace=True)
        sample_data.columns = sample_data.columns.str.strip()
        
        # Convert all columns to numeric
        for col in sample_data.columns:
            sample_data[col] = pd.to_numeric(sample_data[col].apply(lambda x: str(x).strip()), errors='coerce')
        
        # Process candidates
        candidates = []
        for idx, sample_row in sample_data.iterrows():
            features = calculate_features(st.session_state.user_data, sample_row)
            input_vector = prepare_input_vector(features)
            probability = model.predict_proba(input_vector)[0][1]
            
            candidates.append({
                'row_number': idx + 2,
                'age': sample_row['age'],
                'race': sample_row['race'],
                'probability': probability
            })
        
        # Sort and display top 10 candidates
        top_candidates = sorted(candidates, key=lambda x: x['probability'], reverse=True)[:10]
        
        # Display top 10 candidates
        st.markdown('<p class="section-subtitle">Here are your Top 10 matches:</p>', unsafe_allow_html=True)
        for i, candidate in enumerate(top_candidates):
            candidate_race = race_mapping.get(candidate['race'], "Unknown")
            top_label = f"Top {i+1}" if i < 3 else ""
            card_class = f"top{i+1}" if i < 3 else ""
            st.markdown(f"""
                <div class="match-card {card_class}">
                    <p class="recommendation-text">
                        <strong>{top_label}</strong><br>
                        ID: {candidate['row_number']}<br>
                        Race: {candidate_race}<br>
                        Age: {candidate['age']}<br>
                        Match Probability: {candidate['probability']:.2%}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Activity recommendations section
        st.markdown('<p class="section-subtitle">Activity Recommendations</p>', unsafe_allow_html=True)
        
        # Get recommendations for the top match
        if top_candidates:
            recommendations = get_activity_recommendations(
                st.session_state.user_data, 
                top_candidates[0]['row_number'] - 1
            )
            
            if 'candidate_recommendation' in recommendations:
                rec = recommendations['candidate_recommendation']
                st.markdown(f"""
                    <div class="recommendation-section">
                        <p class="recommendation-text">
                            <strong>Based on your top match's interests in {rec['based_on']}:</strong><br>
                            {rec['site']}<br>
                            <a href="{rec['url']}" target="_blank" class="site-link">Visit Website</a>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            if 'user_recommendation' in recommendations:
                rec = recommendations['user_recommendation']
                st.markdown(f"""
                    <div class="recommendation-section">
                        <p class="recommendation-text">
                            <strong>Based on your interests in {rec['based_on']}:</strong><br>
                            {rec['site']}<br>
                            <a href="{rec['url']}" target="_blank" class="site-link">Visit Website</a>
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            rec = recommendations['random_recommendation']
            st.markdown(f"""
                <div class="recommendation-section">
                    <p class="recommendation-text">
                        <strong>Random Recommendation:</strong><br>
                        {rec['site']}<br>
                        <a href="{rec['url']}" target="_blank" class="site-link">Visit Website</a>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    # Add some spacing before the button
    st.write("")
    st.write("")
    
    if st.button("Start Over", key="start_over_button"):
        st.session_state.page = "welcome"
        st.rerun()

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"
    
    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "input":
        user_input_page()
    elif st.session_state.page == "results":
        results_page()

if __name__ == "__main__":
    main() 