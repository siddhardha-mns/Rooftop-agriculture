import streamlit as st


# Set page title and layout
st.set_page_config(page_title="RoofTop Gardening", layout="wide")

# Apply custom CSS for background image (without white overlay)
page_bg_img = f"""
<style>
    body {{
        background-image: url("https://sl.bing.net/df80MIH7xYq");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp {{
        padding: 20px;
        border-radius: 10px;
    }}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Login Functionality
def login(username, password):
    if username == "sanketh" and password == "rooftop":
        return True
    return False

# Login Form in Top Right Corner
col1, col2 = st.columns([4, 1])  # Adjust column widths for layout
with col2:
    with st.expander("🔑 Login"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        login_button = st.button("Login")

        if login_button:
            if login(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Login unsuccessful. Please check your credentials.")

# Sidebar Navigation
st.sidebar.title("🌿 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Chatbot", "Forum"])

# Function to initialize Gemini API (Flash 2 - Free Version)
def setup_gemini():
    API_KEY = "AIzaSyCZyJ5f0yYJWkxZOp7u-Txo0jgDDBhPB_k"  # Replace with your actual API key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using Flash 2 (Free version)
    return model

# Initialize session state for forum discussions
if "forum_data" not in st.session_state:
    st.session_state.forum_data = []

# Home Page
if page == "Home":
    st.title("🌿 Welcome to Our RoofTop Gardening Web App!")
    
    st.markdown("""
    RoofTop gardening transforms underutilized rooftop spaces into thriving green areas.  
    This web app serves as your **go-to guide** for starting and maintaining a **cost-effective, sustainable** garden right on your terrace.  

    With easy-to-follow tips and expert recommendations, you can enjoy **fresh, organic produce** while contributing to a greener environment.
    """)

    st.header("🌱 Why RoofTop Gardening?")
    st.markdown("""
    - **Utilize Your Space:** Convert rooftops into lush gardens.
    - **Grow Fresh & Organic:** Enjoy pesticide-free, home-grown produce.
    - **Cost-Effective Solutions:** Gardening tips that don’t break the bank.
    - **Health & Well-being:** Gardening reduces stress and promotes a healthier lifestyle.
    - **Eco-Friendly Choice:** Green spaces help lower urban heat and improve air quality.
    """)

    st.header("🚀 What You’ll Find Here")
    st.markdown("""
    ✅ **Step-by-step gardening guides**  
    ✅ **Best plants for rooftop gardening**  
    ✅ **DIY solutions for low-cost gardening**  
    ✅ **Organic farming techniques**  
    ✅ **Community & expert advice**  
    """)

    st.info("🌍 Start your RoofTop gardening journey today and make a positive impact on your health and the environment!")

# Chatbot Page (Gemini Flash 2 API Integration)
elif page == "Chatbot":
    st.title("🤖 Gardening Assistant Chatbot")
    st.markdown("Ask anything about **RoofTop gardening** and get instant responses powered by **Gemini Flash 2 AI**!")

    # Initialize Gemini Model
    model = setup_gemini()

    # Chat UI
    with st.container():
        st.write("### 🌱 Ask Your Gardening Question Below:")
        user_input = st.text_area("Type your question here...", height=100)

        # Submit button
        if st.button("Generate Response 🌿"):
            if user_input:
                with st.spinner("Thinking... 💡"):
                    try:
                        response = model.generate_content(user_input)
                        st.subheader("🤖 AI Response:")
                        st.markdown(f"**{response.text}**")
                    except Exception as e:
                        st.error("⚠️ Error: Could not process your request. Please check your API key and try again.")
            else:
                st.warning("⚠️ Please enter a question before submitting.")

# Forum Page (Community Discussions)
elif page == "Forum":
    st.title("💬 Community Forum")
    st.markdown("Engage with fellow gardening enthusiasts, ask questions, and share experiences.")

    # Form to submit a new discussion
    with st.form(key="forum_form"):
        user_name = st.text_input("Your Name", placeholder="Enter your name")
        post_content = st.text_area("Share your thoughts or ask a question...", height=100)
        submit_button = st.form_submit_button("Post")

        if submit_button and user_name and post_content:
            new_post = {"user": user_name, "content": post_content, "replies": []}
            st.session_state.forum_data.append(new_post)
            st.success("✅ Your post has been added!")
            st.experimental_rerun()

    # Display all forum posts
    if st.session_state.forum_data:
        st.write("### 🌿 Community Discussions")
        for idx, post in enumerate(st.session_state.forum_data):
            with st.container():
                st.markdown(f"**📝 {post['user']} says:**")
                st.info(post["content"])
                
                # Form to reply to a post
                with st.expander("💬 Reply to this post"):
                    reply_text = st.text_area(f"Reply to {post['user']}", key=f"reply_{idx}")
                    if st.button(f"Reply to {post['user']}", key=f"reply_button_{idx}"):
                        if reply_text:
                            post["replies"].append({"user": "Anonymous", "content": reply_text})
                            st.success("✅ Your reply has been posted!")
                            st.experimental_rerun()
                        else:
                            st.warning("⚠️ Please enter a reply before submitting.")

                # Display replies
                if post["replies"]:
                    st.write("📌 **Replies:**")
                    for reply in post["replies"]:
                        st.markdown(f"➡️ **{reply['user']}**: {reply['content']}")

# Footer
st.sidebar.write("🔗 More features coming soon!")
