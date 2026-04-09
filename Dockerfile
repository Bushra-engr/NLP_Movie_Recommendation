FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Dono ports kholo
EXPOSE 8000
EXPOSE 8501

# Start script ko permission do aur chalao
RUN chmod +x start.sh
CMD ["./start.sh"]