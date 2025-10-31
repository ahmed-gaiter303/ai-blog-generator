import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Blog Post Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: white;
    }
    .stTextArea > div > div > textarea {
        background-color: #262730;
        color: white;
    }
    .generated-content {
        background-color: #1e4d2b;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Settings
with st.sidebar:
    st.title("⚙️ Blog Settings")
    st.markdown("---")
    
    # Blog style
    blog_style = st.selectbox(
        "Blog Style",
        ["Casual & Engaging", "Professional & Formal", "News Style", "Marketing & Persuasive", "Educational"]
    )
    
    # Word count
    word_count = st.slider("Target Word Count", 300, 3000, 800, 100)
    
    # Tone
    tone = st.select_slider(
        "Tone",
        ["Very Serious", "Serious", "Neutral", "Friendly", "Very Casual"],
        value="Neutral"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Generation Stats")
    if 'blog_count' not in st.session_state:
        st.session_state.blog_count = 0
    st.metric("Blogs Generated", st.session_state.blog_count)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("""
    **Write Good Topics:**
    - "How to start a blog in 2025"
    - "10 AI tools for marketers"
    - "Complete guide to SEO"
    
    The better your topic, the better the blog!
    """)

# Function to generate blog
def generate_blog(topic, keywords, style, word_count, tone):
    try:
        # Construct the prompt
        prompt = f"""Write a blog post with these requirements:

Topic: {topic}
Keywords to include: {keywords}
Style: {blog_style}
Target word count: approximately {word_count} words
Tone: {tone}

Requirements:
1. Start with an engaging introduction
2. Use clear headings (H2, H3)
3. Include the keywords naturally
4. Add actionable tips or insights
5. End with a strong conclusion
6. Make it SEO-friendly
7. Use short paragraphs (2-3 sentences max)
8. Include a call-to-action at the end

Write the blog post now. Make it valuable, readable, and shareable."""

        llm = GoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        
        blog_content = llm.invoke(prompt)
        return blog_content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Function to generate title and meta description
def generate_seo(topic):
    try:
        prompt = f"""Generate SEO content for this topic: "{topic}"

Provide:
1. 3 compelling blog titles (each 50-60 characters)
2. 3 meta descriptions (each 150-160 characters)
3. 5 relevant keywords/phrases

Format your response clearly with sections."""

        llm = GoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.8,
            google_api_key=os.environ.get("GOOGLE_API_KEY")
        )
        
        seo_content = llm.invoke(prompt)
        return seo_content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Main content
st.title("✍️ AI Blog Post Generator")
st.markdown("**Generate high-quality blog posts in seconds**")
st.markdown("---")

# Check API key
if not os.environ.get("GOOGLE_API_KEY"):
    st.error("⚠️ GOOGLE_API_KEY not found! Add it to your Secrets.")
    st.stop()

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input(
        "📝 Blog Topic",
        placeholder="e.g., How to start a successful blog in 2025",
        label_visibility="collapsed"
    )

with col2:
    st.write("")
    st.write("")
    generate_button = st.button("🚀 Generate Blog", type="primary", use_container_width=True)

# Keywords input
keywords = st.text_input(
    "🔑 Keywords (comma-separated)",
    placeholder="e.g., blog, blogging, content creation, SEO",
    label_visibility="collapsed"
)

st.markdown("---")

# Generate blog
if generate_button:
    if not topic:
        st.warning("⚠️ Please enter a blog topic!")
    else:
        # Generate SEO first
        st.subheader("📊 SEO Suggestions")
        with st.spinner("Generating SEO suggestions..."):
            seo_result = generate_seo(topic)
        st.markdown(seo_result)
        
        st.markdown("---")
        
        # Generate blog
        st.subheader("📄 Your Blog Post")
        with st.spinner("Generating your blog post... (this might take 30-45 seconds)"):
            blog_result = generate_blog(topic, keywords, blog_style, word_count, tone)
        
        # Display blog
        st.markdown(blog_result)
        
        # Actions
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download as Text",
                data=blog_result,
                file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📥 Download as Markdown",
                data=f"# {topic}\n\n{blog_result}",
                file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with col3:
            if st.button("📋 Copy to Clipboard"):
                st.success("✅ Copied! (Paste it anywhere)")
        
        st.session_state.blog_count += 1

# Info section
st.markdown("---")
with st.expander("ℹ️ About This Tool"):
    st.markdown("""
    ### AI Blog Post Generator
    
    This tool helps you create high-quality blog posts in seconds using Google's Gemini AI.
    
    **Features:**
    - 5 different writing styles
    - SEO optimization
    - Customizable tone and length
    - Download options (TXT, Markdown)
    - Keyword suggestions
    - Meta descriptions
    
    **How it works:**
    1. Enter your blog topic
    2. Add relevant keywords
    3. Choose your style and tone
    4. Click Generate
    5. Download and use!
    
    **Tips for best results:**
    - Be specific with your topic
    - Include relevant keywords
    - Match the style to your audience
    - Edit for your brand voice
    
    Made with ❤️ by Ahmed Gaiter
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("💻 Built with LangChain & Gemini")
with col2:
    st.caption(f"📊 Blogs generated: {st.session_state.blog_count}")
with col3:
    st.caption("🤖 Powered by AI")
