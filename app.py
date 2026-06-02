import streamlit as st
import joblib
import pandas as pd

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

    # --- 關卡一：自由經營模擬 (已完美對齊排列) ---
    if st.session_state.game_mode == "basic":
        with st.container(border=True):
            st.markdown("### 🛠️ 自由調配基地")
            g1_city = st.selectbox("選擇進駐商圈", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈")
            
            st.markdown("#### 店內硬體與品質設定")
            # 5 個拉桿乾淨排列
            c1, c2 = st.columns(2)
            with c1:
                wifi = st.slider("WiFi 穩定度", 1, 5, 3)
                quiet = st.slider("環境安靜度", 1, 5, 3)
                tasty = st.slider("產品美味度", 1, 5, 3)
            with c2:
                cheap = st.slider("物美價廉 CP值", 1, 5, 3)
                music = st.slider("空間音樂舒適度", 1, 5, 3)
            
            st.markdown("#### 顧客福利開放")
            # 單選按鈕獨立移至下方，並且左右並排同行
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
                
                if prob > 0.75:
                    st.balloons()
                    st.success("🎉 **餐飲界降臨的救世主神店！！！**")
                    st.markdown("> **AI 評價**：天啊！這到底是什麼完美的神仙配置？！妳開的不是咖啡廳，是信仰中心吧！店門口排隊的人潮已經繞了商圈三圈，連警察都來維持秩序了。客滿機率高到隨機森林模型都在為妳鼓掌，準備躺著數錢數到手抽筋吧！💰✨")
                elif prob > 0.45:
                    st.success("☕ **穩紮穩打的排隊名店！**")
                    st.markdown("> **AI 評價**：非常精準的商業眼光！這套配置完全踩中了顧客的痛點。店內高朋滿座，鍵盤敲擊聲與咖啡香交織，基本客源穩如泰山。雖然沒有到驚天動地，但絕對是天天客滿、穩定獲利，隔壁店家都在偷偷抄妳的菜單呢！😎")
                elif prob > 0.20:
                    st.warning(" 🥶 **生意冷清的勉強度日小店...**")
                    st.markdown("> **AI 評價**：唔... 現場氣氛有點尷尬。店裡雖然偶爾有一兩桌客人，但大部分時間服務生都在擦桌子跟發呆。這個配置不上不下，顧客找不到特地過來的理由。快去調整一下滑桿，不然下個月的房租可能會讓妳哭出來喔！下定決心做出改變吧！🥺")
                else:
                    st.error(" 😭 **慘不忍睹！正面臨倒閉危機！**")
                    st.markdown("> **AI 評價**：逼波逼波逼波！根本爛！這是一個連冷氣吹出來都是絕望味道的配置。客滿率低到隨機森林模型都在流淚。店裡安靜得掉下一根針都聽得到，門口還在貼頂讓紅單。不要氣餒！身為創業者這只是必經之路，快回頭重新配製完美的客滿配方！💪")

    # --- 關卡二：17點策略挑戰 (同步完成完美對齊) ---
    elif st.session_state.game_mode == "advanced":
        with st.container(border=True):
            st.markdown("### 🏆 17點極限商業戰")
            st.markdown("""
                <div style="background-color: #fcfbfa; padding: 15px; border-radius: 8px; border-left: 5px solid #2A5290; margin-bottom: 20px;">
                    <b>17點挑戰規則：</b> 創業資金有限！以下拉桿分數加總，外加提供插座(算1分)與不限時福利(算1分)，最高不能超過 17 分！
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
            
            if total > 17: st.error(f"❌ 預算爆表！目前已使用：{total} / 17 分（請調低分數以符合競賽規範）")
            else: st.success(f"✅ 預算安全！目前已使用：{total} / 17 分（尚餘 {17 - total} 分）")
            st.progress(min(1.0, total/17))

            if st.button("送交 AI 進行賽果評定", use_container_width=True):
                if total > 17:
                    st.error("🛑 資金超支！請調整配置至 17 分以內。")
                else:
                    s_val = s_score
                    l_val = 1 if limit == "限時" else 0
                    prob = get_prediction(g2_city, wifi, quiet, tasty, cheap, music, s_val, l_val, feature_cols, model)
                    st.markdown("---")
                    st.metric("挑戰賽最終得分", f"{prob*100:.2f}%")
                    
                    if prob > 0.65:
                        st.balloons()
                        st.success("👑 **商業傳奇！終極鐵桿客滿經理人！**")
                        st.markdown("> **AI 評定**：跪了！妳就是高難度極限挑戰的華爾街之狼！在預算只有 17 分的極致地獄限制下，妳居然還能把每一毛錢都花在刀口上，精準重擊該商圈的痛點！這客滿率簡報拿出去，創投直接現場給妳簽開支票！滿分通關啦！🏆🔥")
                    elif prob > 0.45:
                        st.success("🤝 **精明過人的創業智多星！**")
                        st.markdown("> **AI 評定**：太厲害了！這算盤打得真響！在有限的資源裡做到了最完美的權衡取捨（Trade-off）。店裡的翻桌率跟客滿機率配合得天衣無縫，既沒超支又確保了顧客心甘情願掏錢，妳非常有當大老闆的商業天賦！💰")
                    else:
                        st.warning(" 🤕 **預算沒超支，但顧客不買單... 遺憾落敗！**")
                        st.markdown("> **AI 評定**：可惜了！雖然妳很克制地把預算控制在 17 分之內，但這個配置方法在該商圈像是把錢丟進水裡，顧客完全不賞臉啊。咖啡廳變成了「蚊子館生態園區」，快去重新調配點數，證明妳的商業策略實力吧！別認輸！⚔️")
