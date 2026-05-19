import streamlit as st
import requests
import os
from datetime import timedelta, date

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
        prazo = c4.number_input('Prazo em dias', min_value=0, value=0, step=1)
        data_fim_calculada = (data_inicio + timedelta(days=prazo)) if data_inicio else None
        data_fim = c5.date_input('Data de fim', value=data_fim_calculada, disabled=True)

        if st.button("Salvar Objetivo"):
            requests.post(f"{API_URL}/objetivos", json={
                "titulo": tit,
                "descricao": desc,
                'data_inicio': data_inicio.isoformat() if data_inicio else None,
                'prazo_dias': prazo,
                'data_fim': data_fim.isoformat() if data_fim else None
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
            if l.get('data_inicio'):
                col_info.write(f"Data de início: {l['data_inicio']}")
            if l.get('prazo_dias'):
                col_info.write(f"Prazo em dias: {l['prazo_dias']}")
            if l.get('data_fim'):
                col_info.write(f"Data de término: {l['data_fim']}")
            if col_del.button("Excluir", key=f"del_{l['id']}"):
                requests.delete(f"{API_URL}/objetivos/{l['id']}")
                st.rerun()

            with st.expander("Editar Objetivo"):
                ec1, ec2, ec3, ec4, ec5 = st.columns(5)
                edit_tit = ec1.text_input("Objetivo", value=l['titulo'], key=f"edit_tit_{l['id']}")
                edit_desc = ec2.text_input("Descrição", value=l['descricao'], key=f"edit_desc_{l['id']}")
                
                init_val_data = date.fromisoformat(l['data_inicio']) if l.get('data_inicio') else date.today()
                init_val_prazo = int(l['prazo_dias']) if l.get('prazo_dias') else 0
                
                edit_data_inicio = ec3.date_input('Data de início', value=init_val_data, key=f"edit_start_{l['id']}")
                edit_prazo = ec4.number_input('Prazo em dias', min_value=0, value=init_val_prazo, step=1, key=f"edit_prazo_{l['id']}")
                
                edit_data_fim_calculada = (edit_data_inicio + timedelta(days=edit_prazo)) if edit_data_inicio else None
                ec5.date_input('Data de fim', value=edit_data_fim_calculada, disabled=True, key=f"edit_fim_{l['id']}")
                
                if st.button("Salvar Alterações", key=f"save_{l['id']}"):
                    requests.put(f"{API_URL}/objetivos/{l['id']}", json={
                        "titulo": edit_tit,
                        "descricao": edit_desc,
                        "data_inicio": edit_data_inicio.isoformat() if edit_data_inicio else None,
                        "prazo_dias": edit_prazo,
                        "data_fim": edit_data_fim_calculada.isoformat() if edit_data_fim_calculada else None
                    })
                    st.toast("Objetivo atualizado!")
                    st.rerun()
else:
    st.info("Acesse com seu usuário para gerenciar os objetivos.")
