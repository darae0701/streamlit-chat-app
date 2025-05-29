import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

PASSWORD = "6313a"

def login():
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
        return False
    return True

def chat_app():
    st.title("🗨️ 비밀번호 보호된 실시간 채팅 (2초 자동 새로고침)")

    chat_file = "shared_chat.txt"
    st_autorefresh(interval=2000, key="refresh")

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "message" not in st.session_state:
        st.session_state.message = ""

    st.session_state.user_name = st.text_input("사용자 이름을 입력하세요", st.session_state.user_name, key="user_name")
    st.session_state.message = st.text_input("메시지를 입력하세요", st.session_state.message, key="message")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("전송"):
            if not st.session_state.user_name.strip():
                st.warning("사용자 이름을 입력해주세요!")
            elif st.session_state.message.strip():
                with open(chat_file, "a", encoding="utf-8") as f:
                    f.write(f"{st.session_state.user_name}: {st.session_state.message}\n")
                st.experimental_rerun()  # 메시지 보낸 후에도 입력창 유지하려면 이 줄 없애도 됩니다.
    with col2:
        if st.button("입력창 비우기"):
            st.session_state.message = ""
            st.experimental_rerun()

    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            chat_history = f.read()
    else:
        chat_history = "아직 채팅 내용이 없습니다."

    st.text_area("채팅 내역", value=chat_history, height=400)

def main():
    if login():
        chat_app()

if __name__ == "__main__":
    main()