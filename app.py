import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 終極 CSS 注入：鎖定海軍藍與奶油白背景，美化雙按鈕佈局
st.markdown("""
    <style>
    /* 全域背景色鎖定為奶油白 */
    .stApp, .main { 
        background-color: #F7F5F2 !important; 
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
    
    /* 高級海軍藍按鈕樣式 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%) !important;
        color: #ffffff !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 12px 20px !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(42, 82, 144, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(42, 82, 144, 0.35) !important;
        color: #ffffff !important;
    }
    .stButton > button p {
        color: #ffffff !important;
    }
    
    /* 返回按鈕專用樣式 (稍微小一點，區隔功能) */
    .back-btn button {
        background: #6b5b4b !important;
        font-size: 0.9rem !important;
        padding: 5px 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化導覽狀態
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None  # None=封面, basic=基礎, advanced=進階

# 4. 載入模型函式
@st.cache_resource
def load_model():
    try:
        return joblib.load("cafe_model.pkl")
    except:
        return None

# 預測邏輯
def get_prediction(city, wifi, quiet, tasty, cheap, music, socket_val, limit_val, feature_cols, model):
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
    for c in (set(feature_cols) - set(input_df.columns)): input_df[c] = 0
    input_df = input_df[feature_cols]
    prob = model.predict(input_df)[0]
    return max(0.0, min(1.0, prob))

# =====================================================================
# 🎬 畫面邏輯控制
# =====================================================================

# --- 頁面 A：封面與模式選擇 ---
if st.session_state.game_mode is None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="cover-container">
            <img class="cover-image" src="https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！請選擇您的挑戰模式：
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # 放置兩個並排的大按鈕
    _, col_left, col_right, _ = st.columns([1, 2, 2, 1])
    with col_left:
        if st.button("基礎模式：自由經營模擬", use_container_width=True):
            st.session_state.game_mode = "basic"
            st.rerun()
    with col_right:
        if st.button("進階模式：17點策略挑戰", use_container_width=True):
            st.session_state.game_mode = "advanced"
            st.rerun()

# --- 頁面 B：遊戲內容 ---
else:
    # 檢查模型
    saved_data = load_model()
    if not saved_data:
        st.error("找不到模型檔 cafe_model.pkl")
        st.stop()
    
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]

    # 頂部導覽區
    nav_col1, nav_col2 = st.columns([1, 5])
    with nav_col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ 返回主選單"):
            st.session_state.game_mode = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with nav_col2:
        title_text = "基礎經營模擬市集" if st.session_state.game_mode == "basic" else "17點策略極限挑戰賽"
        st.markdown(f"<h2 style='color: #2A5290; margin-top:-10px;'>{title_text}</h2>", unsafe_allow_html=True)

    # --- 關卡一內容 ---
    if st.session_state.game_mode == "basic":
        with st.container(border=True):
            st.markdown("### 🛠️ 自由調配基地")
            g1_city = st.selectbox("選擇進駐商圈", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化" if x=="changhua" else "台中" if x=="taichung" else "高雄")
            
            c1, c2 = st.columns(2)
            with c1:
                wifi = st.slider("WiFi 穩定度", 1, 5, 3)
                quiet = st.slider("環境安靜度", 1, 5, 3)
                tasty = st.slider("產品美味度", 1, 5, 3)
            with c2:
                cheap = st.slider("物美價廉 CP值", 1, 5, 3)
                music = st.slider("空間音樂舒適度", 1, 5, 3)
                socket = st.radio("提供免費插座", ["不提供", "提供"], index=1, horizontal=True)
            
            limit = st.radio("用餐時間限制", ["不限時", "限時"], index=0, horizontal=True)
            
            if st.button("啟動 AI 經營預測", use_container_width=True):
                s_val = 1 if socket == "提供" else 0
                l_val = 1 if limit == "限時" else 0
                prob = get_prediction(g1_city, wifi, quiet, tasty, cheap, music, s_val, l_val, feature_cols, model)
                st.markdown("---")
                st.metric("AI 預估客滿機率", f"{prob*100:.2f}%")
                if prob > 0.6: st.balloons(); st.success("表現優異！")
                else: st.warning("還有進步空間！")

    # --- 關卡二內容 ---
    elif st.session_state.game_mode == "advanced":
        with st.container(border=True):
            st.markdown("### 🏆 17點極限商業戰")
            st.info("規則：各項加總（含插座、不限時各1分）最高不能超過 17 分！")
            g2_city = st.selectbox("挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化" if x=="changhua" else "台中" if x=="taichung" else "高雄")
            
            c3, c4 = st.columns(2)
            with c3:
                wifi = st.slider("WiFi 投資", 1, 5, 1)
                quiet = st.slider("安靜度投資", 1, 5, 1)
                tasty = st.slider("美味度投資", 1, 5, 1)
            with c4:
                cheap = st.slider("CP值投資", 1, 5, 1)
                music = st.slider("音樂投資", 1, 5, 1)
                socket = st.radio("插座服務(1分)", ["不提供", "提供"], horizontal=True)
            
            limit = st.radio("時間福利(不限時1分)", ["限時", "不限時"], horizontal=True)
            
            s_score = 1 if socket == "提供" else 0
            l_score = 1 if limit == "不限時" else 0
            total = wifi + quiet + tasty + cheap + music + s_score + l_score
            
            if total > 17: st.error(f"預算爆表！目前：{total}/17")
            else: st.success(f"預算安全：{total}/17")
            st.progress(min(1.0, total/17))

            if st.button("送交 AI 賽果評定", use_container_width=True):
                if total > 17: st.error("預算超支無法開店！")
                else:
                    s_val = s_score
                    l_val = 1 if limit == "限時" else 0
                    prob = get_prediction(g2_city, wifi, quiet, tasty, cheap, music, s_val, l_val, feature_cols, model)
                    st.markdown("---")
                    st.metric("挑戰賽最終得分", f"{prob*100:.2f}%")
                    if prob > 0.6: st.balloons(); st.success("恭喜通關！")
