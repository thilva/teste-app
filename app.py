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
                # 1. URL limpa e isolada (Usando a API v1beta do Gemini 2.5 Flash)
                # Garanta que a sua chave entra estritamente após o '?key='
                url = "https://googleapis.com"
                params = {"key": api_key}
                
                # 2. Estrutura de dados para o modelo
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente esportivo em tempo real. Forneça as informações esportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                        }]
                    }]
                }
                
                # 3. Envio da requisição separando os parâmetros da URL para evitar erros de colagem
                response = requests.post(url, params=params, json=payload)
                data = response.json()
                
                # 4. Tratamento da resposta
                if response.status_code == 200:
                    # Coleta o texto de dentro da estrutura correta da Google
                    texto_resposta = data['candidates'][0]['content']['parts'][0]['text']
                    st.subheader("📊 Resultados Encontrados:")
                    st.markdown(texto_resposta)
                else:
                    erro_msg = data.get('error', {}).get('message', 'Erro desconhecido')
                    st.error(f"Erro da API do Google ({response.status_code}): {erro_msg}")
                    
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
