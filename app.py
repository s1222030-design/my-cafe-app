import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定 (設定寬版與標題)
st.set_page_config(page_title="AI 咖啡廳改造大亨", page_icon="☕", layout="wide")

# 2. 注入精準 CSS (完美實現 #2A5290 與 #F7F5F2 色彩，並美化封面)
st.markdown("""
    <style>
    /* 全域背景微調，襯托奶油白 */
    .main { background-color: #fcfbfa; }
    
    /* 1. 精準修改拉桿軌道顏色 (#2A5290) */
    .stSlider > div > div > div > div {
        background-color: #2A5290 !important;
    }
    
    /* 2. 精準修改拉桿滑動圓鈕顏色 (#F7F5F2) 與藍色邊框 */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #F7F5F2 !important;
        border: 3px solid #2A5290 !important;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* 封面與遊戲主按鈕美化 */
    .stButton > button {
        background: linear-gradient(135deg, #2A5290 0%, #1e3a6d 100%);
        color: #F7F5F2 !important;
        border-radius: 30px !important;
        font-weight: bold !important;
        font-size: 1.25rem !important;
        padding: 12px 40px !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(42, 82, 144, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 20px rgba(42, 82, 144, 0.35);
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
        # 使用極具氛圍感的咖啡廳特寫插圖作為封面
        st.image("https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200", use_column_width=True)
        
        st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px;">☕ AI 咖啡廳改造大亨</h1>
                <p style="color: #6b5b4b; font-size: 1.2rem; margin-top: 10px; font-weight: 500;">
                    歡迎來到商業數據戰場！妳能成功利用大數據，調配出完美的客滿配方嗎？
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 封面進入遊戲大按鈕
        if st.button("🎮 點擊開始遊戲 🚀", key="start_game_trigger"):
            st.session_state.game_started = True
            st.rerun()
            
    st.stop() # 阻斷後續畫面，直到玩家按下按鈕

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
    st.error("❌ 讀取模型失敗，請確認 cafe_model.pkl 是否存在。")
    st.stop()

# 遊戲主頁大標題
st.markdown("""
    <div style="padding: 10px 0; margin-bottom: 20px;">
        <h2 style="color: #2A5290; font-weight: 800;">🏆 AI 咖啡廳策略模擬戰場</h2>
        <p style="color: #718096; margin-top: -5px;">配置專屬指標，隨機森林模型將即時為妳的商業決策打分數！</p>
    </div>
""", unsafe_allow_html=True)

# 建立兩個遊戲的頁籤
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
    
    if st.button("🚀 啟動 AI 大數據經營模擬预测", key="g1_submit_btn"):
        s_val = 1 if g1_socket == "提供" else 0
        l_val = 1 if g1_limit == "限時" else 0
        prob = get_prediction(g1_city, g1_wifi, g1_quiet, g1_tasty, g1_cheap, g1_music, s_val, l_val)
        
        st.markdown("---")
        st.metric(label="📊 AI 預估最終『客滿機率』", value=f"{prob * 100:.2f}%")
        
        if prob > 0.75:
            st.balloons()
            st.success("🏆 【傳奇神店】太強了！服務與品質皆為頂級，店門口排隊排到馬路上！")
        elif prob > 0.45:
            st.success("👍 【穩定獲利】表現不錯！店內高朋滿座，基本客源非常穩固。")
        elif prob > 0.20:
            st.warning("⚠️ 【勉強度日】生意稍微冷清... 建議檢查一下配置是否有優化空間？")
        else:
            st.error("🚨 【面臨倒閉】慘不忍睹！客滿率極低，請立刻重新調整經營品質！")
            
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# 🔥 Tab 2：17點策略挑戰賽
# ---------------------------------------------------------------------
with tab2:
    st.markdown("<div class='game-card'>", unsafe_allow_html=True)
    st.markdown("### 💸 17點極限商業戰")
    st.markdown("""
        <div style='background-color: #f7f5f2; padding: 15px; border-radius: 8px; border-left: 5px solid #2A5290; margin-bottom: 20px;'>
            <b>📌 17點挑戰規則：</b> 創業資金有限！以下拉桿分數加總，外加<b>提供插座(算1分)</b>與<b>不限時福利(算1分)</b>，最高<b>不能超過 17 分</b>！
        </div>
    """, unsafe_allow_html=True)
    
    g2_city = st.selectbox("📍 選擇本次競賽挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈", key="g2_city_select")
    
    col5, col6 = st.columns(2)
    with col5:
        g2_wifi = st.slider("📶 投資 WiFi 穩定度", 1, 5, 1, key="g2_slider_w")
        g2_quiet = st.slider("🤫 投資 環境安靜度", 1, 5, 1, key="g2_slider_q")
        g2_tasty = st.slider("☕ 投資 產品美味度", 1, 5, 1, key="g2_slider_t")
    with col6:
        g2_cheap = st.slider("💰 投資 CP值與價格", 1, 5, 1, key="g2_slider_c")
        g2_music = st.slider("🎵 投資 音樂環境", 1, 5, 1, key="g2_slider_m")
    
    st.markdown("#### 🔹 加值策略配置")
    col7, col8 = st.columns(2)
    with col7:
        g2_socket = st.radio("🔌 插座服務 (提供 = 1分)", ["不提供", "提供"], index=0, horizontal=True, key="g2_radio_s")
    with col8:
        g2_limit = st.radio("⏳ 限時規定 (不限時 = 1分)", ["限時", "不限時"], index=0, horizontal=True, key="g2_radio_l")
        
    # 動態點數運算
    s_score = 1 if g2_socket == "提供" else 0
    l_score = 1 if g2_limit == "不限時" else 0
    total_points = g2_wifi + g2_quiet + g2_tasty + g2_cheap + g2_music + s_score + l_score
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 動態預算條提示
    if total_points > 17:
        st.error(f"🟥 💥 預算爆表！目前已使用：{total_points} / 17 分（請調低分數以符合競賽規範）")
    else:
        st.success(f"🟩 預算安全！目前已使用：{total_points} / 17 分（尚餘 {17 - total_points} 分）")
    st.progress(min(1.0, total_points / 17))
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏆 送交 AI 進行賽果評定", key="g2_submit_btn"):
        if total_points > 17:
            st.error("❌ 資金超支！無法開店，請調整配置。")
        else:
            s_val = s_score
            l_val = 1 if g2_limit == "限時" else 0
            prob = get_prediction(g2_city, g2_wifi, g2_quiet, g2_tasty, g2_cheap, g2_music, s_val, l_val)
            
            st.markdown("---")
            st.metric(label="🎯 最終經營挑戰賽得分（客滿機率）", value=f"{prob * 100:.2f}%")
            
            if prob > 0.65:
                st.balloons()
                st.success("👑 【神級鐵桿經理人】太強了！妳用有限的 17 分預算，精準切中商圈痛點，完美通關！")
            elif prob > 0.45:
                st.success("💰 【精明創業家】很不錯！預算控制得當，店裡生意興隆，穩穩賺大錢！")
            else:
                st.warning("📉 【決策失誤】可惜！配置雖然沒超支，但無法吸引該城市的目標客群，再換個配方試試看！")
                
    st.markdown("</div>", unsafe_allow_html=True)
