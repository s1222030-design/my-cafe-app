import streamlit as st
import joblib
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(page_title="AI Cafe Tycoon", page_icon="☕", layout="wide")

# 2. 終極 CSS 注入：鎖定海軍藍與奶油白背景，並完美修正元件不見的問題
st.markdown("""
    <style>
    /* 全域背景色鎖定為指定的奶油白 */
    .stApp, .main { 
        background-color: #F7F5F2 !important; 
    }
    
    /* 移除 Streamlit tabs 預設產生的白色大底座與外框（改由卡片承載內容） */
    div[data-baseweb="tab-panel"] {
        background-color: transparent !important;
        border: none !important;
    }
    div[data-testid="stTab"] {
        background-color: transparent !important;
    }
    
    /* 頁籤選取狀態顏色 */
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2A5290 !important;
        border-bottom-color: #2A5290 !important;
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
    
    /* 高級海軍藍按鈕本體美化 */
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
    
    /* 確保按鈕內部的 Streamlit 文字元件也強制繼承 #F7F5F2 */
    .stButton > button p {
        color: #F7F5F2 !important;
    }
    .stButton > button:hover p {
        color: #ffffff !important;
    }
    
    /* 修正後的純白高質感卡片框（確保內部元件與字體100%渲染） */
    .game-card {
        background-color: #ffffff !important;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #eedece;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 初始化控制封面的 Session State
if 'game_started'
