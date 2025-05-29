import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

# --- 비밀번호 설정 ---
PASSWORD = "6313a"  # 여기에 원하는 비밀번호 입력하세요

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")
else:
    st.title("🗨️ 비밀번호 보호된 실시간 채팅 (2초 자동 새로고침)")

    chat_file = "shared_chat.txt"

    # 2초마다 새로고침
    st_autorefresh(interval=1000, key="refresh")

    # 사용자 이름 입력 (친구들과 구분하려고)
    user_name = st.text_input("사용자 이름을 입력하세요", "")

    # 메시지 입력
    message = st.text_input("메시지를 입력하세요")

    if st.button("전송"):
        if not user_name.strip():
            st.warning("사용자 이름을 입력해주세요!")
        elif message.strip():
            with open(chat_file, "a", encoding="utf-8") as f:
                f.write(f"{user_name}: {message}\n")
            st.experimental_rerun()

    # 채팅 내용 읽어오기
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            chat_history = f.read()
    else:
        chat_history = "아직 채팅 내용이 없습니다."

    st.text_area("채팅 내역", value=chat_history, height=400)