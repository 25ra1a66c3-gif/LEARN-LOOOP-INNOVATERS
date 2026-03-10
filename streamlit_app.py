import streamlit as st
from gtts import gTTS
import io
import base64
import graphviz as graphviz

# Page config
st.set_page_config(page_title="LearnSphere", page_icon="🧠", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .welcome-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-icons {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    .feature-icons div {
        text-align: center;
        font-size: 1rem;
        color: #636e72;
    }
    .feature-icons div .icon {
        font-size: 2rem;
        display: block;
        margin-bottom: 5px;
    }
    .login-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        padding: 40px;
        max-width: 400px;
        margin: auto;
        text-align: center;
    }
    .card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .btn-primary {
        background: linear-gradient(135deg, #5d5fef, #3b3fd9);
        color: white;
        border: none;
        padding: 12px 32px;
        border-radius: 25px;
        font-size: 1rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

def login():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.subheader("Login to LearnSphere")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.page = 'dashboard'
            st.rerun()
        else:
            st.error("Please enter username and password")
    st.markdown('</div>', unsafe_allow_html=True)

def welcome():
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.title("Welcome to LearnSphere")
    st.write("Your AI-powered platform for mastering Machine Learning. Get explanations, coding labs, and visual tools all in one place.")
    if st.button("Start Learning", key="start"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown("""
    <div class="feature-icons">
        <div><span class="icon">🤖</span>AI Tutor</div>
        <div><span class="icon">💻</span>Coding Labs</div>
        <div><span class="icon">🎨</span>Visual Learning</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def dashboard():
    st.title("Learning Mode")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("📖")
        st.subheader("Text Explanation")
        st.write("Get structured learning paths for any ML topic.")
        if st.button("Start Learning", key="text"):
            st.session_state.page = 'text'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("💻")
        st.subheader("Code Examples")
        st.write("Explore interactive code examples for ML algorithms.")
        if st.button("Generate Code", key="code"):
            st.session_state.page = 'code'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("🎵")
        st.subheader("Audio Lessons")
        st.write("Access audio lessons for immersive learning.")
        if st.button("Generate Audio", key="audio"):
            st.session_state.page = 'audio'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("🖼️")
        st.subheader("Visual Diagrams")
        st.write("Visualize complex architectures and flows.")
        if st.button("Visualize Now", key="visual"):
            st.session_state.page = 'visual'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def text_explanation():
    st.title("Text Explanation")
    topic = st.text_input("What would you like to learn?", "Machine Learning")
    if st.button("Generate Explanation"):
        st.subheader(f"Learning: {topic}")
        st.write("**Information:** Here is some general information about the topic to help you understand the context.")
        st.write(f"**Summary:** {topic} is a fundamental concept in machine learning that involves understanding patterns in data. It forms the basis for many advanced algorithms and applications in data science.")
        st.write("**Key Points:**")
        st.markdown("""
        - **Definition:** Refers to the process of teaching computers to learn from data.
        - **Importance:** Crucial for building intelligent systems.
        - **Components:** Data, algorithms, and computational power.
        - **Advantages:** Automation, accuracy, handling complex tasks.
        """)
        st.write("**Real World Applications:**")
        st.markdown("""
        - **Healthcare:** Medical diagnosis and monitoring.
        - **Finance:** Fraud detection and trading.
        - **Retail:** Recommendation systems.
        - **Autonomous Vehicles:** Computer vision.
        """)
    if st.button("Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

def code_examples():
    st.title("Code Examples")
    topic = st.text_input("Topic for Code", "Linear Regression")
    if st.button("Generate Code"):
        st.subheader(f"Generated Python Code for {topic}")
        code = """
import numpy as np
from sklearn.linear_model import LinearRegression

# Model initialization
model = LinearRegression()
print('Model ready for data!')
        """
        st.code(code, language='python')
    if st.button("Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

def audio_lessons():
    st.title("Audio Lessons")
    topic = st.text_input("Enter a Machine Learning topic", "Neural Networks")
    if st.button("Generate Audio Lesson"):
        text = f"""
        Welcome to your audio lesson on {topic}.
        
        Summary: {topic} is a fundamental concept in machine learning that involves understanding patterns in data.
        
        Key Points:
        - Definition: Refers to the process of teaching computers to learn from data.
        - Importance: Crucial for building intelligent systems.
        - Components: Data, algorithms, and computational power.
        - Advantages: Automation, accuracy, handling complex tasks.
        
        Real World Applications:
        - Healthcare: Medical diagnosis.
        - Finance: Fraud detection.
        - Retail: Recommendations.
        - Autonomous Vehicles: Computer vision.
        
        Thank you for listening.
        """
        st.write("**Generated Text:**")
        st.write(text)
        
        # Generate audio
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_bytes = audio_buffer.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        # Download
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="audio_lesson.mp3">Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
    if st.button("Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

def visual_diagrams():
    st.title("Visual Diagrams")
    topic = st.text_input("What would you like to visualize?", "Decision Tree")
    if st.button("Generate Visual"):
        if "decision tree" in topic.lower():
            graph = graphviz.Digraph()
            graph.node('A', 'Root Node\nFeature: Age')
            graph.node('B', '<=30')
            graph.node('C', '>30')
            graph.node('D', 'Leaf: Yes\nClass: Buy')
            graph.node('E', 'Leaf: No\nClass: Not Buy')
            graph.node('F', 'Leaf: Yes\nClass: Buy')
            graph.node('G', 'Leaf: No\nClass: Not Buy')
            graph.edges(['AB', 'AC', 'BD', 'BE', 'CF', 'CG'])
            st.graphviz_chart(graph)
        elif "neural network" in topic.lower():
            st.write("Neural Network Diagram (placeholder)")
            # Could add more diagrams
        else:
            st.write("Default ML Workflow")
            graph = graphviz.Digraph()
            graph.node('A', 'Start')
            graph.node('B', 'Process Data')
            graph.node('C', 'Train Model')
            graph.node('D', 'Validate')
            graph.node('E', 'Deploy')
            graph.edges(['AB', 'BC', 'CD', 'DE'])
            st.graphviz_chart(graph)
    if st.button("Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# Main app logic
if st.session_state.page == 'welcome':
    welcome()
elif st.session_state.page == 'login':
    login()
elif st.session_state.page == 'dashboard':
    if st.session_state.logged_in:
        dashboard()
    else:
        st.session_state.page = 'welcome'
        st.rerun()
elif st.session_state.page == 'text':
    text_explanation()
elif st.session_state.page == 'code':
    code_examples()
elif st.session_state.page == 'audio':
    audio_lessons()
elif st.session_state.page == 'visual':
    visual_diagrams()

# Logout option
if st.session_state.logged_in and st.session_state.page != 'welcome':
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = 'welcome'
        st.rerun()