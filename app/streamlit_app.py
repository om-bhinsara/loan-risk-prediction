import streamlit as st
import pickle
import numpy as np

# Load model and scaler
model = pickle.load(open("models/svm_model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

st.title("Loan Approval Prediction System")

st.write("Enter Applicant Details")

# User Inputs
no_of_dependents = st.number_input("Number of Dependents", min_value=0)
education = st.selectbox("Education (0 = Graduate, 1 = Not Graduate)", [0, 1])
self_employed = st.selectbox("Self Employed (0 = No, 1 = Yes)", [0, 1])
income_annum = st.number_input("Annual Income")
loan_amount = st.number_input("Loan Amount")
loan_term = st.number_input("Loan Term (months)")
cibil_score = st.number_input("CIBIL Score")

residential_assets_value = st.number_input("Residential Assets Value")
commercial_assets_value = st.number_input("Commercial Assets Value")
luxury_assets_value = st.number_input("Luxury Assets Value")
bank_asset_value = st.number_input("Bank Asset Value")


if st.button("Predict Loan Status"):

    # Feature Engineering
    total_assets = (
        residential_assets_value
        + commercial_assets_value
        + luxury_assets_value
        + bank_asset_value
    )

    loan_to_income_ratio = loan_amount / income_annum if income_annum != 0 else 0

    asset_to_loan_ratio = total_assets / loan_amount if loan_amount != 0 else 0

    income_per_dependent = income_annum / (no_of_dependents + 1)

    # Final feature vector (15 features)
    data = np.array([
        no_of_dependents,
        education,
        self_employed,
        income_annum,
        loan_amount,
        loan_term,
        cibil_score,
        residential_assets_value,
        commercial_assets_value,
        luxury_assets_value,
        bank_asset_value,
        total_assets,
        loan_to_income_ratio,
        asset_to_loan_ratio,
        income_per_dependent
    ])

    # Scaling
    data_scaled = scaler.transform([data])

    # Prediction
    prediction = model.predict(data_scaled)

    if prediction[0] == 1:
        st.success("Loan can be given to the applicant ✅")
        st.write("The applicant satisfies the financial criteria for loan approval.")
    else:
        st.error("Loan cannot be given to the applicant ❌")
        st.write("The applicant does not satisfy the required financial conditions.")