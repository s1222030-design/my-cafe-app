import streamlit as st

import joblib

import pandas as pd



# 1. 網頁基本設定

st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")



# 2. 注入自訂 CSS：強制套用顏色，消滅紅色，並修正 Streamlit 核心元件主題

st.markdown("""

    <style>

    /* 全域背景色微調 */

    .main { background-color: #fcfbfa; }

    

    /* 核心變數強力壓制 */

    :root {

        --primary-color: #2A5290 !important;

    }

    

    /* 頁籤選取狀態顏色 */

    div[data-baseweb="tab-list"] button[aria-selected="true"] {

        color: #2A5290 !important;

        border-bottom-color: #2A5290 !important;

    }

    

    /* 修改拉桿軌道和進度條為海軍藍 */

    /* 整體軌道背景 */

    .stSlider [data-baseweb="slider"] > div > div {

        background-color: rgba(42, 82, 144, 0.1) !important;

    }

    /* 累積進度部分 */

    .stSlider [data-baseweb="slider"] div[role="presentation"] div:first-child {

        background-color: #2A5290 !important;

    }

    

    /* 修改拉桿滑動圓鈕 */

    .stSlider [data-baseweb="slider"] [role="slider"] {

        background-color: #F7F5F2 !important;

        border: 3px solid #2A5290 !important;

        box-shadow: 0px 2px 6px rgba(0,0,0,0.2) !important;

        width: 24px !important;

        height: 24px !important;

    }

    

    /* 修改 Radio 單選鈕為海軍藍 */

    /* 被選中時的核心圓點 */

    div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="true"] > div {

        border-color: #2A5290 !important;

        background-color: #2A5290 !important;

    }

    /* 選中時的外圈 */

    div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="true"] {

        border-color: #2A5290 !important;

    }

    /* 未選中時的外圈 */

    div[data-testid="stRadio"] div[role="radiogroup"] div[data-checked="false"] {

        border-color: rgba(42, 82, 144, 0.5) !important;

    }

    

    /* 進度條顏色變更 */

    div[data-baseweb="progress-bar"] > div { background-color: #2A5290 !important; }

    

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

    

    /* 高級海軍藍按鈕本體美化（字體顏色強制修正為 #F7F5F2） */

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

    

    /* 高質感卡片框 */

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

        

        _, g1_btn_col, _ = st.columns([1, 1, 1])

        with g1_btn_col:

            g1_click = st.button("啟動 AI 大數據經營模擬預測", key="g1_submit_btn", use_container_width=True)

            

        if g1_click:

            s_val = 1 if g1_socket == "提供" else 0

            l_val = 1 if g1_limit == "限時" else 0

            prob = get_prediction(g1_city, g1_wifi, g1_quiet, g1_tasty, g1_cheap, g1_music, s_val, l_val)

            

            st.markdown("---")

            st.metric(label="AI 預估最終客滿機率", value=f"{prob * 100:.2f}%")

            

            if prob > 0.75:

                st.balloons()

                st.success("傳奇神店！服務與品質皆為頂級，店門口排隊排到馬路上！")

            elif prob > 0.45:

                st.success("穩定獲利！表現不錯！店內高朋滿座，基本客源非常穩固。")

            elif prob > 0.20:

                st.warning("勉強度日！生意稍微冷清... 建議檢查一下配置是否有優化空間？")

            else:

                st.error("面臨倒閉！慘不忍睹！客滿率極低，請立刻重新調整經營品質！")

                

        st.markdown("</div>", unsafe_allow_html=True)



    # ---------------------------------------------------------------------

    # Tab 2：17點策略挑戰賽

    # ---------------------------------------------------------------------

    with tab2:

        st.markdown("<div class='game-card'>", unsafe_allow_html=True)

        st.markdown("### 17點極限商業戰")

        st.markdown("""

            <div style="background-color: #f7f5f2; padding: 15px; border-radius: 8px; border-left: 5px solid #2A5290; margin-bottom: 20px;">

                <b>17點挑戰規則：</b> 創業資金有限！以下拉桿分數加總，外加提供插座(算1分)與不限時福利(算1分)，最高不能超過 17 分！

            </div>

        """, unsafe_allow_html=True)

        

        g2_city = st.selectbox("選擇本次競賽挑戰城市", ["changhua", "taichung", "kaohsiung"], format_func=lambda x: "彰化核心商圈" if x=="changhua" else "台中精華商圈" if x=="taichung" else "高雄三多商圈", key="g2_city_select")

        

        col5, col6 = st.columns(2)

        with col5:

            g2_wifi = st.slider("投資 WiFi 穩定度", 1, 5, 1, key="g2_slider_w")

            g2_quiet = st.slider("投資 環境安靜度", 1, 5, 1, key="g2_slider_q")

            g2_tasty = st.slider("投資 產品美味度", 1, 5, 1, key="g2_slider_t")

        with col6:

            g2_cheap = st.slider("投資 CP值與價格", 1, 5, 1, key="g2_slider_c")

            g2_music = st.slider("投資 音樂環境", 1, 5, 1, key="g2_slider_m")

        

        st.markdown("#### 加值策略配置")

        col7, col8 = st.columns(2)

        with col7:

            g2_socket = st.radio("插座服務 (提供 = 1分)", ["不提供", "提供"], index=0, horizontal=True, key="g2_radio_s")

        with col8:

            g2_limit = st.radio("限時規定 (不限時 = 1分)", ["限時", "不限時"], index=0, horizontal=True, key="g2_radio_l")

            

        s_score = 1 if g2_socket == "提供" else 0

        l_score = 1 if g2_limit == "不限時" else 0

        total_points = g2_wifi + g2_quiet + g2_tasty + g2_cheap + g2_music + s_score + l_score

        

        st.markdown("<br>", unsafe_allow_html=True)

        

        if total_points > 17:

            st.error(f"預算爆表！目前已使用：{total_points} / 17 分（請調低分數以符合競賽規範）")

        else:

            st.success(f"預算安全！目前已使用：{total_points} / 17 分（尚餘 {17 - total_points} 分）")

        st.progress(min(1.0, total_points / 17))

        st.markdown("<br>", unsafe_allow_html=True)

        

        _, g2_btn_col, _ = st.columns([1, 1, 1])

        with g2_btn_col:

            g2_click = st.button("送交 AI 進行賽果評定", key="g2_submit_btn", use_container_width=True)

            

        if g2_click:

            if total_points > 17:

                st.error("資金超支！無法開店，請調整配置。")

            else:

                s_val = s_score

                l_val = 1 if g2_limit == "限時" else 0

                prob = get_prediction(g2_city, g2_wifi, g2_quiet, g2_tasty, g2_cheap, g2_music, s_val, l_val)

                

                st.markdown("---")

                st.metric(label="最終經營挑戰賽得分", value=f"{prob * 100:.2f}%")

                

                if prob > 0.65:

                    st.balloons()

                    st.success("神級鐵桿經理人！妳用有限的 17 分預算，精準切中商圈痛點，完美通關！")

                elif prob > 0.45:

                    st.success("精明創業家！很不錯！預算控制得當，店裡生意興隆，穩穩賺大錢！")

                else:

                    st.warning("決策失誤！可惜！配置雖然沒超支，但無法吸引該城市的目標客群，再換個配方試試看！")

                    

        st.markdown("</div>", unsafe_allow_html=True)
