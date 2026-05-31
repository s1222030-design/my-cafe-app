import streamlit as st
import joblib
import pandas as pd

# 1. 網頁頂部設定（設定為寬版、高質感標題）
st.set_page_config(
    page_title="AI 咖啡廳改造大亨",
    page_icon="☕",
    layout="wide"
)

# 自訂網頁 CSS 樣式（美化拉桿與卡片底色）
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stSlider > div > div > div > div { background-color: #319795; }
    div.stButton > button:first-child {
        background-color: #319795; color: white; font-weight: bold;
        border-radius: 8px; width: 100%; height: 45px; border: none;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11);
        transition: all 0.15s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #2c7a7b; transform: translateY(-1px);
    }
    .custom-card {
        background-color: #ffffff; padding: 25px; 
        border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 載入模型
@st.cache_resource
def load_model():
    return joblib.load("cafe_model.pkl")

try:
    saved_data = load_model()
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]
except Exception as e:
    st.error("❌ 找不到模型檔案 cafe_model.pkl，請確保它跟 app.py 放在同一個 GitHub 庫喔！")
    st.stop()

# 3. 頂級奢華網頁大標題
st.markdown("""
    <div style="text-align: center; padding: 20px 0px;">
        <h1 style="color: #1a202c; font-size: 3rem; font-weight: 800; margin-bottom: 5px;">☕ AI 咖啡廳改造大亨</h1>
        <p style="color: #718096; font-size: 1.2rem;">利用隨機森林大數據，精準預測妳的店面客滿率！</p>
        <hr style="border: 0; height: 2px; background: linear-gradient(to right, rgba(0,0,0,0), #319795, rgba(0,0,0,0)); margin-top: 20px;">
    </div>
""", unsafe_allow_html=True)

# 預測運算核心
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

# 4. 建立美美的 Tabs 標籤頁
tab1, tab2 = st.tabs(["🎮 自由經營模擬市集", "🔥 17點策略極限挑戰賽"])

