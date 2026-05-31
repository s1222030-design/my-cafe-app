import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfbfa; }
    :root { --primary-color: #2A5290 !important; }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }
    .stSlider > div > div > div > div { background-color: #2A5290 !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    div[data-baseweb="progress-bar"] > div { background-color: #2A5290 !important; }
    .cover-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .cover-image {
        width: 100%;
        max-width: 700px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.3rem !important;
        padding: 12px 60px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(42, 82, 144, 0.25) !important;
        transition: all 0.3s ease !important;
        display: block !important;
        margin: 0 auto !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(42, 82, 144, 0.4) !important;
        color: #ffffff !important;
    }
    .game-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #eedece;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if not st.session_state.game_started:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="cover-container"><img class="cover-image" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200"><h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1><p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？</p></div>', unsafe_allow_html=True)
    
    if st.button("點擊開始遊戲", key="start_game_trigger"):
        st.session_state.game_started = True
        st.rerun()
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load("cafe_model.pkl")

try:
    saved_data = load_model()
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]
except Exception as e:
    st.error("讀取模型失敗，請確認 cafe_model.pkl 是否與 app.py 放一起。")
    st.stop()

st.markdown('<div style="padding: 10px 0; margin-bottom: 20px;"><h2 style="color: #2A5290; font-weight: 800;">AI 咖啡廳策略模擬戰場</h2><p style="color: #718096; margin-top: -5px;">配置專屬指標，隨機森林模型將即時為妳的商業決策打分數！</p></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["關卡一：自由經營模擬市集", "關卡二：17點策略極限挑戰賽"])

def get_prediction(city, wifi, quiet, tasty, cheap, music, socket_val, limit_val):
    city_geo_centers = {
        "changhua": {"lat": 24.078, "lng": 120.551},
        "taichung": {"lat": 24.151, "lng": 120.664},
        "kaohsiung": {"lat": 22.614, "lng": 120.306},
    }
    lat = city_geo_centers[city]["lat"]
    lng = city_geo_centers
