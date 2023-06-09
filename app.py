import pickle as pkl
import streamlit as st

# Loading scaler and model
scaler = pkl.load(open('scaler.pkl', 'rb'))
model = pkl.load(open('model.pkl', 'rb'))

# User input
def get_user_input() -> list[int]:

    input_container = st.container()

    with input_container:

        col1, col2 = st.columns(2)

        with col1:

            pregnancies = st.number_input('Pregnancy Count', value=0, min_value=0, max_value=30)
            glucose = st.number_input('Glucose Concentration (mg / dL)', value=121.0, min_value=0.0, max_value=250.0, step=1., format='%.2f')
            blood_pressure = st.number_input('Diastolic Blood Pressure (mmHg)', value=69.1, min_value=0.0, max_value=250.0, step=1., format='%.2f')
            kg = st.number_input('Your Mass (kg)', value=51.0, min_value=0.1, max_value=500.0, step=1., format='%.2f')
            
        with col2:

            age = st.number_input('Current Age', value=20, min_value=0, max_value=150)
            insulin = st.number_input('Insulin Concentration (μU / ml)', value=79.8, min_value=0.0, max_value=250.0, step=1., format='%.2f')
            skin_thickness = st.number_input('Tricep Skin Fold Thickness (mm)', value=20.5, min_value=1.0, max_value=500.0, step=1., format='%.2f')
            height = st.number_input('Your Height (m)', value=150.0, min_value=1.0, max_value=250.0, step=1., format='%.2f')

        diabetes_pedigree_function = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=1000.0, step=1., format='%.2f')

        bmi = kg / (height ** 2)

    return [pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age]

# Display result
def show_result(user_input: list[int]) -> None:
    result = model.predict(scaler.transform([user_input]))

    st.markdown('## Result')

    if result == 0:
        st.write(f'You are **UNLIKELY** to get diabetes!')
    else:
        st.write(f'You are **LIKELY** to get diabetes!')
        featuresExceededLevel(user_input)
        show_recommendation(user_input)
        
def featuresExceededLevel(user_input):
    if user_input[1] > 126:
        st.write('- High glucose concentration')

    if user_input[3] > 20:
        st.write('- Thick skin')

    if user_input[4] > 230:
        st.write('- High insulin concentration')

    if user_input[4] < 30:
        st.write('- Low insulin concentration')

    if user_input[5] > 25:
        st.write('- Overweight')

def show_recommendation(user_input):
    st.write('Tips on improving your health\n')
    if user_input[1] > 126:
        st.write('- Manage your carbohydrate intake')
        st.write('- Get enough quality sleep')

    if user_input[3] > 20:
        st.write('- Increase physical activity')

    if user_input[4] > 230:
        st.write('- Manage your food portions')

    if user_input[4] < 30:
        st.write('- Have foods that boost natural insulin')

    if user_input[5] > 25:
        st.write('- Reduce daily calorie intake')
        st.write('- Reduce your weight')

# UI
st.title('Diabetes Risk Calculator')
user_input_arr = get_user_input()
result_button = st.button('Predict', use_container_width=True)

if result_button: show_result(user_input_arr)
else: st.write()
