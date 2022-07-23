import streamlit as st
import pandas as pd

df = pd.read_csv("mod_hospitals.csv").reset_index(drop=True)
df.rename(columns={"hospital_name": "Hospital Name"}, inplace=True)

def app():

    if "username" in st.session_state:
        st.markdown(f"""
            <b> Welcome, {st.session_state.username} </b>
        """, True)

    if "location" not in st.session_state:
        location = st.selectbox("Enter your city name or the closest city to you", df.location.unique().tolist())
        if location:
            st.markdown(f"""
                    <h3> List of Hospitals in {location} </h3>
                """, True)

            list_of_hosp = df[df["location"]==location]["Hospital Name"].tolist()
            st.dataframe(pd.DataFrame(list_of_hosp, columns=["Hospital Name"], index=list(range(1, len(list_of_hosp)+1))))
    else:
        st.markdown(f"""
                    <h3> List of Hospitals in {st.session_state.location} </h3>
            """, True)

        list_of_hosp = df[df["location"]==st.session_state.location]["Hospital Name"].tolist()
        st.dataframe(pd.DataFrame(list_of_hosp, columns=["Hospital Name"], index=list(range(1, len(list_of_hosp)+1))))

    st.markdown("""
        <hr> 
        """, True)

    classes = ["Normal", "Pneumonia", "Tuberculosis"]

    if "diagnosis" in st.session_state:
        if st.session_state.diagnosis == "Pneumonia":
            st.markdown("""
                #### Precautions to be taken if you're diagnosed with Pneumonia
            """, True)

            st.markdown("""
                <ul>
                    <li> Wash your hands regularly, especially after you go to the bathroom and before you eat. </li>
                    <li> Being around people who are sick increases your risk of catching what they have. </li>
                    <li> Smoking damages your lungs and makes it harder for your body to defend itself from germs and disease. If you smoke, talk to your family doctor about quitting as soon as possible. </li>
                </ul>
            """, True)

        elif st.session_state.diagnosis == "Tuberculosis":
            st.markdown("""
                #### Precautions to be taken if you're diagnosed with Tuberculosis
            """, True)

            st.markdown("""
                <ul>
                    <li> Always cover your mouth with a tissue when you cough or sneeze. Wash your hands after coughing or sneezing. </li>
                    <li> Use a fan or open windows to move around fresh air. </li>
                    <li> Take all of your medicines as they’re prescribed, until your doctor takes you off them. </li>
                </ul>
            """, True)

        elif st.session_state.diagnosis == "Normal":
            st.markdown("""
                #### For normal chest X-ray predictions
            """, True)

            st.markdown("""
                <ul> <li> <h6> Likely consult a doctor for 100 percent confirmation </h6> </li> </ul>
            """, True)
    else:
        diagnosis = st.selectbox("Which disease are you diagnosed with?", classes)

        if diagnosis == "Pneumonia":
            st.markdown("""
                #### Precautions to be taken if you're diagnosed with Pneumonia
            """, True)

            st.markdown("""
                <ul>
                    <li> Wash your hands regularly, especially after you go to the bathroom and before you eat. </li>
                    <li> Being around people who are sick increases your risk of catching what they have. </li>
                    <li> Smoking damages your lungs and makes it harder for your body to defend itself from germs and disease. If you smoke, talk to your family doctor about quitting as soon as possible. </li>
                </ul>
            """, True)

        elif diagnosis == "Tuberculosis":
            st.markdown("""
                #### Precautions to be taken if you're diagnosed with Tuberculosis
            """, True)

            st.markdown("""
                <ul>
                    <li> Always cover your mouth with a tissue when you cough or sneeze. Wash your hands after coughing or sneezing. </li>
                    <li> Use a fan or open windows to move around fresh air. </li>
                    <li> Take all of your medicines as they’re prescribed, until your doctor takes you off them. </li>
                </ul>
            """, True)

        elif diagnosis == "Normal":
            st.markdown("""
                #### For normal chest X-ray predictions
            """, True)

            st.markdown("""
                <ul> <li> <h6> Likely consult a doctor for 100 percent confirmation </h6> </li> </ul>
            """, True)