import pandas as pd
import streamlit as st
import plotly.express as px
import tensorflow as tf
from tensorflow import keras
import time
# import webbrowser

st.set_page_config(page_title="Tuberculosis and Pneumonia")
st.set_option('deprecation.showPyplotGlobalUse', False)

def app():
    
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 500px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    padding_top = 0
    padding_bottom = 10
    padding_left = 1
    padding_right = 10

    st.markdown(f'''
                <style>
                    .block-container .css-1lcbmhc .e1fqkh3o0 {{
                        padding-top: 100rem;
                    }}
                    .reportview-container .main .block-container {{
                        padding-top: 0rem;
                        padding-right: {padding_right}rem;
                        padding-left: {padding_left}rem;
                        padding-bottom: {padding_bottom}rem;
                    }}
                </style>
                ''', unsafe_allow_html=True,
    )

    json_file = open('balanced_dataset_best_model/best_balanced_dataset_model.json','r')
    loaded_model_json = json_file.read()
    json_file.close()

    loaded_model = keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights("balanced_dataset_best_model/best_balanced_dataset_model.h5")

    loaded_model.compile(loss=keras.losses.CategoricalCrossentropy(label_smoothing=0.2), optimizer=keras.optimizers.Adam(), 
                        metrics=["accuracy", keras.metrics.Precision(), keras.metrics.Recall()])

    st.header("Tuberculosis and Pneumonia Detection")
    st.write("""
        #### Please drop your X-Ray image here
    """)

    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        with st.spinner("Please wait for few seconds"):
            time.sleep(10)

        path = "static/uploads/" + uploaded_file.name
        path = path.replace("\\", "")
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        image = keras.utils.load_img(path, target_size=(256, 256))
        img = tf.image.rgb_to_grayscale(image)
        img = tf.expand_dims(img, axis=0) 
        pred = loaded_model.predict(img)[0]

        output_dict = dict(zip(['Normal', 'Pneumonia', 'Tuberculosis'], map(float, pred*100)))
        pred_x = [x for x in output_dict.keys()]
        pred_y = [x for x in output_dict.values()]
        pred_df = pd.DataFrame({"x":pred_x, "y":pred_y})

        output = max(output_dict, key=output_dict.get)
        output_value = round(max(output_dict.values()), 2)

        st.markdown(f"""
            <b> Uploaded X-Ray image is {output} ({output_value}%) </b>
        """, True)

        st.session_state.diagnosis = output

        fig = px.bar(pred_df, x="x", y="y", labels={"x": "", "y": "Prediction probability (in %)"}, 
                    title="Prediction Probability percentage for each label",
                    template="plotly_dark", color="y", color_continuous_scale="bluered")
        fig.update_layout(
                    font_family="Times New Roman", font_color="white", 
                    title_font_family="Times New Roman", xaxis_tickfont_size=16,
                    yaxis_tickfont_size=16, title_x=0.5, showlegend=False
                    )
        st.plotly_chart(fig)

    st.sidebar.header("Model Performance metrics")
    st.sidebar.markdown("""
        <br>
    """, True)

    conf_matrix = pd.read_csv("balanced_dataset_best_model/conf_matrix.csv")
    conf_matrix.index.names = ["Pred/True"]
    conf_matrix.rename(columns={"Unnamed: 0": "True/Pred"}, inplace=True)
    conf_matrix["True/Pred"] = ["Normal (True Label)", "Pnuemonia (True Label)", "Tuberculosis (True Label)"]
    conf_matrix.set_index("True/Pred", inplace=True)    

    st.sidebar.markdown("""
        #### Confusion Matrix
    """, True)
    st.sidebar.table(conf_matrix.style.highlight_max(axis=0, color="green"))

    with st.sidebar.expander("What is a confusion matrix?"):
        st.markdown("""
            <p> <i> In simple words, the above DataFrame is the truth table where it represents if the true label was 'A', 
        how many times our model predicted it as 'A' and the more times the truth label is equal to the predicted label,
        the better and powerful our model will be. </i> </p>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <br>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.sidebar.columns(3)
    col1.metric(label="Accuracy", value="95.0 %")
    col2.metric(label="Precision", value="95.0 %")
    col3.metric(label="Recall", value="92.0 %")

    st.sidebar.markdown("""
        <br>
    """, unsafe_allow_html=True)

    with st.sidebar.expander("Accuracy, Precision and Recall"):
        st.markdown("""
            <p> Accuracy: <i> the number of correct predictions divided by the total number of predictions. </i> </p> 
            <p> Precision: <i> The proportion of positive results that were correctly classified. This tells us what percentage of patients with any diagnosis (tuberculosis or pneumonia) were correctly identified. </i> </p>
            <p> Recall: <i> This tells us what percentage of patients with any following diagnosis (tuberculosis or pneumonia) were identified correctly respectively. Meaning, a tuberculosis infected chest x-ray predicted as tuberculosis and pneumonia infected chest x-ray predicted as pneumonia. </i> </p>
        """, True)

    st.sidebar.markdown("""
        <br>
        <p> If you want to have a look at the architecture of our model, you can download it. <p>
    """, True)

    with open("balanced_dataset_best_model/best_balanced_dataset_model_architecture.png", "rb") as file:
        btn = st.sidebar.download_button(label="Download Model Architecture", data=file, 
                                        file_name="model_summary.png", mime="image/png")

    st.sidebar.markdown("""
        <br>
        <p> If you want to have a look at the loss and accuracy of the model over the span of the number of epochs for which it was trained, you can download it. <p>
    """, True)

    with open("balanced_dataset_best_model/best_balanced_dataset_model_loss_acc_graph.png", "rb") as file:
        btn = st.sidebar.download_button(label="Download Model History",
                                         data=file, file_name="model_history.png", mime="image/png")