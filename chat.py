import streamlit as st
import time
import os
import json

CHAT_LOG_PATH = "chat_log.json"
PASSWORD = "1231"

# 파일 기반 채팅 기록 초기화
def clear_chat():
    with open(CHAT_LOG_PATH, "w") as f:
        json.dump([], f)

# 채팅 불러오기
def load_chat():
    if not os.path.exists(CHAT_LOG_PATH):
        clear_chat()
        with open(CHAT_LOG_PATH, "w") as f:
            f.write("[]")  # 빈 JSON 배열 저장 등
        return []
    with open(CHAT_LOG_PATH, "r") as f:
        data = f.read()
        return json.load(f)

# 채팅 저장
def save_chat(chat_data):
    with open(CHAT_LOG_PATH, "w") as f:
        json.dump(chat_data, f)

# 초기 로그인 단계
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 로그인")
    name = st.text_input("이름")
    password = st.text_input("비밀번호", type="password")

    if st.button("입장"):
        if password == PASSWORD and name:
            st.session_state.name = name
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸거나 이름이 비어 있습니다.")
    st.stop()

# 로그인 완료 후 채팅창 표시
st.title("💬 실시간 채팅방")

# 메시지 입력 후 자동 비우기
def submit_message():
    if st.session_state.msg.strip():
        chat = load_chat()
        chat.append({"name": st.session_state.name, "message": st.session_state.msg})
        save_chat(chat)
        st.session_state.msg = ""  # 입력창 비우기
        
# 채팅 초기화 버튼
if st.button("💣 초기화"):
    clear_chat()
    st.rerun()

# 채팅 메시지 입력
st.text_input("메시지 입력", key="msg", on_change=submit_message)

# 채팅창
st.markdown("---")
st.subheader("📜 채팅 로그")
chat_history = load_chat()
for entry in chat_history:
    st.markdown(f"**{entry['name']}**: {entry['message']}")

# 새로고침 (매초마다)
time.sleep(1)
st.rerun()