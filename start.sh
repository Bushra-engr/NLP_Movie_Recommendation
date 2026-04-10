uvicorn main:app --host 0.0.0.0 --port 8000 &
sleep 3
streamlit run app.py --server.port=8501 --server.address=0.0.0.0