import pandas as pd
import random

def recommend_random(df, preferences, num_recommendations=9, random_seed=None):
    if random_seed is not None:
        random.seed(random_seed)

    # Filter by content type
    if preferences['content_type'].lower() == 'long form':
        df = df[df['type'] == 'TV Show']
        if preferences['duration']:
            df = df[df['duration'] <= preferences['duration']]
    elif preferences['content_type'].lower() == 'short form':
        df = df[df['type'] == 'Movie']

    # Adjusted audience filtering
    if preferences['audience'] == 'Adults':
        df = df[df['rating'].isin(['R', 'TV-MA', 'PG-13', 'TV-14', 'PG', 'G', 'TV-Y', 'TV-Y7'])]
    elif preferences['audience'] == 'Teens':
        df = df[df['rating'].isin(['PG-13', 'TV-14', 'PG', 'G', 'TV-Y', 'TV-Y7'])]
    elif preferences['audience'] == 'Kids':
        df = df[df['rating'].isin(['PG', 'G', 'TV-Y', 'TV-Y7'])]

    # Filter by genre
    df = df[df['genre'].str.contains(preferences['genre'], case=False, na=False)]

    # Filter by popularity or awards
    special = preferences['special'].lower()
    if special == 'new' or special == '1':
        df = df[df['release_year'] >= 2020]
    elif special == 'popular' or special == '2':
        df = df[df['popularity'] == 'High']
    elif special == 'award winning' or special == '3':
        df = df[df['awards'] == 'Yes']

    # Check if any content is available after filtering
    if df.empty:
        return "No recommendations available for the specified criteria."

    # Select multiple random titles from the filtered DataFrame
    num_available = len(df)
    num_recommendations = min(num_recommendations, num_available)

    # Use the random seed here if needed
    if random_seed is not None:
        recommendations = df.sample(n=num_recommendations, random_state=random_seed)
    else:
        recommendations = df.sample(n=num_recommendations)

    return recommendations[['title', 'type', 'genre', 'rating', 'release_year']]

# No need for get_user_preferences or main function since those are handled by Flask
