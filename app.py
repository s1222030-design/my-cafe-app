import streamlit as st
import joblib
import pandas as pd
import base64
import random  # 👈 1. 導入隨機套件！

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 終極 CSS 注入
st.markdown("""
    <style>
    .stApp, .main { 
        background-color: #F7F5F2 !important; 
    }
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
    .back-btn button {
        background: #6b5b4b !important;
        font-size: 0.9rem !important;
        padding: 5px 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化導覽狀態
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None

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

# ─── 🛠️ 2. 改良版：隨機選圖並顯示的函式 ───
def show_random_result_image(image_list):
    try:
        chosen_image = random.choice(image_list) # 從清單裡隨機抽一張
        st.image(chosen_image, width=400)
    except:
        st.caption(f"💡 [提示：請確認資料夾內是否有這幾張圖：{', '.join(image_list)}]")

# =====================================================================
# 🎬 畫面邏輯控制
# =====================================================================

# --- 頁面 A：封面與模式選擇 (用妳自己的圖片版) ---
if st.session_state.game_mode is None:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ─── 🛠️ 新增這段：讀取並編碼妳的本地圖片 ───
    try:
        # ⚠️ 這裡要改成妳實際的圖片檔名，例如 "cover.jpg" 或 "my_cafe.png"
        with open("那我們就走吧.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        img_src = f"data:image/jpeg;base64,{encoded_string}"
    except FileNotFoundError:
        # 如果不小心找不到檔案，就用原本的預設網址擋一下，避免網頁掛掉
        img_src = "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&q=80&w=1200"
    # ──────────────────────────────────────

    st.markdown(f"""
        <div class="cover-container">
            # 👇 這裡的 src="https://..." 已經換成一個變數 img_src 了
            <img class="cover-image" src="{img_src}">
            <h1 style="color: #2A5290; font-size: 3rem; font-weight: 800; letter-spacing: 2px; margin-bottom: 5px;">AI Cafe Tycoon</h1>
            <p style="color: #6b5b4b; font-size: 1.2rem; font-weight: 500; margin-bottom: 30px;">
                歡迎來到商業數據戰場！請選擇您的挑戰模式：
            </p>
        </div>
    """, unsafe_allow_html=True)
    
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
    saved_data = load_model()
    if not saved_data:
        st.error("找不到模型檔 cafe_model.pkl")
        st.stop()
    
    model = saved_data["model"]
    feature_cols = saved_data["feature_cols"]

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

    # --- 關卡一：自由經營模擬 ---
    if st.session_state.game_mode == "basic":
        with st.container(border=True):
            st.markdown("### 🛠️ 自由調配基地")
            g1_city = st.selectbox("選擇進駐商圈", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈")
            
            st.markdown("#### 店內硬體與品質設定")
            c1, c2 = st.columns(2)
            with c1:
                wifi = st.slider("WiFi 穩定度", 1, 5, 3)
                quiet = st.slider("環境安靜度", 1, 5, 3)
                tasty = st.slider("產品美味度", 1, 5, 3)
            with c2:
                cheap = st.slider("物美價廉 CP值", 1, 5, 3)
                music = st.slider("空間音樂舒適度", 1, 5, 3)
            
            st.markdown("#### 顧客福利開放")
            c_welfare1, c_welfare2 = st.columns(2)
            with c_welfare1:
                socket = st.radio("每個座位提供免費插座", ["不提供", "提供"], index=1, horizontal=True)
            with c_welfare2:
                limit = st.radio("客滿時的用餐時間限制", ["不限時", "限時"], index=0, horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("啟動 AI 大數據經營模擬預測", use_container_width=True):
                s_val = 1 if socket == "提供" else 0
                l_val = 1 if limit == "限時" else 0
                prob = get_prediction(g1_city, wifi, quiet, tasty, cheap, music, s_val, l_val, feature_cols, model)
                st.markdown("---")
                st.metric("AI 預估客滿機率", f"{prob*100:.2f}%")
                
                # 🖼️ 3. 隨機圖片池設定（妳可以自由把新圖片檔名加進去中括號裡喔！）
                if prob > 0.75:
                    st.balloons()
                    st.success("🎉 **餐飲界降臨的救世主神店！！！**")
                    # 👇 丟入神店圖片池，程式會自己 3 抽 1
                    show_random_result_image(["god1.jpg", "god2.jpg", "god3.jpg", "god4.jpg", "god5.jpg", "god6.jpg"]) 
                    st.markdown("> **AI 評價**：天啊！這到底是什麼完美的神仙配置？！妳開的不是咖啡廳，是信仰中心吧！")
                elif prob > 0.45:
                    st.success("☕ **穩紮穩打的排隊名店！**")
                    # 👇 丟入好店圖片池，2 抽 1
                    show_random_result_image(["good1.jpg", "good2.jpg", "good3.jpg", "good4.jpg", "good5.jpg", "good6.jpg"]) 
                    st.markdown("> **AI 評價**：非常精準的商業眼光！這套配置完全踩中了顧客的痛點。")
                elif prob > 0.20:
                    st.warning(" 🥶 **生意冷清的勉強度日小店...**")
                    show_random_result_image(["bad1.jpg", "bad2.jpg", "bad3.jpg", "bad4.jpg", "bad5.jpg"]) 
                    st.markdown("> **AI 評價**：唔... 現場氣氛有點尷尬。店裡雖然偶爾有一兩桌客人。")
                else:
                    st.error(" 😭 **慘不忍睹！正面臨倒閉危機！**")
                    # 👇 丟入倒閉圖片池
                    show_random_result_image(["die1.jpg", "die2.jpg", "die3.jpg", "die4.jpg", "die5.jpg", "die6.jpg"]) 
                    st.markdown("> **AI 評價**：逼波逼波逼波！根本爛！這是一個連冷氣吹出來都是絕望味道的配置。")

    # --- 關卡二：17點策略挑戰 ---
    elif st.session_state.game_mode == "advanced":
        with st.container(border=True):
            st.markdown("### 🏆 17點極限商業戰")
            st.markdown("""
                <div style="background-color: #fcfbfa; padding: 15px; border-radius: 8px; border-left: 5px solid #2A5290; margin-bottom: 20px;">
                    <b>17點挑戰規則：</b> 創業資金有限！最高不能超過 17 分！
                </div>
            """, unsafe_allow_html=True)
            
            g2_city = st.selectbox("選擇本次競賽挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈", key="g2_city_select")
            
            st.markdown("#### 投資項目設定")
            c3, c4 = st.columns(2)
            with c3:
                wifi = st.slider("投資 WiFi 穩定度", 1, 5, 1)
                quiet = st.slider("投資 環境安靜度", 1, 5, 1)
                tasty = st.slider("投資 產品美味度", 1, 5, 1)
            with c4:
                cheap = st.slider("投資 CP值與價格", 1, 5, 1)
                music = st.slider("投資 音樂環境", 1, 5, 1)
            
            st.markdown("#### 加值策略配置 (完美同行並列)")
            c_welfare3, c_welfare4 = st.columns(2)
            with c_welfare3:
                socket = st.radio("插座服務 (提供 = 1分)", ["不提供", "提供"], horizontal=True)
            with c_welfare4:
                limit = st.radio("限時規定 (不限時 = 1分)", ["限時", "不限時"], horizontal=True)
                
            s_score = 1 if socket == "提供" else 0
            l_score = 1 if limit == "不限時" else 0
            total = wifi + quiet + tasty + cheap + music + s_score + l_score
            
            if total > 17: st.error(f"❌ 預算爆表！目前已使用：{total} / 17 分")
            else: st.success(f"✅ 預算安全！目前已使用：{total} / 17 分")
            st.progress(min(1.0, total/17))

            if st.button("送交 AI 進行賽果評定", use_container_width=True):
                if total > 17:
                    st.error("🛑 資金超支！政府稽查勒令停業。")
                else:
                    s_val = s_score
                    l_val = 1 if limit == "限時" else 0
                    prob = get_prediction(g2_city, wifi, quiet, tasty, cheap, music, s_val, l_val, feature_cols, model)
                    st.markdown("---")
                    st.metric("挑戰賽最終得分", f"{prob*100:.2f}%")
                    
                    # 🖼️ 進階賽同步啟用隨機抽圖！
                    if prob > 0.65:
                        st.balloons()
                        st.success("👑 **商業傳奇！終極鐵桿客滿經理人！**")
                        show_random_result_image(["god1.jpg", "god2.jpg", "god3.jpg", "god4.jpg", "god5.jpg", "god6.jpg"])
                        st.markdown("> **AI 評定**：跪了！妳就是高難度極限挑戰的華爾街之狼！")
                    elif prob > 0.45:
                        st.success("🤝 **精明過人的創業智多星！**")
                        show_random_result_image(["good1.jpg", "good2.jpg", "good3.jpg", "good4.jpg", "good5.jpg", "good6.jpg"])
                        st.markdown("> **AI 評定**：太厲害了！這算盤打得真響！")
                    else:
                        st.warning(" 🤕 **預算沒超支，但顧客不買單... 遺憾落敗！**")
                        show_random_result_image(["bad1.jpg", "bad2.jpg", "bad3.jpg", "bad4.jpg", "bad5.jpg", "die1.jpg", "die2.jpg", "die3.jpg", "die4.jpg", "die5.jpg", "die6.jpg"])
                        st.markdown("> **AI 評定**：可惜了！咖啡廳變成了「蚊子館生態園區」。")
