# Customer_Churn_Predictions

Streamlit.io deployment link: https://manjunathmca1999-customer-churn-predictions-app-7wttsk.streamlit.app/

Docker code:

FROM python:3.10
COPY . .

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
