FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt streamlit
COPY . .
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
