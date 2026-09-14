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
                # CORREÇÃO DEFINITIVA DA URL: Montamos a string de forma direta e unificada
                # Isso impede o servidor do Google de redirecionar a chamada para a página inicial '/'
                url_completa = f"https://googleapis.com{api_key}"
                
                # 2. Estrutura de dados exata exigida pelo Gemini
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente esportivo em tempo real. Forneça as informações esportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                        }]
                    }]
                }
                
                # 3. Envio da requisição direta usando apenas a URL unificada
                response = requests.post(url_completa, json=payload)
                
                # PROTEÇÃO: Verifica se o servidor aceitou a chamada antes de tratar o JSON
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes do erro do servidor:\n{response.text}")
                else:
                    data = response.json()
                    
                    # Navegação segura pelos índices da lista da resposta oficial do Gemini
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                            texto_resposta = candidate['content']['parts'][0]['text']
                            st.subheader("📊 Resultados Encontrados:")
                            st.markdown(texto_resposta)
                        else:
                            st.warning("A estrutura de conteúdo esperada não foi encontrada na resposta.")
                    else:
                        st.warning("Nenhum resultado foi retornado pelo modelo para esta pesquisa.")
                    
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
