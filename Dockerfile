FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ✅ Key directly baked into image
ENV TMDB_API_KEY=5f70da5489576ec78c2df4f64b021a1e

EXPOSE 8000
EXPOSE 8501
RUN chmod +x start.sh
CMD ["sh", "start.sh"]