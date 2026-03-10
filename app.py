from flask import Flask, request, jsonify, send_file, render_template_string
from gtts import gTTS
import io
import os

app = Flask(__name__)

# Store the HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edu Orbit - ML Learning Assistant</title>
    <style>
        :root {
            --primary: #5d5fef;
            --bg: #f8faff;
            --card-bg: #ffffff;
            --text-dark: #2d3436;
            --text-light: #636e72;
        }

        body { 
            font-family: 'Inter', 'Segoe UI', sans-serif; 
            margin: 0; 
            background-color: var(--bg); 
            color: var(--text-dark);
            line-height: 1.6;
        }

        /* --- Header & Navigation --- */
        header { 
            background: var(--primary); 
            color: white; 
            padding: 40px 20px 80px 20px; 
            text-align: center;
        }

        .logo { font-size: 2rem; font-weight: bold; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        
        nav { margin-top: 20px; }
        nav button {
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            padding: 8px 18px;
            margin: 0 5px;
            border-radius: 20px;
            cursor: pointer;
            transition: 0.3s;
        }
        nav button:hover { background: rgba(255, 255, 255, 0.3); }

        /* --- Layout Containers --- */
        .container { max-width: 1000px; margin: -50px auto 50px auto; padding: 0 20px; }
        
        .view-section { display: none; animation: fadeIn 0.4s ease-in-out; }
        .view-section.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- Card & Grid Styling --- */
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        
        .card { 
            background: var(--white); 
            padding: 30px; 
            border-radius: 15px; 
            text-align: center; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            background: white;
        }

        .icon-box { font-size: 40px; margin-bottom: 15px; }

        /* --- Welcome Section --- */
        .welcome-section {
            text-align: center;
            margin-bottom: 50px;
            padding: 40px 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        }
        .welcome-section h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
            color: var(--primary);
        }
        .welcome-section p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: var(--text-light);
        }

        /* --- Form Elements --- */
        .input-group { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        label { display: block; margin-bottom: 8px; font-weight: 600; }
        input, select, textarea { 
            width: 100%; padding: 12px; margin-bottom: 20px; 
            border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;
        }

        .btn-main {
            background: var(--primary); color: white; border: none; 
            padding: 12px 30px; border-radius: 25px; cursor: pointer; font-weight: bold;
        }

        /* --- Results Area --- */
        .result-area { 
            margin-top: 30px; padding: 25px; background: #fff; 
            border-left: 5px solid var(--primary); border-radius: 8px; display: none;
        }
        pre { background: #2d3436; color: #fab1a0; padding: 15px; border-radius: 8px; overflow-x: auto; }
        
        /* --- Loading Spinner --- */
        .loading { display: none; text-align: center; margin: 20px 0; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid var(--primary); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; display: inline-block; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        
        /* --- Audio Section --- */
        .audio-controls { display: flex; gap: 10px; margin-top: 20px; justify-content: center; }
        .audio-controls button { padding: 10px 20px; }
    </style>
</head>
<body>

<header>
    <div class="logo">🧠 Edu Orbit</div>
    <p>Master Machine Learning with AI-powered explanations, code, and visuals.</p>
    <nav>
        <button onclick="showView('home')">Home</button>
        <button onclick="showView('text-view')">Text</button>
        <button onclick="showView('code-view')">Code</button>
        <button onclick="showView('visual-view')">Visuals</button>
        <button onclick="showView('audio-view')">Audio</button>
    </nav>
</header>

<div class="container">

    <div id="home" class="view-section active">
        <div class="welcome-section">
            <h1>Welcome to LearnSphere</h1>
            <p>Embark on your machine learning journey with AI-powered explanations, code generation, and interactive visuals designed to make learning engaging and effective.</p>
            <button class="btn-main" onclick="showView('text-view')">Start Learning</button>
        </div>
        <h2 style="text-align: center; margin: 40px 0 20px 0; color: var(--primary);">Learning Mode</h2>
        <div class="grid">
            <div class="card">
                <div class="icon-box">📖</div>
                <h3>Text Explanation</h3>
                <p>Get structured learning paths for any ML topic.</p>
                <button class="btn-main" onclick="showView('text-view')">Start Learning</button>
            </div>
            <div class="card">
                <div class="icon-box">💻</div>
                <h3>Code Examples</h3>
                <p>Explore interactive code examples for ML algorithms.</p>
                <button class="btn-main" onclick="showView('code-view')">Generate Code</button>
            </div>
            <div class="card">
                <div class="icon-box">🎵</div>
                <h3>Audio Lessons</h3>
                <p>Access audio lessons for immersive learning.</p>
                <button class="btn-main" onclick="showView('audio-view')">Generate Audio</button>
            </div>
            <div class="card">
                <div class="icon-box">🖼️</div>
                <h3>Visual Diagrams</h3>
                <p>Visualize complex architectures and flows.</p>
                <button class="btn-main" onclick="showView('visual-view')">Visualize Now</button>
            </div>
        </div>
    </div>

    <div id="text-view" class="view-section">
        <div class="input-group">
            <h2>Text Explanation</h2>
            <label>What would you like to learn?</label>
            <input type="text" id="text-topic" placeholder="e.g. Neural Networks, Random Forest...">
            <label>Explanation Depth</label>
            <select id="text-depth">
                <option>Brief (1-2 paragraphs)</option>
                <option selected>Detailed (Comprehensive)</option>
            </select>
            <button class="btn-main" onclick="generateResult('text')">Generate Explanation</button>
        </div>
        <div id="text-result" class="result-area"></div>
    </div>

    <div id="code-view" class="view-section">
        <div class="input-group">
            <h2>Code Generation</h2>
            <label>Topic for Code</label>
            <input type="text" id="code-topic" placeholder="e.g. Linear Regression, CNN...">
            <label>Programming Language</label>
            <select>
                <option>Python (Scikit-Learn/PyTorch)</option>
                <option>C++</option>
            </select>
            <button class="btn-main" onclick="generateResult('code')">Generate Code</button>
        </div>
        <div id="code-result" class="result-area">
            <h3>Generated Python Code</h3>
            <pre id="code-display"></pre>
        </div>
    </div>

    <div id="visual-view" class="view-section">
        <div class="input-group">
            <h2>Image Visualization</h2>
            <label>What would you like to visualize?</label>
            <input type="text" placeholder="e.g. Decision Tree structure...">
            <button class="btn-main" onclick="generateResult('visual')">Generate Visual</button>
        </div>
        <div id="visual-result" class="result-area" style="text-align: center;">
            <h3>AI Generated Diagram</h3>
            <div style="width: 100%; height: 200px; background: #eee; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <p>[Image Result Displayed Here]</p>
            </div>
        </div>
    </div>

    <div id="audio-view" class="view-section">
        <div class="input-group">
            <h2>Audio Lessons</h2>
            <label>Enter a Machine Learning topic</label>
            <input type="text" id="audio-topic" placeholder="e.g. Neural Networks, Supervised Learning...">
            <button class="btn-main" onclick="generateAudioLesson()">Generate Audio Lesson</button>
            <div class="loading" id="audio-loading">
                <div class="spinner"></div>
                <p>Generating audio lesson...</p>
            </div>
        </div>
        <div id="audio-result" class="result-area">
            <div id="audio-text"></div>
            <audio id="audio-player" controls style="width: 100%; margin: 20px 0;"></audio>
            <div class="audio-controls">
                <button class="btn-main" id="download-btn" onclick="downloadAudio()" style="display: none;">Download Audio</button>
            </div>
        </div>
    </div>

</div>

<script>
    // Logic to switch between "Pages" without reloading
    function showView(viewId) {
        // Hide all sections
        const sections = document.querySelectorAll('.view-section');
        sections.forEach(s => s.classList.remove('active'));
        
        // Show selected section
        document.getElementById(viewId).classList.add('active');
        
        // Scroll to top
        window.scrollTo(0, 0);
    }

    // Simulated AI Content Generation
    function generateResult(type) {
        if(type === 'text') {
            const topic = document.getElementById('text-topic').value || "Machine Learning";
            const res = document.getElementById('text-result');
            res.style.display = "block";
            res.innerHTML = `
                <h3>Learning: ${topic}</h3>
                <p><strong>Summary:</strong> ${topic} is a fundamental concept in machine learning that involves [brief description]. It forms the basis for many advanced algorithms and applications in data science.</p>
                
                <strong>Key Points:</strong>
                <ul>
                    <li><strong>Definition:</strong> ${topic} refers to [detailed definition]</li>
                    <li><strong>Importance:</strong> Understanding ${topic} is crucial for [why it's important]</li>
                    <li><strong>Components:</strong> Key elements include [main components]</li>
                    <li><strong>Advantages:</strong> Benefits include [pros]</li>
                </ul>
                
                <strong>Real World Applications:</strong>
                <ul>
                    <li><strong>Healthcare:</strong> Used in medical diagnosis and patient monitoring systems</li>
                    <li><strong>Finance:</strong> Applied in fraud detection and algorithmic trading</li>
                    <li><strong>Retail:</strong> Powers recommendation systems and customer behavior analysis</li>
                    <li><strong>Autonomous Vehicles:</strong> Essential for computer vision and decision-making</li>
                </ul>
                
                <p><em>Note: This is a simulated response. In a real application, this would be generated by an AI model like Gemini.</em></p>
            `;
        } 
        
        if(type === 'code') {
            const res = document.getElementById('code-result');
            const display = document.getElementById('code-display');
            res.style.display = "block";
            display.innerText = "import numpy as np\\nfrom sklearn.linear_model import LinearRegression\\n\\n# Model initialization\\nmodel = LinearRegression()\\nprint('Model ready for data!')";
        }

        if(type === 'visual') {
            document.getElementById('visual-result').style.display = "block";
        }
    }

    // Generate Audio Lesson
    async function generateAudioLesson() {
        const topic = document.getElementById('audio-topic').value || "Machine Learning";
        const loading = document.getElementById('audio-loading');
        const result = document.getElementById('audio-result');
        const audioPlayer = document.getElementById('audio-player');
        const downloadBtn = document.getElementById('download-btn');
        const audioText = document.getElementById('audio-text');

        // Show loading
        loading.style.display = "block";
        result.style.display = "none";

        try {
            const response = await fetch('/generate_audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topic: topic }),
            });

            if (!response.ok) {
                throw new Error('Failed to generate audio');
            }

            const data = await response.json();
            
            // Display text
            audioText.innerHTML = `<h3>Audio Lesson: ${topic}</h3><p>${data.text}</p>`;
            
            // Set audio source
            audioPlayer.src = data.audio_url;
            
            // Show download button
            downloadBtn.style.display = "inline-block";
            
            // Hide loading, show result
            loading.style.display = "none";
            result.style.display = "block";
            
        } catch (error) {
            console.error('Error:', error);
            loading.style.display = "none";
            alert('Error generating audio lesson. Please try again.');
        }
    }

    // Download Audio
    function downloadAudio() {
        const audioPlayer = document.getElementById('audio-player');
        if (audioPlayer.src) {
            const a = document.createElement('a');
            a.href = audioPlayer.src;
            a.download = 'audio_lesson.mp3';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }

    // Load audio file into player (for upload, if needed)
    function loadAudio() {
        const fileInput = document.getElementById('audio-file');
        const audioPlayer = document.getElementById('audio-player');
        
        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];
            const url = URL.createObjectURL(file);
            audioPlayer.src = url;
        }
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.get_json()
    topic = data.get('topic', 'Machine Learning')
    
    # Generate text explanation
    text = f"""
    Welcome to your audio lesson on {topic}.
    
    Summary: {topic} is a fundamental concept in machine learning that involves understanding patterns in data. It forms the basis for many advanced algorithms and applications in data science.
    
    Key Points:
    - Definition: {topic} refers to the process of teaching computers to learn from data without being explicitly programmed.
    - Importance: Understanding {topic} is crucial for building intelligent systems that can make predictions and decisions.
    - Components: Key elements include data, algorithms, and computational power.
    - Advantages: Benefits include automation, accuracy, and the ability to handle complex tasks.
    
    Real World Applications:
    - Healthcare: Used in medical diagnosis and patient monitoring systems.
    - Finance: Applied in fraud detection and algorithmic trading.
    - Retail: Powers recommendation systems and customer behavior analysis.
    - Autonomous Vehicles: Essential for computer vision and decision-making.
    
    Thank you for listening to this audio lesson on {topic}.
    """
    
    # Generate audio using gTTS
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save to bytes
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    # For simplicity, save to file and return URL
    filename = f"audio_{topic.replace(' ', '_')}.mp3"
    filepath = os.path.join('static', filename)
    os.makedirs('static', exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(audio_buffer.getvalue())
    
    audio_url = f"/static/{filename}"
    
    return jsonify({
        'text': text.replace('\n', '<br>'),
        'audio_url': audio_url
    })

if __name__ == '__main__':
    app.run(debug=True)