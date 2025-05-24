from flask import Flask, render_template, request
from recommender import recommend_by_title
import pandas as pd
import os 

app = Flask(__name__)
df = pd.read_csv("arabic_music_data.csv")
song_titles = df['Title'].tolist()

@app.route('/')
def home():
    return render_template('index.html', names=song_titles)

@app.route('/recom', methods=['POST'])
def recom():
    selected_song = request.form['names']
    recommendations = recommend_by_title(selected_song)

    if recommendations is None or isinstance(recommendations, str):
        error_message = f"الأغنية '{selected_song}' غير موجودة في قاعدة البيانات."
        return render_template('index.html', names=song_titles, songs=[], error=error_message)

    return render_template('index.html', names=song_titles, songs=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
