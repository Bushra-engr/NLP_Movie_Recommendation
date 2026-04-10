# 🎬 Movie Recommender System (End-to-End)

A modern, full-stack movie recommendation engine built with **Machine Learning (TF-IDF)**, a **FastAPI** backend, and a **Streamlit** frontend, all orchestrated using **Docker Compose**.

## 🚀 Features
- **Smart Recommendations**: Content-based filtering using TF-IDF and Cosine Similarity.
- **Live Search**: Auto-suggestions and real-time movie search via TMDB API.
- **Interactive UI**: Clean, professional dashboard with movie banners, posters, and details.
- **Containerized Architecture**: Backend and Frontend running in sync using Docker Compose.
- **Microservices Ready**: Decoupled architecture for high performance and scalability.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Uvicorn)
- **ML Model**: Scikit-Learn (TF-IDF Vectorizer)
- **Data**: TMDB ~50k samples Movies Dataset
- **DevOps**: Docker & Docker Compose

---

## 🏗️ Project Architecture

The application uses a unified Docker environment. The Streamlit frontend communicates with the FastAPI backend over a local bridge network to fetch metadata and compute similarity scores.


---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Bushra-engr/NLP_Movie_Recommendation.git](https://github.com/Bushra-engr/NLP_Movie_Recommendation.git)
cd NLP_Movie_Recommendation
