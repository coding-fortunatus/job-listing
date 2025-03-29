from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from job.models import Job
from django.contrib.auth import get_user_model
User = get_user_model()


def recommend_jobs(user_id, top_n=3):

    user = User.objects.filter(id=user_id).first()
    jobs = Job.objects.all()

    if not user or not jobs:
        return {'error': 'No recommendations'}

    user_df = pd.DataFrame([{
        'user_id': user.id,
        'profile': f"{user.position} {user.work_experience} {user.skills} {user.category} {user.secondary_category}"
    }])

    job_df = pd.DataFrame([{
        'job_id': job.id,
        'title': job.title,
        'description': f"{job.description} {job.job_tags} {job.job_category} {job.requirements}"
    } for job in jobs])

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    user_tfidf = tfidf_vectorizer.fit_transform(user_df["profile"])
    job_tfidf = tfidf_vectorizer.transform(job_df["description"])

    # Compute similarity matrix
    similarity_matrix = cosine_similarity(user_tfidf, job_tfidf)

    # Get top N recommendations
    sim_scores = list(enumerate(similarity_matrix[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:top_n]]

    recommended_jobs = job_df.iloc[top_indices][[
        "job_id", "title"]].to_dict(orient="records")
    return recommended_jobs


def recommendations(request, user_id):
    recommended_jobs = recommend_jobs(user_id)
    jobs = []

    for job in recommended_jobs:
        job_item = Job.objects.filter(id=job["job_id"]).first()
        if job_item:
            jobs.append(job_item)

    return render(request, "site/recommend.html", {"jobs": jobs})