# =====================================================================
# 🎮 Tab 1：自由經營模擬
# =====================================================================
with tab1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### 🛠️ 自由調配經營藍圖")
    st.caption("在這裡妳可以無限制地調整參數，試探各個商圈客人的喜好大數據。")
    
    g1_city = st.selectbox("📍 欲創立店面的目標城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化市核心商圈" if x=="changhua" else "台中市精華商圈" if x=="taichung" else "高雄市三多商圈")
    
    st.markdown("#### 🔹 店內品質設定（1分最差、5分完美）")
    col1, col2 = st.columns(2)
    with col1:
        g1_wifi = st.slider("📶 高速 WiFi 穩定度", 1, 5, 3, key="g1_w")
        g1_quiet = st.slider("🤫 環境安靜、適宜工作度", 1, 5, 3, key="g1_q")
        g1_tasty = st.slider("☕ 咖啡與甜點美味程度", 1, 5, 3, key="g1_t")
    with col2:
        g1_cheap = st.slider("💰 價格親民度 / CP值", 1, 5, 3, key="g1_c")
        g1_music = st.slider("🎵 店內背景音樂舒適度", 1, 5, 3, key="g1_m")
    
    st.markdown("#### 🔹 消費者權益福利")
    col3, col4 = st.columns(2)
    with col3:
        g1_socket = st.radio("🔌 每個座位是否提供免費插座", ["不提供", "提供"], index=1, horizontal=True)
    with col4:
        g1_limit = st.radio("⏳ 客滿時的用餐時間限制規定", ["不限時", "限時"], index=0, horizontal=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 啟動 AI 大數據經營模擬", key="btn1"):
        s_val = 1 if g1_socket == "提供" else 0
        l_val = 1 if g1_limit == "限時" else 0
        prob = get_prediction(g1_city, g1_wifi, g1_quiet, g1_tasty, g1_cheap, g1_music, s_val, l_val)
        
        # 精美結果圖卡
        st.markdown("---")
        st.metric(label="📊 預估平均「客滿機率」", value=f"{prob * 100:.2f}%")
        
        if prob > 0.75:
            st.balloons()
            st.success("🏆 【傳奇神店】太強了！服務與品質皆為頂級，店門口排隊排到馬路上！")
        elif prob > 0.45:
            st.success("👍 【穩定獲利】表現不錯！店內高朋滿座，基本客源非常穩固。")
        elif prob > 0.20:
            st.warning("⚠️ 【勉強度日】生意稍顯冷清... 建議調整內部配置，加強弱項指標。")
        else:
            st.error("🚨 【面臨倒閉】慘不忍睹！客滿率極低，請立刻重新調整經營品質！")
            
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# 🔥 Tab 2：17點策略挑戰賽
# =====================================================================
with tab2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.markdown("### 💸 17點創業極限大考驗")
    st.markdown("""
        <div style="background-color: #edf2f7; padding: 15px; border-radius: 8px; border-left: 5px solid #4a5568; margin-bottom: 20px;">
            <b>📌 商業競賽規則：</b> 創業資金極度有限！以下 7 個指標加總<b>最高不能超過 17 分</b>！<br>
            ⚠️ 拉桿分數即點數；提供插座算 <b>1分</b>；選擇消費者最愛的「不限時」福利算 <b>1分</b>。
        </div>
    """, unsafe_allow_html=True)
    
    g2_city = st.selectbox("📍 選擇本次競賽挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化市核心商圈" if x=="changhua" else "台中市精華商圈" if x=="taichung" else "高雄市三多商圈", key="g2_c_v")
    
    st.markdown("#### 🔹 投資點數分配")
    col5, col6 = st.columns(2)
    with col5:
        g2_wifi = st.slider("📶 投資 WiFi 穩定度", 1, 5, 1, key="g2_w")
        g2_quiet = st.slider("🤫 投資 環境安靜度", 1, 5, 1, key="g2_q")
        g2_tasty = st.slider("☕ 投資 產品美味度", 1, 5, 1, key="g2_t")
    with col6:
        g2_cheap = st.slider("💰 投資 CP值與價格", 1, 5, 1, key="g2_c")
        g2_music = st.slider("🎵 投資 音樂環境", 1, 5, 1, key="g2_m")
    
    st.markdown("#### 🔹 加值福利配置")
    col7, col8 = st.columns(2)
    with col7:
        g2_socket = st.radio("🔌 插座服務 (提供 = 1分)", ["不提供", "提供"], index=0, horizontal=True, key="g2_s")
    with col8:
        g2_limit = st.radio("⏳ 限時規定 (不限時 = 1分)", ["限時", "不限時"], index=0, horizontal=True, key="g2_l")
        
    # 計算點數
    s_score = 1 if g2_socket == "提供" else 0
    l_score = 1 if g2_limit == "不限時" else 0
    total_points = g2_wifi + g2_quiet + g2_tasty + g2_cheap + g2_music + s_score + l_score
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 網頁即時互動進度條
    if total_points > 17:
        st.error(f"💥 預算爆表！目前已使用：{total_points} / 17 分。資金不足，請調低上方投資！")
    else:
        st.success(f"✅ 預算安全。目前已使用：{total_points} / 17 分（剩餘資金：{17 - total_points} 分）")
    
    st.progress(min(1.0, total_points / 17))
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🏆 消耗預算，送交 AI 進行賽果評定", key="btn2"):
        if total_points > 17:
            st.error("❌ 資金超支！無法開店，請先符合預算規則。")
        else:
            s_val = s_score
            l_val = 1 if g2_limit == "限時" else 0
            prob = get_prediction(g2_city, g2_wifi, g2_quiet, g2_tasty, g2_cheap, g2_music, s_val, l_val)
            
            st.markdown("---")
            st.metric(label="🎯 最終經營挑戰賽得分（客滿率）", value=f"{prob * 100:.2f}%")
            
            if prob > 0.65:
                st.balloons()
                st.success("👑 【神級鐵桿經理人】太扯了！妳用精準的 17 分預算切中商圈痛點，完美通關！")
            elif prob > 0.45:
                st.success("💰 【精明創業家】很不錯！預算控制得當，店裡穩穩獲利賺大錢！")
            else:
                st.warning("📉 【決策失誤】可惜！配置雖然沒超支，但無法吸引該城市的目標客群，再換個配方試試看！")
                
    st.markdown("</div>", unsafe_allow_html=True)
