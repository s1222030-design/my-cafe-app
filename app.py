import streamlit as st
import joblib
import pandas as pd

# 1. 設定網頁標題與風格
st.set_page_config(
    page_title="AI 咖啡廳改造大亨",
    page_icon="☕",
    layout="centered"
)

# 2. 載入我們從 Colab 下載的模型檔
@st.cache_resource
def load_model():
    # 請確保 cafe_model.pkl 和這個 app.py 放在同一個資料夾
    return joblib.load("cafe_model.pkl")

try:
    saved_data = load_model()
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]
except Exception as e:
    st.error("❌ 找不到模型檔案 cafe_model.pkl，請確保它跟 app.py 放在一起喔！")
    st.stop()

# 3. 網頁大標題與精美介紹
st.title("☕ AI 咖啡廳改造大亨")
st.subheader("利用隨機森林大數據，精準預測妳的客滿率！")

# 透過 Streamlit 的 Tabs 標籤頁功能，把兩個遊戲優雅地分開
tab1, tab2 = st.tabs(["🎮 關卡一：自由經營模擬", "🔥 關卡二：17點策略挑戰賽"])

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
    # 確保欄位順序完全一致
    missing_cols = set(feature_cols) - set(input_df.columns)
    for c in missing_cols: input_df[c] = 0
    input_df = input_df[feature_cols]
    
    prob = model.predict(input_df)[0]
    return max(0.0, min(1.0, prob))

# =====================================================================
# 🎮 Tab 1：自由經營模擬
# =====================================================================
with tab1:
    st.markdown("### 自由調整參數，觀察大數據的客滿趨勢")
    
    g1_city = st.selectbox("📍 選擇創業城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化縣" if x=="changhua" else "台中市" if x=="taichung" else "高雄市", key="g1_city")
    
    col1, col2 = st.columns(2)
    with col1:
        g1_wifi = st.slider("📶 WiFi穩定度 (5最佳)", 1, 5, 3, key="g1_wifi")
        g1_quiet = st.slider("🤫 安靜程度 (5最佳)", 1, 5, 3, key="g1_quiet")
        g1_tasty = st.slider("☕ 美味程度 (5最佳)", 1, 5, 3, key="g1_tasty")
    with col2:
        g1_cheap = st.slider("💰 CP值/划算 (5最佳)", 1, 5, 3, key="g1_cheap")
        g1_music = st.slider("🎵 音樂舒適 (5最佳)", 1, 5, 3, key="g1_music")
        g1_socket = st.radio("🔌 插座服務", ["不提供", "提供"], index=1, key="g1_socket")
        g1_limit = st.radio("⏳ 限時規定", ["不限時", "限時"], index=0, key="g1_limit")
        
    if st.button("🚀 開始 AI 經營模擬", type="primary", key="g1_btn"):
        s_val = 1 if g1_socket == "提供" else 0
        l_val = 1 if g1_limit == "限時" else 0
        prob = get_prediction(g1_city, g1_wifi, g1_quiet, g1_tasty, g1_cheap, g1_music, s_val, l_val)
        
        st.metric(label="🎯 預估『客滿機率』", value=f"{prob * 100:.2f}%")
        if prob > 0.75: st.balloons(); st.success("🏆 【傳奇神店】太強了！服務與品質皆為頂級，店門口排隊排到馬路上！")
        elif prob > 0.45: st.success("👍 【穩定獲利】表現不錯！店內高朋滿座，基本客源非常穩固。")
        elif prob > 0.20: st.warning("⚠️ 【勉強度日】生意冷清... 建議檢查一下配置是否有優化空間？")
        else: st.error("🚨 【面臨倒閉】慘不忍睹！客滿率極低，請立刻重新調整經營品質！")

# =====================================================================
# 🔥 Tab 2：17點策略挑戰賽
# =====================================================================
with tab2:
    st.markdown("### 💸 17點創業極限大考驗")
    st.info("💡 規則：開店資金有限！所有參數加起來最多只能花 17 分。（拉桿分數即點數、提供插座算 1 分、選擇不限時福利算 1 分）")
    
    g2_city = st.selectbox("📍 選擇挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化縣" if x=="changhua" else "台中市" if x=="taichung" else "高雄市", key="g2_city")
    
    col3, col4 = st.columns(2)
    with col3:
        g2_wifi = st.slider("📶 WiFi穩定度", 1, 5, 1, key="g2_wifi")
        g2_quiet = st.slider("🤫 安靜程度", 1, 5, 1, key="g2_quiet")
        g2_tasty = st.slider("☕ 美味程度", 1, 5, 1, key="g2_tasty")
    with col4:
        g2_cheap = st.slider("💰 CP值/划算", 1, 5, 1, key="g2_cheap")
        g2_music = st.slider("🎵 音樂舒適", 1, 5, 1, key="g2_music")
        g2_socket = st.radio("🔌 插座服務 (提供=1分)", ["不提供", "提供"], index=0, key="g2_socket")
        g2_limit = st.radio("⏳ 限時規定 (不限時=1分)", ["限時", "不限時"], index=0, key="g2_limit")
        
    # 動態點數計算
    s_score = 1 if g2_socket == "提供" else 0
    l_score = 1 if g2_limit == "不限時" else 0
    total_points = g2_wifi + g2_quiet + g2_tasty + g2_cheap + g2_music + s_score + l_score
    
    st.markdown("---")
    # 網頁端專屬：動態高質感進度條與色彩提示
    if total_points > 17:
        st.error(f"🟥 💥 點數超支！目前已使用：{total_points} / 17 分（請降低分數以符合預算）")
        st.progress(1.0)
    else:
        st.success(f"🟩 目前已使用點數：{total_points} / 17 分（尚餘 {17 - total_points} 分）")
        st.progress(total_points / 17)
        
    if st.button("🏆 送交 AI 評定賽果", type="primary", key="g2_btn"):
        if total_points > 17:
            st.error("❌ 預算超支！無法提交，請調低分數再試。")
        else:
            s_val = s_score
            l_val = 1 if g2_limit == "限時" else 0
            prob = get_prediction(g2_city, g2_wifi, g2_quiet, g2_tasty, g2_cheap, g2_music, s_val, l_val)
            
            st.metric(label="🎯 最終預估『客滿機率』", value=f"{prob * 100:.2f}%")
            if prob > 0.65:
                st.balloons()
                st.success("👑 【神級鐵桿經理人】太扯了！你用有限的 17 分預算，調配出完美的黃金比例！堪稱教科書等級的商業決策！")
            elif prob > 0.45:
                st.success("💰 【精明創業家】很不錯！預算控制得當，店裡生意興隆，穩穩賺大錢！")
            else:
                st.warning("📉 【決策失誤】可惜！雖然符合 17 分限制，但你的配置沒辦法吸引該城市的客人。")