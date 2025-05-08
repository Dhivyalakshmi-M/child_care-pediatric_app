# Required installations (if not already installed):
# pip install streamlit textblob plotly streamlit-lottie

import streamlit as st
from streamlit_lottie import st_lottie
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import requests
import os
import plotly.express as px

def show():
    
    # Place back button in the first column (left corner)
    st.markdown("""
        <style>
        .block-container {
           
            background: linear-gradient(to right, #f6d365, #fda085);

        }</style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "dashboard"
    # Load Lottie animations
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    happy_anim = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_4kx2q32n.json")
    sad_anim = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
    neutral_anim = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_3u5u5p1k.json")

    # Page setup
    #st.set_page_config(page_title="Child Mood & Behavior Tracker", page_icon="🧠", layout="centered")
    st.markdown("""
        <h1 style='text-align: center; color: black;'>🧠 Child Mood & Behavior Tracker</h1>
        <p style='text-align: center; color: #333;'>Track and analyze your child's emotional health with smart AI insights.</p>
        <hr style='border: 2px solid #6C63FF;'>
    """, unsafe_allow_html=True)

    # Mood input
    st.subheader("😊 How do you feel right now?")
    mood_emoji = st.radio("Choose your mood emoji:", ["😀 Happy", "😐 Neutral", "😢 Sad", "😡 Angry"])

    # Journal input
    st.subheader("📔 Daily Journal")
    journal = st.text_area("📝 Write about your day:")

    # Behavior input
    st.markdown("### 📊 Daily Behavior Log")
    col1, col2, col3 = st.columns(3)
    with col1:
        sleep_hours = st.slider("😴 Sleep (hrs)", 0, 12, 8)
    with col2:
        screen_time = st.slider("📱 Screen Time (hrs)", 0, 10, 2)
    with col3:
        appetite = st.selectbox("🍽️ Appetite", ["Good", "Average", "Low"])

    # Mood analyzer
    @st.cache_data

    def analyze_mood(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.2:
            return "Happy", polarity
        elif polarity < -0.2:
            return "Sad", polarity
        else:
            return "Neutral", polarity

    def get_suggestions(mood):
        return {
            "Happy": ["🎉 Keep smiling!", "👯‍♀️ Play with friends!", "📸 Take a photo of your smile!"],
            "Sad": ["🎨 Draw or paint your feelings.", "🧘 Try breathing exercises.", "📞 Talk to someone you trust."],
            "Neutral": ["🎵 Listen to calm music.", "🚶 Go for a walk.", "📖 Read a fun book."]
        }.get(mood, ["🤔 Try again later."])

    # Analysis button
    if st.button("🚀 Analyze Mood"):
        if journal.strip() == "":
            st.warning("✍️ Please write something in the journal.")
        else:
            mood, polarity = analyze_mood(journal)

            # Show animation
            st.markdown(f"### 🧠 Detected Mood: **{mood}** (Score: `{round(polarity, 2)}`)")
            if mood == "Happy":
                st_lottie(happy_anim, height=200)
            elif mood == "Sad":
                st_lottie(sad_anim, height=200)
            else:
                st_lottie(neutral_anim, height=200)

            st.subheader("🎯 What you can do:")
            for tip in get_suggestions(mood):
                st.markdown(f"- {tip}")

            # Save entry
            entry = {
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "Mood": [mood],
                "Emoji": [mood_emoji.split()[0]],
                "Polarity": [polarity],
                "Sleep": [sleep_hours],
                "Screen Time": [screen_time],
                "Appetite": [appetite],
                "Journal": [journal]
            }
            new_df = pd.DataFrame(entry)

            if os.path.exists("mood_data.csv"):
                new_df.to_csv("mood_data.csv", mode='a', header=False, index=False)
            else:
                new_df.to_csv("mood_data.csv", index=False)

            st.success("✅ Mood entry saved successfully!")

    # Mood history section
    st.markdown("---")
    st.markdown("## 📅 Mood History & Trends")

    if os.path.exists("mood_data.csv"):
        df = pd.read_csv("mood_data.csv")
        df['Date'] = pd.to_datetime(df['Date'])

        st.dataframe(df.tail(10)[["Date", "Emoji", "Mood", "Sleep", "Screen Time", "Appetite"]])

        # Chart for Polarity
        fig1 = px.line(df, x='Date', y='Polarity', title='🧠 Mood Polarity Over Time', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        # Chart for Sleep and Screen Time
        fig2 = px.bar(df, x='Date', y=['Sleep', 'Screen Time'], title='📊 Sleep vs Screen Time')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("📝 No mood data available yet. Start journaling to view trends!")

