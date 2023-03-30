import pickle
import streamlit as st
import pandas as pd
from PIL import Image
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction import DictVectorizer
from sklearn.compose import ColumnTransformer

import time
bar = st.progress(2)
for i in range(100):
    time.sleep(0.04)
    bar.progress(i + 1)
with st.spinner('Wait for it...'):
    time.sleep(3)

model_file = 'artifacts/model_C=1.0.bin'


with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)


def main():

	image = Image.open('images/icon.png')
	image2 = Image.open('images/image.png')
	st.image(image,use_column_width=False)
	add_selectbox = st.sidebar.selectbox(
	"How would you like to predict?",
	("Online", "Batch"))
	st.sidebar.info('This app is created to predict Customer Churn')
	st.sidebar.image(image2)
	st.title("Predicting Customer Churn")
	if add_selectbox == 'Online':
		gender = st.selectbox('Gender:', ['male', 'female'])
		seniorcitizen= st.selectbox(' Customer is a senior citizen:', [0, 1])
		partner= st.selectbox(' Customer has a partner:', ['yes', 'no'])
		dependents = st.selectbox(' Customer has  dependents:', ['yes', 'no'])
		phoneservice = st.selectbox(' Customer has phoneservice:', ['yes', 'no'])
		multiplelines = st.selectbox(' Customer has multiplelines:', ['yes', 'no', 'no_phone_service'])
		internetservice= st.selectbox(' Customer has internetservice:', ['dsl', 'no', 'fiber_optic'])
		onlinesecurity= st.selectbox(' Customer has onlinesecurity:', ['yes', 'no', 'no_internet_service'])
		onlinebackup = st.selectbox(' Customer has onlinebackup:', ['yes', 'no', 'no_internet_service'])
		deviceprotection = st.selectbox(' Customer has deviceprotection:', ['yes', 'no', 'no_internet_service'])
		techsupport = st.selectbox(' Customer has techsupport:', ['yes', 'no', 'no_internet_service'])
		streamingtv = st.selectbox(' Customer has streamingtv:', ['yes', 'no', 'no_internet_service'])
		streamingmovies = st.selectbox(' Customer has streamingmovies:', ['yes', 'no', 'no_internet_service'])
		contract= st.selectbox(' Customer has a contract:', ['month-to-month', 'one_year', 'two_year'])
		paperlessbilling = st.selectbox(' Customer has a paperlessbilling:', ['yes', 'no'])
		paymentmethod= st.selectbox('Payment Option:', ['bank_transfer_(automatic)', 'credit_card_(automatic)', 'electronic_check' ,'mailed_check'])
		tenure = st.number_input('Number of months the customer has been with the current telco provider :', min_value=0, max_value=240, value=0)
		monthlycharges= st.number_input('Monthly charges :', min_value=0, max_value=240, value=0)
		totalcharges = tenure*monthlycharges
		output= ""
		output_prob = ""
		input_dict={
				"gender":gender ,
				"seniorcitizen": seniorcitizen,
				"partner": partner,
				"dependents": dependents,
				"phoneservice": phoneservice,
				"multiplelines": multiplelines,
				"internetservice": internetservice,
				"onlinesecurity": onlinesecurity,
				"onlinebackup": onlinebackup,
				"deviceprotection": deviceprotection,
				"techsupport": techsupport,
				"streamingtv": streamingtv,
				"streamingmovies": streamingmovies,
				"contract": contract,
				"paperlessbilling": paperlessbilling,
				"paymentmethod": paymentmethod,
				"tenure": tenure,
				"monthlycharges": monthlycharges,
				"totalcharges": totalcharges
			}

		if st.button("Predict"):
			X = dv.transform([input_dict])
			y_pred = model.predict_proba(X)[0, 1]
			churn = y_pred >= 0.5
			output_prob = float(y_pred)
			output = bool(churn)
		st.success('Customer Churn status will be : {0} **AND** Risk Score will be : {1}'.format(output, output_prob))
		
			
		if st.button("Recommendations"):
			if output==True:
				st.info("**Customer need to be taken care with additional services**")
			else:
				st.info("**No worries...The customer is happy with the service**")
	
		

	if add_selectbox == 'Batch':
		file_upload = st.file_uploader("Upload csv file for predictions", type=["xlsx"])
		if file_upload is not None:
			df= pd.read_excel(file_upload)
			df.columns = df.columns.str.lower().str.replace(' ', '_')
			string_columns = list(df.dtypes[df.dtypes == 'object'].index)
			for col in string_columns:
				df[col] = df[col].str.lower().str.replace(' ', '_')
			
			cat_features = df.select_dtypes(include="object").columns
			num_features = df.select_dtypes(exclude="object").columns

			numeric_transformer = StandardScaler()
			oh_transformer = OneHotEncoder()
			preprocessor = ColumnTransformer(
				[
					("OneHotEncoder", oh_transformer, cat_features),
					("StandardScaler", numeric_transformer, num_features),        
					]
				)

			X = preprocessor.fit_transform(df)
			y_pred = model.predict_proba(X)[0, 1]
			churn = y_pred >= 0.5
			output_prob = float(y_pred)
			output = bool(churn)
			st.success('Overall customer Risk Score will be : {0}'.format(output_prob))

			if st.button("Recommendations"):
				if output==True:
					st.info("**Customer need to be taken care with additional services**")
				else:
					st.info("**No worries...The customer is happy with the service**")
	
			

if __name__ == '__main__':
	main(debug=True)
