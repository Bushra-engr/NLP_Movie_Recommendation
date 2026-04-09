FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Scripts ko executable banao aur chalao
RUN chmod +x start.sh
CMD ["sh", "start.sh"]