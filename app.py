import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 終極 CSS 注入：鎖定海軍藍與奶油白背景，並完全移除 tab 預設的無意義白框
st.markdown("""
    <style>
    /* 全域背景色微調為指定的奶油白 */
    .stApp, .main { 
        background-color: #F7F5F2 !important; 
    }
    
    /* 移除 Streamlit tabs 預設產生的白色大方塊容器背景與外框 */
    div[data-baseweb="tab-panel"] {
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stTab"] {
        background-color: transparent !important;
    }
    
    /* 頁籤選取狀態顏色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }

    /* 封面排版容器 */
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
    
    /* 高級海軍藍按鈕本體美化 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 12px 60px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(42, 82, 144, 0.25) !important;
        transition: all 0.3s ease !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(42, 82, 144, 0.4) !important;
        color: #ffffff !important;
    }
    
    /* 確保按鈕內部的 Streamlit 文字元件也強制繼承 #F7F5F2 */
    .stButton > button p {
        color: #F7F5F2 !important;
    }
    .stButton > button:hover p {
        color: #ffffff !important;
    }
    
    /* 高質感卡片框（乾淨底色，融入奶油白背景） */
    .game-card {
        background-color: transparent;
        padding: 10px 0px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化控制封面的 Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# =====================================================================
# 🎬 核心畫面邏輯分配 (由 if-else 確保按鈕點擊後絕對正常載入)
# =====================================================================
if not st.session_state.game_started:
    # 顯示封面頁面
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="cover-container">
            <img class="cover-image" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 藉由標準的 Streamlit columns 將按鈕置中
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button("點擊開始遊戲", key="start_game_trigger", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()

else:
    # =====================================================================
    # 🕹️ 核心遊戲主程式 (點擊開始後 100% 渲染載入)
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

    tab1, tab2 = st.tabs(["關卡一：自由經營模擬市集", "關卡二：17點策略極限挑戰賽"])

    def get_prediction(city, wifi, quiet, tasty, cheap, music, socket_val, limit_val):
        city_geo_centers = {
            "changhua": {"lat": 24.078, "lng": 120.551},
            "taichung": {"lat": 24.151, "lng": 120.664},
            "kaohsiung": {"lat": 22.614, "lng": 120.306}
        }
        lat = city_geo_centers[city]["lat"]
        lng = city_geo_centers[city]["lng"]
        
        input_dict = {
            "wifi": wifi, "quiet": quiet, "tasty": tasty, "cheap": cheap, "music": music,
            "latitude": lat, "longitude": lng
        }
        
        for col in feature_cols:
            if col not in input_dict:
                if col == f"city_{city}": input_dict[col] = 1
                elif col == "limited_time_no": input_dict[col] = 1 - limit_val
                elif col == "limited_time_yes": input_dict[col] = limit_val
                elif col == "socket_yes": input_dict[col] = socket_val
                else: input_dict[col] = 0
                
        input_df = pd.DataFrame([input_dict])
        missing_cols = set(feature_cols) - set(input_df.columns)
        for c in missing_cols: input_df[c] = 0
        input_df = input_df[feature_cols]
