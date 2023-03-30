FROM python:3.10
COPY . .

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
