import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 注入自訂 CSS：精準套用顏色，並修正 Streamlit 核心元件外觀
st.markdown("""
    <style>
    .main { background-color: #fcfbfa; }
    :root { --primary-color: #2A5290 !important; }
    
    /* 頁籤選取狀態顏色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }
    
    /* 修改拉桿軌道顏色 */
    .stSlider > div > div > div > div { background-color: #2A5290 !important; }
    
    /* 修改拉桿滑動圓鈕外觀 */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* 進度條顏色變更 */
    div[data-baseweb="progress-bar"] > div { background-color: #2A5290 !important; }
    
    /* 封面圖片與排版外觀 */
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
    
    /* 所有按鈕美化與圓角設計 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 10px 40px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(42, 82, 144, 0.2) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
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
    
    # 標準包覆與閉合的 HTML 封面排版
    st.markdown("""
        <div class="cover-box">
            <img class="cover-img" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 使用 Streamlit 官方佈局欄位，將按鈕 100% 鎖定在畫面正中央
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        if st.button("點擊開始遊戲", key="start_game_trigger"):
            st.session_state.game_started = True
            st.rerun()
            
    st.stop() # 阻斷後續畫面，直到玩家點擊進入

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

# 標題區塊（確實閉合 </div>）
st.markdown("""
    <div style="padding: 10px 0; margin-bottom: 20px;">
        <h2 style="color: #2A5290; font-weight: 800;">AI 咖啡廳策略模擬戰場</h2>
        <p style="color: #718096; margin-top: -5px;">配置專屬指標，隨機森林模型將即時為妳的商業決策打分數！</p>
    </div>
""", unsafe_allow_html=True)

# 建立兩個遊戲的頁籤（不再被 HTML 錯誤吞掉）
tab1, tab2 = st.tabs(["關卡一：自由經營模擬市集", "關卡二：17點策略極限挑戰賽"])

# 預測推理的核心函式
def get_prediction(city, wifi, quiet, tasty, cheap, music, socket_val, limit_val):
    city
