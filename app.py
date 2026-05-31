import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 注入自訂 CSS：全面抹除紅色 (#FF4B4B) 並強制套用 #2A5290
st.markdown("""
    <style>
    .main { background-color: #fcfbfa; }
    
    /* 1. 強制變更核心主題變數 */
    :root {
        --primary-color: #2A5290 !important;
    }
    
    /* 2. 移除所有 Tabs 選取時的內建底線紅色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
    }
    
    /* 3. 拉桿軌道顏色 */
    .stSlider > div > div > div > div { background-color: #2A5290 !important; }
    
    /* 4. 拉桿滑塊圓鈕外觀 */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* 5. 徹底消滅拉桿上方的紅色數字提示標籤 */
    div[data-testid="stSliderTickBar"] ~ div, 
    .stSlider div[style*="color: rgb(255, 75, 75)"],
    .stSlider div {
        color: #2A5290 !important;
    }
    
    /* 6. 徹底消滅 Radio 單選鈕被選中時的紅色外圈與內部紅點 */
    div[data-testid="stRadio"] [data-checked="true"] > div {
        border-color: #2A5290 !important;
        background-color: #2A5290 !important;
    }
    div[data-testid="stRadio"] [data-checked="true"] > div_ {
        background-color: #F7F5F2 !important;
    }
    
    /* 7. 進度條顏色變更 */
    div[data-baseweb="progress-bar"] > div { background-color: #2A5290 !important; }
    
    /* 8. 封面圖片與排版 */
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
    
    /* 9. 按鈕高級美化（移除所有紅色邊框影響） */
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
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(42, 82, 144, 0.35) !important;
        color: #ffffff !important;
    }
    .stButton > button:focus {
        border-color: #2A5290 !important;
        box-shadow: 0 0 0 0.2rem rgba(42, 82, 144, 0.2) !important;
    }
    
    /* 10. 遊戲卡片框 */
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
                歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客慢配方嗎？
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 欄位分配：[左邊空距, 中間按鈕寬度, 右邊空距]，配合容器填滿來確保100%絕對置中！
    c1, c2, c3 = st.columns([1.2, 1.1, 1.2])
    with c2:
        if st.button("點擊開始遊戲", key="start_game_trigger", use_container_width=True):
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

tab1, tab2 = st.tabs(["關卡一：自由經營模擬市集", "關卡二：17點策略極限挑戰賽"])

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
# Tab 1：自由經營模擬
# ---------------------------------------------------------------------
with tab1:
    st.markdown("<div class='game-card'>", unsafe_allow_html=True)
    st.markdown("### 自由調配基地")
    
    g1_city = st.selectbox("選擇欲進駐的城市商圈", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈")
    
    st.markdown("#### 店內硬體與品質設定")
    col1, col2 = st.columns(2)
    with col1:
        g1_wifi = st.slider("WiFi 穩定度", 1, 5, 3, key="g1_slider_w")
        g1_quiet = st.slider("環境安靜度", 1, 5, 3, key="g1_slider_q")
        g1_tasty = st.slider("產品美味度", 1, 5, 3, key="g1_slider_t")
    with col2:
        g1_cheap = st.slider("物美價廉 CP值", 1, 5, 3, key="g1_slider_c")
        g1_music = st.slider("空間音樂舒適度", 1, 5, 3, key="g1_slider_m")
    
    st.markdown("#### 顧客福利開放")
    col3, col4 = st.columns(2)
    with col3:
        g1_socket = st.radio("每個座位提供免費插座", ["不提供", "提供"], index=1, horizontal=True)
    with col4:
        g1_limit = st.radio("客滿時的用餐時間限制", ["不限時", "限時"], index=0, horizontal=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    c_btn1, c_btn2, c_btn3 = st.columns(
