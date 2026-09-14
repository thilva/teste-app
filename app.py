import streamlit as st
from google import genai
from google.genai import types

# Configuração da página do Streamlit
st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados, jogos e notícias desportivas mais recentes com o Gemini.")

# Entrada da Chave de API (Começando com AQ...)
api_key = st.text_input("AQ.Ab8RN6LRVXTnfUKdoTqVNbE1FA1T-AFq2gPfiQzNnmUBZuSAMA", type="password")

# Entrada da pesquisa do utilizador
query = st.text_input(
    "O que deseja procurar?", 
    placeholder="Ex: Resultados dos jogos da Champions League de hoje"
)

import requests  # Certifique-se de que este import está no topo ou use aqui

if st.button("Buscar Informações"):
    if not api_key:
        st.error("Por favor, insira a sua Chave de API para continuar.")
    elif not query:
        st.warning("Por favor, digite o que deseja procurar.")
    else:
        with st.spinner("A processar as informações desportivas mais recentes..."):
            try:
                # 1. URL e parâmetros isolados
                url = "https://googleapis.com"
                params = {"key": api_key}
                
                # 2. Estrutura de dados exata exigida pelo Gemini
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente esportivo em tempo real. Forneça as informações esportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                        }]
                    }]
                }
                
                # 3. Envio da requisição
                response = requests.post(url, params=params, json=payload)
                
                # PROTEÇÃO: Se não for 200, exibe o texto bruto do erro antes de tentar converter para JSON
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes do erro do servidor:\n{response.text}")
                else:
                    data = response.json()
                    # CORREÇÃO DA EXTRAÇÃO: Acessando os índices corretos [0] da lista da API
                    texto_resposta = data['candidates'][0]['content']['parts'][0]['text']
                    st.subheader("📊 Resultados Encontrados:")
                    st.markdown(texto_resposta)
                    
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
