import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI 咖啡廳改造大亨", page_icon="☕", layout="wide")

# 2. 注入自訂 CSS：全面改為 #2A5290 與 #F7F5F2，消滅所有預設紅 (#FF4B4B)
st.markdown("""
    <style>
    /* 全域背景色微調 */
    .main { background-color: #fcfbfa; }
    
    /* 強制將 Streamlit 核心變數改為海軍藍，徹底消滅 #FF4B4B 紅色 */
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
    
    /* 封面專用：讓圖片與按鈕完全置中的容器 */
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
    
    /* 所有的按鈕外觀奢華升級 */
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
        margin: 0 auto !important; /* 確保按鈕水平置中 */
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(42, 82, 144, 0.4) !important;
        color: #ffffff !important;
    }
    
    /* 高質感遊戲卡片區塊 */
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
# 🎬 關卡封面頁面 (Cover Page) - 採用完全安全的 HTML 置中排版
# =====================================================================
if not st.session_state.game_started:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 透過網頁容器，直接強迫所有封面素材與按鈕全部絕對置中
    st.markdown("""
        <div class="cover-container">
            <img class="cover-image" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">☕ AI 咖啡廳改造大亨</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 開始遊戲按鈕 (CSS 已將 .stButton 設定為 margin: 0 auto 自動置中)
    if st.button("🎮 點擊開始遊戲 🚀", key="start_game_trigger"):
        st.session_state.game_started = True
        st.rerun()
        
    st.stop() # 阻斷後續畫面，直到玩家點擊按鈕進入

# =====================================================================
# 🕹️ 核心遊戲主程式 (當點擊開始後才會載入)
# =====================================================================
@st.cache_resource
def load_model():
    return joblib.load("cafe_model.pkl")

try:
    saved_data = load_model()
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]
except Exception as e:
    st.error("❌ 讀取模型失敗，請確認 cafe_model.pkl 是否與 app.py 放一起。")
    st.stop()

# 遊戲主頁大標題
st.markdown("""
    <div style="padding: 10px 0; margin-bottom: 20px;">
        <h2 style="color: #2A5290; font-weight: 800;">🏆 AI 咖啡廳策略模擬戰場</h2>
        <p style="color: #718096; margin-top: -5px;">配置專屬指標，隨機森林模型將即時為妳的商業決策打分數！</p>
    </div>
""", unsafe_allow_html=True)

# 建立兩個遊戲的頁籤 (底色與字體已被 CSS 修正為海軍藍)
tab1, tab2 = st.tabs(["🎮 關卡一：自由經營模擬市集", "🔥 關卡二：17點策略極限挑戰賽"])

# 預測推理的核心函式
def get_prediction(city, wifi, quiet, tasty, cheap, music, socket_val, limit_val):
    city_geo_centers = {
        "changhua": {"lat": 24.078, "lng": 120.551},
        "taichung": {"lat": 24.151, "lng": 120.664},
        "kaohsiung": {"lat": 22.614, "lng": 120.306},
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
    
    prob = model.predict(input_df)[0]
    return max(0.0, min(1.0, prob))

# ---------------------------------------------------------------------
# 🎮 Tab 1：自由經營模擬
# ---------------------------------------------------------------------
with tab1:
    st.markdown("<div class='game-card'>", unsafe_allow_html=True)
    st.markdown("### 🗺️ 自由調配基地")
    
    g1_city = st.selectbox("📍 選擇欲進駐的城市商圈", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈")
    
    st.markdown("#### 🔹 店內硬體與品質設定")
    col1, col2 = st.columns(2)
    with col1:
        g1_wifi = st.slider("📶 高速 WiFi 穩定度", 1, 5, 3, key="g1_slider_w")
        g1_quiet = st.slider("🤫 環境安靜安穩度", 1, 5, 3, key="g1_slider_q")
        g1_tasty = st.slider("☕ 咖啡甜點美味度", 1, 5, 3, key="g1_slider_t")
    with col2:
        g1_cheap = st.slider("💰 物美價廉 CP值", 1, 5, 3, key="g1_slider_c")
        g1_music = st.slider("🎵 空間音樂舒適度", 1, 5, 3, key="g1_slider_m")
    
    st.markdown("#### 🔹 顧客福利開放")
    col3, col4 = st.columns(2)
    with col3:
        g1_socket = st.radio("🔌 每個座位提供免費插座", ["不提供", "提供"], index=1, horizontal=True)
    with col4:
        g1_limit = st.radio("⏳ 客滿時的用餐時間限制", ["不限時", "限時"], index=0, horizontal=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 啟動 AI 大數據經營模擬預測", key="g1_submit_btn"):
        s_val = 1 if g1_socket == "提供" else 0
        l_val = 1 if g1_limit == "限時" else 0
        prob = get_prediction(g1_city, g1_wifi, g1_quiet, g1_tasty, g1_cheap, g1_music, s_val, l_val)
        
        st.markdown("---")
        st.metric(label="📊 AI
