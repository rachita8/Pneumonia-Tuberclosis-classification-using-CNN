import streamlit as st
import pandas as pd
from db_helper import *

# avatar1 ="https://www.w3schools.com/howto/img_avatar1.png"
# avatar2 ="https://www.w3schools.com/howto/img_avatar2.png"

# var = """ <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle; width: 50px;height: 50px;border-radius: 50%;" > """

title_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<u> <h4 style="color:white;text-align:center;">{}</h4> </u>
	<h6 style="display: inline-block; font-size: 20px;"> By {}</h6>
    <br>
	<p style="text-align:justify">{}</p>
	</div>
	"""

article_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<u> <h4 style="color:white;text-align:center;">{}</h4> </u>
	<h6 style="font-size: 20px;">By {}</h6> 
	<p style="text-align:justify">{}</p>
	</div>
	"""

head_message_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
	<u> <h4 style="color:white;text-align:center;">{}</h4> </u>
	<h6 style="font-size: 20px;"> By {}</h6> 			
	</div>
	"""

full_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<p style="text-align:justify;color:black;padding:10px">{}</p>
	</div>
	"""

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
df = pd.read_csv("mod_hospitals.csv")

def app():
    
    menu = ["Home","View Posts","Add Post","Search","Manage Query"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.markdown("<h3 style='text-align: center;'>Home</h3>", unsafe_allow_html=True)	
        result = view_all_notes()

        for i in result:
            short_article = str(i[2])[0:100]
            st.write(title_temp.format(i[1],i[0],short_article),unsafe_allow_html=True)

    elif choice == "View Posts":
        st.markdown("<h3 style='text-align: center;'>View Posts</h3>", unsafe_allow_html=True)	

        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("Posts",all_titles)
        post_result = get_blog_by_title(postlist)

        for i in post_result:
            st.markdown(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
            st.markdown(full_message_temp.format(i[2]),unsafe_allow_html=True)

    elif choice == "Add Post":
        st.markdown("<h3 style='text-align: center;'>Add your Query</h3>", unsafe_allow_html=True)	
        create_table()
        blog_title = st.text_input('Enter Post Title')
        blog_author = st.text_input("Enter Author Name",max_chars=50)
        blog_article = st.text_area("Enter Your Message",height=200)
        user_location = st.selectbox("Enter your city name or the closest city to you", df.location.unique().tolist())
        blog_post_date = st.date_input("Post Date")

        st.session_state.username = blog_author
        st.session_state.location = user_location

        if st.button("Add"):
            add_data(blog_author,blog_title,blog_article,user_location,blog_post_date)
            st.success("Post::'{}' Saved".format(blog_title))

    elif choice == "Search":
        st.markdown("<h3 style='text-align: center;'>Search</h3>", unsafe_allow_html=True)	
        search_term = st.text_input("Enter Term")
        search_choice = st.radio("Field to Search",("title","author"))

        if st.button('Search'):
            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice =="author":
                article_result = get_blog_by_author(search_term)
 
            for i in article_result:
    
                # st.write(article_temp.format(i[1],i[0],i[3],i[2]),unsafe_allow_html=True)
                st.write(head_message_temp.format(i[1],i[0],i[3]),unsafe_allow_html=True)
                st.write(full_message_temp.format(i[2]),unsafe_allow_html=True)	

    elif choice == "Manage Query":
        st.markdown("<h3 style='text-align: center;'>Manage Query</h3>", unsafe_allow_html=True)	
        result = view_all_notes()
        
        clean_db = pd.DataFrame(result,columns=["Author","Title","Article","Location","Date"])
        st.dataframe(clean_db)
        unique_list = [i[0] for i in view_all_titles()]
        delete_by_title =  st.selectbox("Select Title",unique_list)

        if st.button("Delete"):
            delete_data(delete_by_title)
            st.warning("Deleted: '{}'".format(delete_by_title))