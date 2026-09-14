import streamlit as st
import requests

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

if st.button("Buscar Informações"):
    if not api_key:
        st.error("Por favor, insira a sua Chave de API para continuar.")
    elif not query:
        st.warning("Por favor, digite o que deseja procurar.")
    else:
        with st.spinner("A processar as informações desportivas mais recentes..."):
             try:
                # Isolamos completamente o endereço para o Python nunca juntar as palavras
                url_base = "https://googleapis.com"
                
                # Remove espaços em branco que possam vir na chave por engano
                chave_limpa = api_key.strip()
                
                url_completa = f"{url_base}?key={chave_limpa}"
                
                # Estrutura de dados exata exigida pelo Gemini
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Você é um assistente desportivo em tempo real. Forneça as informações desportivas mais recentes, resultados ao vivo e dados atualizados de hoje sobre: {query}"
                        }]
                    }]
                }
                
                # Envio da requisição
                response = requests.post(url_completa, json=payload)
                
                if response.status_code != 200:
                    st.error(f"Erro da API do Google (Código {response.status_code})")
                    st.text(f"Detalhes do erro do servidor:\n{response.text}")
                else:
                    data = response.json()
                    
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]  # Correção do índice da lista
                        if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                            texto_resposta = candidate['content']['parts'][0]['text']  # Correção do índice da lista
                            st.subheader("📊 Resultados Encontrados:")
                            st.markdown(texto_resposta)
                        else:
                            st.warning("A estrutura de conteúdo esperada não foi encontrada na resposta.")
                    else:
                        st.warning("Nenhum resultado foi retornado pelo modelo para esta pesquisa.")
                        
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar a requisição: {e}")
