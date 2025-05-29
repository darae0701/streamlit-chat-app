import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

PASSWORD = "1231"
CHAT_FILE = "shared_chat.txt"

def login_page():
    st.title("🔐 로그인")

    user_name = st.text_input("사용자 이름을 입력하세요", key="username")
    pwd = st.text_input("비밀번호를 입력하세요", type="password", key="password")

    if st.button("로그인"):
        if pwd == PASSWORD and user_name.strip():
            st.session_state.authenticated = True
            st.session_state.user_name = user_name.strip()
            st.experimental_rerun()
        else:
            st.error("비밀번호가 틀리거나 이름을 입력하지 않았습니다.")

def chat_page():
    st.title("💬 실시간 채팅 (2초 자동 새로고침)")

    st_autorefresh(interval=2000, key="autorefresh")

    st.write(f"👤 **{st.session_state.user_name}**님, 환영합니다!")

    msg = st.text_input("메시지를 입력하세요", key="msg_input")

    if st.button("전송"):
        if msg.strip():
            with open(CHAT_FILE, "a", encoding="utf-8") as f:
                f.write(f"{st.session_state.user_name}: {msg.strip()}\n")
            st.experimental_rerun()
        else:
            st.warning("메시지를 입력해주세요.")

    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            chat_history = f.read()
    else:
        chat_history = "아직 채팅 내용이 없습니다."

    st.text_area("📜 채팅 내역", value=chat_history, height=400, key="chat_area", disabled=True)

    if st.button("초기화"):
        if os.path.exists(CHAT_FILE):
            os.remove(CHAT_FILE)
        st.experimental_rerun()

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if not st.session_state.authenticated:
        login_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()