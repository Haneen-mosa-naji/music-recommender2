
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

# تحميل stopwords مرة واحدة
try:
    arabic_stopwords = stopwords.words('arabic')
except LookupError:
    nltk.download('stopwords')
    arabic_stopwords = stopwords.words('arabic')

# قراءة البيانات
df = pd.read_csv('arabic_music_data.csv')

# تجهيز عمود موحد للنصوص
df['combined'] = df['Title'].fillna('') + ' ' + df['Artist'].fillna('')

# تهيئة TF-IDF
vectorizer = TfidfVectorizer(stop_words=arabic_stopwords)
tfidf_matrix = vectorizer.fit_transform(df['combined'])

def recommend_by_title(title, top_n=5):
    idx = df.index[df['Title'].str.lower() == title.lower()]
    if len(idx) == 0:
        return None 

    idx = idx[0]
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    related_indices = cosine_sim.argsort()[::-1][1:top_n+1]

    recommendations = []
    for i in related_indices:
        recommendations.append({
            'Title': df.iloc[i]['Title'],
            'Artist': df.iloc[i]['Artist'],
            'Similarity': cosine_sim[i],
            'URL': df.iloc[i]['URL'],          # رابط اليوتيوب
            'ImageURL': df.iloc[i]['ImageURL']  # رابط الصورة
            
        })
    return recommendations
