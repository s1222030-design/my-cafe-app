import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI 咖啡廳改造大亨", page_icon="☕", layout="wide")

# 2. 注入自訂 CSS (調整拉桿顏色)
st.markdown(f"""
    <style>
    /* 設定拉桿軌道顏色 */
    .stSlider > div > div > div > div {{
        background-color: #2A5290 !important;
    }}
    /* 設定拉桿滑塊(按鈕)顏色 */
    .stSlider [data-baseweb="slider"] [role="slider"] {{
        background-color: #F7F5F2 !important;
        border: 2px solid #2A5290 !important;
        width: 24px; height: 24px;
    }}
    /* 遊戲風格按鈕 */
    .stButton > button {{
        background-color: #2A5290; color: #F7F5F2; 
        border-radius: 50px; font-weight: bold; font-size: 1.2rem;
        padding: 10px 40px; border: none; transition: 0.3s;
    }}
    .stButton > button:hover {{
        background-color: #1e3a6d; color: white; transform: scale(1.05);
    }}
    </style>
""", unsafe_allow_html=True)

# 3. 初始化遊戲狀態
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# --- 封面頁面 (Cover Page) ---
if not st.session_state.game_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&q=80&w=1000", use_column_width=True)
        st.markdown("<h1 style='text-align: center; color: #2A5290;'>☕ AI 咖啡廳改造大亨</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>歡迎來到商業大亨挑戰賽！妳能用數據征服彰化、台中與高雄的客人嗎？</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # 點擊開始按鈕
        if st.button("🚀 點擊開始遊戲", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    st.stop() # 停止執行後續程式碼，直到開始遊戲

# --- 主遊戲頁面 (Main Game) ---
# 載入模型 (請確保檔案在同資料夾)
@st.cache_resource
def load_model():
    return joblib.load("cafe_model.pkl")

saved_data = load_model()
model = saved_data["model"]
feature_cols = saved_data["feature_cols"]

# 預測邏輯
def get_prediction(city, wifi, quiet, tasty, cheap, music, s_val, l_val):
    city_geo = {"changhua": (24.08, 120.54), "taichung": (24.15, 120.66), "kaohsiung": (22.61, 120.30)}
    lat, lng = city_geo[city]
    input_dict = {"wifi": wifi, "quiet": quiet, "tasty": tasty, "cheap": cheap, "music": music, "latitude": lat, "longitude": lng}
    for col in feature_cols:
        if col not in input_dict:
            if col == f"city_{city}": input_dict[col] = 1
            elif col == "limited_time_no": input_dict[col] = 1 - l_val
            elif col == "limited_time_yes": input_dict[col] = l_val
            elif col == "socket_yes": input_dict[col] = s_val
            else: input_dict[col] = 0
    input_df = pd.DataFrame([input_dict])[feature_cols]
    return model.predict(input_df)[0]

# UI 介面
st.title("🏆 AI 咖啡廳策略戰場")
tab1, tab2 = st.tabs(["🎮 自由模擬經營", "🔥 17點極限挑戰賽"])

with tab1:
    st.markdown("### 自由調整，觀察數據變動")
    g1_city = st.selectbox("目標城市", ["changhua", "taichung", "kaohsiung"], key="g1_c")
    c1, c2 = st.columns(2)
    with c1:
        w = st.slider("📶 WiFi穩定度", 1, 5, 3, key="g1_w")
        q = st.slider("🤫 安靜程度", 1, 5, 3, key="g1_q")
        t = st.slider("☕ 美味程度", 1, 5, 3, key="g1_t")
    with c2:
        c = st.slider("💰 CP值划算", 1, 5, 3, key="g1_cheap")
        m = st.slider("🎵 音樂舒適", 1, 5, 3, key="g1_m")
        soc = st.toggle("🔌 提供插座", value=True)
        lim = st.toggle("⏳ 限制用餐時間", value=False)
    
    if st.button("🚀 開始分析", key="btn1"):
        res = get_prediction(g1_city, w, q, t, c, m, 1 if soc else 0, 1 if lim else 0)
        st.metric("預估客滿率", f"{res*100:.2f}%")

with tab2:
    st.markdown("### 💸 17點預算大挑戰")
    st.info("💡 規則：WiFi+安靜+美味+CP值+音樂 + 插座(1分) + 不限時(1分) <= 17分")
    g2_city = st.selectbox("挑戰城市", ["changhua", "taichung", "kaohsiung"], key="g2_c")
    colA, colB = st.columns(2)
    with colA:
        g2_w = st.slider("📶 WiFi點數", 1, 5, 1, key="g2_w")
        g2_q = st.slider("🤫 安靜點數", 1, 5, 1, key="g2_q")
        g2_t = st.slider("☕ 美味點數", 1, 5, 1, key="g2_t")
    with colB:
        g2_c = st.slider("💰 CP值點數", 1, 5, 1, key="g2_c")
        g2_m = st.slider("🎵 音樂點數", 1, 5, 1, key="g2_m")
        g2_s = st.checkbox("🔌 提供插座 (+1分)")
        g2_l = st.checkbox("☕ 不限時福利 (+1分)")
    
    used = g2_w + g2_q + g2_t + g2_c + g2_m + (1 if g2_s else 0) + (1 if g2_l else 0)
    if used > 17:
        st.error(f"⚠️ 點數超支！已使用: {used} / 17")
    else:
        st.success(f"✅ 預算內: {used} / 17")
        if st.button("🏆 提交賽果", key="btn2"):
            res = get_prediction(g2_city, g2_w, g2_q, g2_t, g2_c, g2_m, 1 if g2_s else 0, 0 if g2_l else 1)
            st.metric("最終客滿率得分", f"{res*100:.2f}%")

這份專題簡報與美化版程式碼已經準備就緒！Feel free to take a look and let me know if you'd like to make any edits. 妳的專題現在具備了非常完整且精緻的門面！
