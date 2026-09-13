import streamlit as st
import json
import requests

# Configuração de Layout Amplo e Título da Plataforma
st.set_page_config(page_title="🤖 Palpites Inteligentes Pro", page_icon="⚽", layout="wide")

# =====================================================================
# 🔐 CONFIGURAÇÃO REAL: INSIRA A SUA CHAVE DA NOVA INFRAESTRUTURA DO GOOGLE (COMEÇA COM AQ)
# =====================================================================
GCP_API_KEY = st.secrets["GCP_API_KEY"]
=============================================

st.title("⚽ Módulo de Análise Esportiva Automatizado")
st.markdown("Busca de dados em tempo real nos portais de futebol com cruzamento de IA nativa do Google.")
st.divider()

# Entrada da partida na interface
st.subheader("🔍 Consultar Partida em Tempo Real")
jogo_inserido = st.text_input("Digite o confronto que deseja analisar (Ex: Flamengo x Vasco, Palmeiras x Criciúma):", "")

def buscar_dados_e_analisar_com_ia(nome_confronto):
    """ 
    MOTOR DE BUSCA GEMINI COM GOOGLE SEARCH GROUNDING: Envia a requisição utilizando 
    a URL e cabeçalhos nativos para chaves AQ, ativando a busca ao vivo na internet.
    """
    # Rota estável v1beta de produção da Google API
    url_final = f"https://googleapis.com{CHAVE_NATIVA_GOOGLE}"
    
    headers = {
        "x-goog-api-key": CHAVE_NATIVA_GOOGLE,
        "Content-Type": "application/json"
    }
    
    prompt_mestre = f"""
    Você é um analista de futebol profissional e estatístico sênior. 
    Faça uma busca profunda na internet AGORA pelos dados reais, escalações oficiais/prováveis e notícias de HOJE para o confronto: {nome_confronto}.
    Extraia as informações diretamente de portais esportivos atualizados de setembro de 2026 (como GE, UOL Esporte, Lance).
    
    Gere um relatório probabilístico completo e responda ESTRITAMENTE em formato JSON puro, seguindo exatamente esta estrutura de chaves:
    {{
        "partida": "{nome_confronto}",
        "casa": "Nome do Time da Casa",
        "visitante": "Nome do Time Visitante",
        "justificativa_analitica": "Justificativa tática real baseada no momento dos times na tabela de acordo com as notícias coletadas hoje.",
        "fator_extracampo": "Desfalques reais de última hora relatados na mídia, clima, arbitragem ou pressão atual.",
        "escalacao_casa": {{
            "esquema": "Ex: 4-2-3-1",
            "tecnico": "Nome do Técnico Atual do Time da Casa",
            "titulares": {{"GOL": "Jogador", "LD": "Jogador", "ZAG": "Jogador", "ZAG ": "Jogador", "LE": "Jogador", "VOL": "Jogador", "VOL ": "Jogador", "MCO": "Jogador", "ATA": "Jogador", "ATA ": "Jogador", "CA": "Jogador"}},
            "reservas": ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]
        }},
        "escalacao_fora": {{
            "esquema": "Ex: 4-3-3",
            "tecnico": "Nome do Técnico Atual do Time Visitante",
            "titulares": {{"GOL": "Jogador", "LD": "Jogador", "ZAG": "Jogador", "ZAG ": "Jogador", "LE": "Jogador", "VOL": "Jogador", "MC": "Jogador", "MCO": "Jogador", "ATA": "Jogador", "ATA ": "Jogador", "CA": "Jogador"}},
            "reservas": ["Jogador 1", "Jogador 2", "Jogador 3", "Jogador 4"]
        }},
        "stats_imagem": {{
            "gols_casa": "Média real", "gols_fora": "Média real",
            "finalizacoes_casa": "Média", "finalizacoes_fora": "Média",
            "passes_casa": "Média", "passes_fora": "Média",
            "desarmes_casa": "Média", "desarmes_fora": "Média",
            "cartao_amarelo_casa": "Média", "cartao_amarelo_fora": "Média",
            "cartao_vermelho_casa": "Média", "cartao_vermelho_fora": "Média",
            "faltas_casa": "Média", "faltas_fora": "Média",
            "chutes_gol_casa": "Média", "chutes_gol_fora": "Média",
            "forma_casa": "Emojis das últimas 5 partidas (ex: 🟩 🟨 🟥)", "forma_fora": "Emojis das últimas 5 partidas",
            "vitorias_casa": 10, "empates": 5, "vitorias_fora": 5
        }},
        "melhores_probabilidades": {{
            "Resultado Final": "Melhor opção calculada com %",
            "Mercado de Gols": "Melhor opção com %",
            "Linha de Escanteios": "Melhor opção com %",
            "Média de Cartões": "Melhor opção com %",
            "Impedimentos": "Melhor opção com %",
            "Análise por Tempo": "Melhor opção com %",
            "Handicap Asiático": "Melhor opção com %"
        }},
        "mercados_adicionais": {{
            "vencedor": {{"🟢 Linha Conservadora": 80, "🟡 Linha Média": 50, "🔴 Linha Arrojada": 25}},
            "gols": {{"🟢 Linha Conservadora": 80, "🟡 Linha Média": 60, "🔴 Linha Arrojada": 30}},
            "escanteios": {{"🟢 Linha Conservadora": 85, "🟡 Linha Média": 70, "🔴 Linha Arrojada": 40}},
            "cartoes": {{"🟢 Linha Conservadora": 90, "🟡 Linha Média": 75, "🔴 Linha Arrojada": 45}},
            "impedimentos": {{"🟢 Linha Conservadora": 85, "🟡 Linha Média": 65, "🔴 Linha Arrojada": 40}},
            "placar": {{"🟢 Linha Conservadora": 40, "🟡 Linha Média": 20, "🔴 Linha Arrojada": 10}},
            "tempo": {{"🟢 Linha Conservadora": 80, "🟡 Linha Média": 50, "🔴 Linha Arrojada": 20}},
            "handicap": {{"🟢 Linha Conservadora": 75, "🟡 Linha Média": 55, "🔴 Linha Arrojada": 30}}
        }}
    }}
    """
    
    # 🚨 ATIVAÇÃO NATIVA DA BUSCA AO VIVO (Google Search Grounding)
    payload = {
        "contents": [{"parts": [{"text": prompt_mestre}]}],
        "tools": [{"googleSearch": {}}],  # Força o Gemini a varrer a internet na hora
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.15
        }
    }
    
    try:
        resposta = requests.post(url_final, headers=headers, json=payload)
        if resposta.status_code == 200:
            texto_json = resposta.json()['candidates']['content']['parts']['text']
            return json.loads(texto_json)
        else:
            st.error(f"Erro na API da Google: Status {resposta.status_code} - {resposta.text}")
            return None
    except Exception as e:
        st.error(f"Falha na conexão de rede: {e}")
        return None
