import streamlit as st
import google.generativeai as genai

# Set page title
st.set_page_config(page_title="RoofTop Gardening")

# Function to initialize Gemini API (Hardcoded API Key)
def setup_gemini():
    API_KEY = "AIzaSyCZyJ5f0yYJWkxZOp7u-Txo0jgDDBhPB_k"  # Hardcoded API key (Not recommended for security reasons)
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        st.error("⚠️ Error: Could not connect to the API. Please check your API key.")
        return None

# Login Functionality
def login(username, password):
    return username == "sanketh" and password == "rooftop"

# Sidebar Navigation
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Chatbot", "Forum"])

# Home Page
if page == "Home":
    st.title("🌿 Welcome to Our RoofTop Gardening Web App!")
    st.markdown("""
    RoofTop gardening transforms underutilized rooftop spaces into thriving green areas.  
    This web app serves as your **go-to guide** for starting and maintaining a **cost-effective, sustainable** garden right on your terrace.
    """)

    st.header("🌱 Why RoofTop Gardening?")
    st.markdown("""
    - **Utilize Your Space:** Convert rooftops into lush gardens.
    - **Grow Fresh & Organic:** Enjoy pesticide-free, home-grown produce.
    - **Cost-Effective Solutions:** Gardening tips that don’t break the bank.
    - **Health & Well-being:** Gardening reduces stress and promotes a healthier lifestyle.
    - **Eco-Friendly Choice:** Green spaces help lower urban heat and improve air quality.
    """)

# Chatbot Page
elif page == "Chatbot":
    st.title("🤖 Gardening Assistant Chatbot")
    st.markdown("Ask anything about **RoofTop gardening** and get instant responses powered by **Gemini Flash 2 AI**!")

    model = setup_gemini()
    if model:
        user_input = st.text_area("Type your question here...", height=100)
        if st.button("Generate Response 🌿") and user_input:
            with st.spinner("Thinking... 💡"):
                try:
                    response = model.generate_content(user_input)
                    st.subheader("🤖 AI Response:")
                    st.markdown(f"**{response.text}**")
                except Exception as e:
                    st.error("⚠️ Error: Could not process your request. Please check your API key and try again.")

# Forum Page
elif page == "Forum":
    st.title("💬 Community Forum")
    st.markdown("Engage with fellow gardening enthusiasts, ask questions, and share experiences.")

    with st.form(key="forum_form"):
        user_name = st.text_input("Your Name", placeholder="Enter your name")
        post_content = st.text_area("Share your thoughts or ask a question...", height=100)
        submit_button = st.form_submit_button("Post")

        if submit_button and user_name and post_content:
            st.session_state.setdefault("forum_data", []).append({"user": user_name, "content": post_content, "replies": []})
            st.success("✅ Your post has been added!")
            st.experimental_rerun()

    if "forum_data" in st.session_state and st.session_state.forum_data:
        st.write("### 🌿 Community Discussions")
        for idx, post in enumerate(st.session_state.forum_data):
            st.markdown(f"**📝 {post['user']} says:**")
            st.info(post["content"])

            with st.expander("💬 Reply to this post"):
                reply_text = st.text_area(f"Reply to {post['user']}", key=f"reply_{idx}")
                if st.button(f"Reply to {post['user']}", key=f"reply_button_{idx}") and reply_text:
                    post["replies"].append({"user": "Anonymous", "content": reply_text})
                    st.success("✅ Your reply has been posted!")
                    st.experimental_rerun()

            if post["replies"]:
                st.write("📌 **Replies:**")
                for reply in post["replies"]:
                    st.markdown(f"➡️ **{reply['user']}**: {reply['content']}")

st.sidebar.write("🔗 More features coming soon!")
