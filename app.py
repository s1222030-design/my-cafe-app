import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定 (設定寬版與標題)
st.set_page_config(page_title="AI 咖啡廳改造大亨", page_icon="☕", layout="wide")

# 2. 注入精準 CSS (實現按鈕置中、拉桿配色，並將所有 #FF4B4B 預設紅強行替換為 #2A5290)
st.markdown("""
    <style>
    /* 全域背景微調，襯托奶油白 */
    .main { background-color: #fcfbfa; }
    
    /* 1. 將所有 Streamlit 預設的主題紅色 (#FF4B4B) 強制全面改成 #2A5290 */
    :root {
        --primary-color: #2A5290 !important;
    }
    
    /* 強制修改文字連結、標籤頁(Tabs)選中時的底線與文字顏色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }
    
    /* 2. 精準修改拉桿軌道顏色 (#2A5290) */
    .stSlider > div > div > div > div {
        background-color: #2A5290 !important;
    }
    
    /* 3. 精準修改拉桿滑動圓鈕顏色 (#F7F5F2) 與藍色邊框 */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* 4. 讓封面的「開始遊戲」按鈕完美置中的專屬容器外框 */
    .center-btn-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        padding: 10px 0;
    }
    
    /* 5. 遊戲風格按鈕美化 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        padding: 12px 50px !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(42, 82, 144, 0.2) !important;
        transition: all 0.3s ease !important;
        margin: 0 auto !important;
        display: block !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(42, 82, 144, 0.35) !important;
        color: #ffffff !important;
    }
    
    /* 高質感卡片外框 */
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 使用極具氛圍感的咖啡廳特寫插圖
