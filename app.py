import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 終極 CSS 注入：強制鎖定海軍藍 (#2A5290)，消滅全部紅色，強制按鈕置中
st.markdown("""
    <style>
    /* 全域背景色微調 */
    .main { background-color: #fcfbfa; }
    
    /* 核心變數強力壓制 */
    :root {
        --primary-color: #2A5290 !important;
    }
    
    /* 徹底染藍：拉桿上方的紅字數字小標籤 */
    div[data-testid="stSliderTickBar"] ~ div,
    div[class*="st-emotion-cache"] span,
    div[class*="st-emotion-cache"] div,
    .stSlider div,
    .stSlider p,
    span[data-testid="stWidgetLabel"] p {
        color: #2A5290 !important;
    }
    
    /* 強制將 Slider 最左側累積的紅色進度條與軌道換成海軍藍 */
    div[data-testid="stSlider"] div[role="presentation"] div {
        background-color: #2A5290 !important;
    }
    
    /* 修改拉桿滑動圓鈕 */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
    }
    
    /* 徹底染藍：Radio 單選鈕外圈與被選中時的內部「核心紅點」 */
    div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="true"] > div {
        border-color: #2A5290 !important;
        background-color: #2A5290 !important;
    }
    
    /* 進度條、網頁分頁標籤（Tabs）的所有紅色全面攔截 */
    div[data-baseweb="progress-bar"] > div { background-color: #2A5290 !important; }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }

    /* 封面排版與 100% 絕對置中容器 */
    .cover-box {
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .cover-img {
        width: 100%;
        max-width: 700px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    
    /* 強制按鈕居中 */
    div.stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        width: 100%;
        text-align: center;
    }
    
    /* 高級海軍藍按鈕本體美化 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 12px 60px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(42, 82, 144, 0.2) !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
        width: auto !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(42, 82, 144, 0.35) !important;
        color: #ffffff !important;
    }
    
    /* 高質感遊戲卡片框 */
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

# 3. 初始化控制封面的 Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# =====================================================================
# 🎬 關卡封面頁面 (Cover Page)
# =====================================================================
if not st.session_state.game_started:
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="cover-box">
            <img class="cover-img" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("點擊開始遊戲", key="start_game_trigger"):
        st.session_state.game_started = True
        st.rerun()
            
    st.stop()

# =====================================================================
# 🕹️ 核心遊戲主程式 (點擊開始後載入)
# =====================================================================
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

st.markdown("""
    <div style="padding: 10px 0; margin-bottom: 20px;">
        <h2 style="color: #2A5290; font-weight: 800;">AI 咖啡廳策略模擬戰場</h2>
        <p style="color: #718096; margin-top: -5px;">配置專屬指標，隨機森林模型將即時為妳的商業決策打分數！</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs
