import os
from flask import Flask, render_template, request
from n_recomm import recommend_random
import pandas as pd

app = Flask(__name__)

# Load the dataset globally
df = pd.read_csv('netflix_titles_extended.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations', methods=['POST'])
def recommend():
    # Get user preferences
    preferences = {
        'content_type': request.form['content_type'],
        'duration': int(request.form['duration']) if request.form['duration'] else None,
        'audience': request.form['audience'],
        'genre': request.form['genre'],
        'special': request.form['special']
    }

    print("User preferences:", preferences)  # Debugging line

    # Get recommendations
    recommendations = recommend_random(df, preferences, num_recommendations=9)

    print("Recommendations:", recommendations)  # Debugging line

    # Render recommendations
    return render_template('recommendations.html', recommendations=recommendations.to_dict(orient='records') if not isinstance(recommendations, str) else [])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)