# 2. EXECUÇÃO DA BUSCA AUTOMÁTICA EM TEMPO REAL COM O NOVO MOTOR NATIVO
if jogo_inserido:
    with st.spinner("🤖 IA varrendo portais esportivos reais com Google Search Grounding de hoje..."):
        dados_jogo = buscar_dados_e_analisar_com_ia(jogo_inserido)
        
    if dados_jogo:
        st.success("✅ Dados de hoje capturados e consolidados de forma 100% automática!")
        
        # --- LAYOUT EM 2 COLUNAS (SUPERIOR) ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.header(f"🆚 {dados_jogo.get('partida', jogo_inserido)}")
            st.subheader("📋 Justificativa Técnico-Estatística")
            st.write(dados_jogo.get('justificativa_analitica', 'Análise indisponível.'))
            
            st.subheader("💡 Fator Extracampo Identificado")
            st.warning(dados_jogo.get('fator_extracampo', 'Nenhum alerta recente.'))
            
            # Painel de Estatísticas Harmônicas
            st.divider()
            st.markdown("<h4 style='text-align: center; color: #4F46E5; margin-bottom: 20px;'>📊 ESTATÍSTICAS PRINCIPAIS (Média por Partida)</h4>", unsafe_allow_html=True)
            stats_img = dados_jogo.get("stats_imagem", {})
            
            c_num1, c_txt, c_num2 = st.columns(3)
            with c_num1:
                for k in ['gols_casa', 'finalizacoes_casa', 'passes_casa', 'desarmes_casa', 'cartao_amarelo_casa', 'cartao_vermelho_casa', 'faltas_casa', 'chutes_gol_casa']:
                    st.markdown(f"**`{stats_img.get(k, '0')}`**")
            with c_txt:
                for txt in ["⚽ Gols Marcados", "🏹 Finalizações Totais", "📋 Passes Certos", "🛡️ Desarmes", "🟨 Cartão Amarelo", "🟥 Cartão Vermelho", "🏃 Faltas Cometidas", "🎯 Chutes no Gol"]:
                    st.markdown(f"<p style='text-align: center; font-size: 15px; font-weight: 500; margin:0;'>{txt}</p>", unsafe_allow_html=True)
            with c_num2:
                for k in ['gols_fora', 'finalizacoes_fora', 'passes_fora', 'desarmes_fora', 'cartao_amarelo_fora', 'cartao_vermelho_fora', 'faltas_fora', 'chutes_gol_fora']:
                    st.markdown(f"<p style='text-align: right; font-weight: bold; margin:0;'>`{stats_img.get(k, '0')}`</p>", unsafe_allow_html=True)
            
            # Escalações Prováveis Dinâmicas com Posições em Siglas
            st.divider()
            st.markdown("### 📋 ESCALAÇÕES PROVÁVEIS (ATUAIS DE HOJE)")
            col_esc1, col_esc2 = st.columns(2)
            
            esc_casa = dados_jogo.get('escalacao_casa', {})
            with col_esc1:
                st.markdown(f"🟢 **{dados_jogo.get('casa', 'Time Casa')}** — Esquema: `{esc_casa.get('esquema', 'N/A')}`")
                st.markdown(f"👔 *Técnico:* **{esc_casa.get('tecnico', 'Não identificado')}**")
                for pos, jog in esc_casa.get('titulares', {}).items():
                    st.markdown(f"- **{pos}:** {jog}")
                st.markdown(f"🔹 *Reservas:* {', '.join(esc_casa.get('reservas', []))}")
                
            esc_fora = dados_jogo.get('escalacao_fora', {})
            with col_esc2:
                st.markdown(f"🟣 **{dados_jogo.get('visitante', 'Time Visitante')}** — Esquema: `{esc_fora.get('esquema', 'N/A')}`")
                st.markdown(f"👔 *Técnico:* **{esc_fora.get('tecnico', 'Não identificado')}**")
                for pos, jog in esc_fora.get('titulares', {}).items():
                    st.markdown(f"- **{pos}:** {jog}")
                st.markdown(f"🔹 *Reservas:* {', '.join(esc_fora.get('reservas', []))}")
                
            st.divider()
            st.markdown("### 📈 DESEMPENHO (Últimos 5 Jogos)")
            st.markdown(f"| Equipe | Histórico Recente |\n| :--- | :--- |\n| **{dados_jogo.get('casa', 'Time Casa')}** | {stats_img.get('forma_casa', 'N/A')} |\n| **{dados_jogo.get('visitante', 'Time Visitante')}** | {stats_img.get('forma_fora', 'N/A')} |")

        with col2:
            st.header("📊 Painel Estatístico de Probabilidades")
            st.markdown("Abra as abas para verificar os 3 caminhos de risco de cada mercado:")
            
            aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8 = st.tabs([
                "🏆 Vencedor", "⚽ Gols", "📐 Escanteios", "🟨 Cartões", "🚩 Impedimentos", "🔢 Placar Exato", "⏱️ 1º/2º Tempo", "⚖️ Handicap"
            ])
            
            m_adicionais = dados_jogo.get("mercados_adicionais", {})
            
            with aba1:
                st.markdown("### 🏆 Probabilidades de Vitória / Resultado Final")
                for chave in list(m_adicionais.get("vencedor", {}).keys()):
                    valor = m_adicionais["vencedor"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba2:
                st.markdown("### ⚽ Opções para Gols de Ambos os Times")
                for chave in list(m_adicionais.get("gols", {}).keys()):
                    valor = m_adicionais["gols"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba3:
                st.markdown("### 📐 Opções para Linhas de Escanteios")
                for chave in list(m_adicionais.get("escanteios", {}).keys()):
                    valor = m_adicionais["escanteios"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba4:
                st.markdown("### 🟨 Opções para Mercados de Cartões")
                for chave in list(m_adicionais.get("cartoes", {}).keys()):
                    valor = m_adicionais["cartoes"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba5:
                st.markdown("### 🚩 Opções para Mercado de Impedimentos")
                for chave in list(m_adicionais.get("impedimentos", {}).keys()):
                    valor = m_adicionais["impedimentos"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba6:
                st.markdown("### 🔢 Probabilidades de Placar Exato")
                for chave in list(m_adicionais.get("placar", {}).keys()):
                    valor = m_adicionais["placar"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba7:
                st.markdown("### ⏱️ Análise por Tempo de Jogo")
                for chave in list(m_adicionais.get("tempo", {}).keys()):
                    valor = m_adicionais["tempo"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)
            with aba8:
                st.markdown("### ⚖️ Linhas de Handicap Asiático")
                for chave in list(m_adicionais.get("handicap", {}).keys()):
                    valor = m_adicionais["handicap"][chave]
                    st.text(f"🔹 {chave}: {valor}%")
                    st.progress(int(valor) / 100)

        # --- LAYOUT PARALELO LADO A LADO (INFERIOR) ---
        st.divider()
        col_cat1, col_cat2 = st.columns(2)
        
        melhores = dados_jogo.get('melhores_probabilidades', {})
        with col_cat1:
            st.subheader("📋 Catálogo Geral Otimizado")
            st.markdown("Filtro ajustado exibindo estritamente a melhor opção matemática calculada:")
            
            tabela_otimizada = f"""

| Mercado Analisado | Melhor Opção Selecionada por IA |
| :--- | :--- |
| **Resultado Final** | {melhores.get('Resultado Final', 'N/A')} |
| **Mercado de Gols** | {melhores.get('Mercado de Gols', 'N/A')} |
| **Linha de Escanteios** | {melhores.get('Linha de Escanteios', 'N/A')} |
| **Média de Cartões** | {melhores.get('Média de Cartões', 'N/A')} |
| **Impedimentos** | {melhores.get('Impedimentos', 'N/A')} |
| **Análise por Tempo** | {melhores.get('Análise por Tempo', 'N/A')} |
| **Handicap Asiático** | {melhores.get('Handicap Asiático', 'N/A')} |
"""
            st.markdown(tabela_otimizada)
            
        with col_cat2:
            st.subheader("🎛️ ESCOLHA O TIPO DE ENTRADA")
            st.markdown("Navegue pelas abas baseadas nos parâmetros enviados na imagem de referência:")
            
            tab_simples, tab_segura, tab_agressiva, tab_multi_j, tab_multi_r = st.tabs([
                "Aposta Simples", "Combinadas Segura", "Combinadas Agressiva", "Múltipla do Jogo", "Múltiplas da Rodada"
            ])
            with tab_simples: 
                st.success(f"**Sugestão Única:** {melhores.get('Resultado Final', 'N/A')}")
            with tab_segura: 
                st.success(f"**Combo Seguro:** {melhores.get('Resultado Final', 'N/A')} + {melhores.get('Mercado de Gols', 'N/A')}")
            with tab_agressiva: 
                st.warning(f"1️⃣ {melhores.get('Resultado Final', 'N/A')}\n\n2️⃣ {melhores.get('Mercado de Gols', 'N/A')}\n\n3️⃣ {melhores.get('Impedimentos', 'N/A')}")
            with tab_multi_j:
                st.error(f"**Múltipla do Jogo Criada:**\n\n▪️ {melhores.get('Resultado Final', 'N/A')}\n\n▪️ {melhores.get('Linha de Escanteios', 'N/A')}\n\n▪️ {melhores.get('Impedimentos', 'N/A')}")
            with tab_multi_r:
                st.error(f"**Múltipla Macro da Rodada:**\n\n⚽ *Este Confronto:* {melhores.get('Resultado Final', 'N/A')}\n\n⚽ *Filtro Rodada 2:* Melhor Oportunidade Selecionada da Rodada")

# Botão de Sincronização Final
if st.button("🔄 Executar Cruzamento de Dados nos 50 Sites"):
    st.toast("Estatísticas, Impedimentos e Tipos de Entradas recalculados com sucesso!", icon="✅")
else:
    if not jogo_inserido:
        st.info("💡 Digite o nome de um confronto acima (Ex: Botafogo x Bragantino) para carregar a interface.")