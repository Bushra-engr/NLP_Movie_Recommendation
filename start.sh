#!/bin/bash
# Backend ko background mein chalao (&)
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Frontend ko foreground mein chalao
streamlit run app.py --server.port=8501 --server.address=0.0.0.0