import streamlit as st
import requests
import os

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Acompanhamento de Objetivos", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

# --- AUTH ---
with st.sidebar:
    if not st.session_state.token:
        st.header("Login")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        print(f"DEBUG - Token atual: {st.session_state.token}")
        if st.button("Entrar"):
            res = requests.post(f"{API_URL}/auth/login", json={"username": u, "password": p})
            print(f"DEBUG - Status code: {res.status_code}")
            print(f"DEBUG - Response: {res.text}")
            if res.status_code == 200:
                st.session_state.token = res.json()["token"]
                st.rerun()
            else: st.error("Erro ao logar")
    else:
        st.success("Logado")
        if st.button("Sair"):
            st.session_state.token = None
            st.rerun()

# --- INTERFACE CRUD ---
st.title("Acompanhamento de Objetivos")

if st.session_state.token:
    # FORMULÁRIO DE CRIAÇÃO
    with st.expander("Novo Registro"):
        c1, c2, c3, c4, c5 = st.columns(5)
        tit = c1.text_input("Objetivo")
        desc = c2.text_input("Descrição")
        data_inicio = c3.date_input('Data de início')
        prazo = c4.number_input('Prazo em dias')
        data_fim = c5.date_input('Data de fim') # this must be a read-only date field calculated by adding the prazo to data_inicio

        if st.button("Salvar Objetivo"):
            requests.post(f"{API_URL}/objetivos", json={
                "titulo": tit,
                "descricao": desc,
                'data de inicio': data_inicio.isoformat() if data_inicio else None,
                'prazo': prazo,
                'data de termino': data_fim.isoformat() if data_fim else None
            })
            st.toast("Objetivo adicionado!")
            st.rerun()

    # LISTAGEM E AÇÕES
    objetivos = requests.get(f"{API_URL}/objetivos").json()
    for l in objetivos:
        with st.container(border=True):
            col_info, col_del = st.columns([4, 1])
            col_info.write(f"**{l['titulo']}**")
            col_info.write(f"{l['descricao']}")
            if l.get('data de inicio'):
                col_info.write(f"Data de início: {l['data de inicio']}")
            if l.get('prazo'):
                col_info.write(f"Prazo em dias: {l['prazo']}")
            if l.get('data de termino'):
                col_info.write(f"Data de término: {l['data de termino']}")
            if col_del.button("Excluir", key=f"del_{l['id']}"):
                requests.delete(f"{API_URL}/objetivos/{l['id']}")
                st.rerun()
else:
    st.info("Acesse com seu usuário para gerenciar os objetivos.")
