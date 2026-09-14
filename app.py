import streamlit as st
import requests

# Configuração da página do Streamlit
st.set_page_config(page_title="Resultados Desportivos Ao Vivo", page_icon="⚽", layout="wide")

st.title("⚽ Busca de Informações Desportivas em Tempo Real")
st.write("Obtenha os resultados, jogos e notícias desportivas mais recentes com o Gemini.")

# Entrada da Chave de API (Começando com AQ...)
api_key = st.text_input("Insira a sua Chave de API do Google AI (prefixo AQ...):", type="password")

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
                # Remove espaços em branco invisíveis
                entrada_chave = api_key.strip()
                
                # SEgurança Máxima: Se colou a URL inteira por engano, extrai apenas o que vem após o '?key='
                if "?key=" in entrada_chave:
                    chave_limpa = entrada_chave.split("?key=")[-1]
                elif "googleapis.com" in entrada_chave:
                    # Remove o domínio antigo se ele estiver colado antes da chave AQ...
                    chave_limpa = entrada_chave.replace("googleapis.com", "")
                else:
                    chave_limpa = entrada_chave
                
                url_completa = f"https://googleapis.com{chave_limpa}"
                
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
                    
                    # Correção e navegação segura pelos índices [0] das listas da API do Gemini
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
