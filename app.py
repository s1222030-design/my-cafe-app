import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 注入自訂 CSS：精準套用 #2A5290 與 #F7F5F2，並強行消滅 Streamlit 的 #FF4B4B 紅色
st.markdown("""
    <style>
    /* 全域背景色微調 */
    .main { background-color: #fcfbfa; }
    
    /* 強制將 Streamlit 核心主題色全面改為海軍藍 */
    :root {
        --primary-color: #2A5290 !important;
    }
    
    /* 頁籤 (Tabs) 選取時的文字與底線顏色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }
    
    /* 修改拉桿軌道顏色 (#2A5290) */
    .stSlider > div > div > div > div {
        background-color: #2A5290 !important;
    }
    
    /* 修改拉桿滑動圓鈕顏色 (#F7F5F2) */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* 進度條顏色強制改為海軍藍 */
    div[data-baseweb="progress-bar"] > div {
        background-color: #2A5290 !important;
    }
    
    /* 封面專用：圖片與按鈕完全置中的版面配置 */
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
    
    /* 所有的按鈕外觀高級化，並強制水平置中 */
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
    
    /* 高質感卡片區塊 */
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
    
    # 完全安全的 HTML 排版
    st.markdown("""
        <div class="cover-container">
            <img class="cover-image" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 開始遊戲按鈕 (透過自訂 CSS 達成全置中)
    if st.button("點擊開始遊戲", key="start_game_trigger"):
        st.session_state.game_started = True
        st.rerun()
        
    st.stop() # 阻斷後續畫面，直到玩家點擊進入

# =====================================================================
# 🕹️ 核心遊戲主程式 (點擊開始後載入)
# =====================================================================
@st.cache_resource
def load_model():
