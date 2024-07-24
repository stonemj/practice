import streamlit as st
import openai
import time

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit 앱 제목
st.title("AI 어시스턴트 챗봇")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력 받기
user_input = st.text_input("메시지를 입력하세요:")

# 메시지 전송 버튼
if st.button("전송"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 새로운 스레드 생성
    thread = openai.beta.threads.create()

    # 메시지 추가
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # 실행 생성
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_kSpI6lSV52HpMJczFXXPuGyT"
    )

    # 실행 완료 대기
    while run.status != "completed":
        time.sleep(1)
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # 메시지 검색
    messages = openai.beta.threads.messages.list(thread_id=thread.id)

    # AI 응답 추가
    ai_response = messages.data[0].content[0].text.value
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 대화 내용 표시
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("사용자:", value=message["content"], height=50, disabled=True)
    else:
        st.text_area("AI:", value=message["content"], height=50, disabled=True)