import streamlit as st
from groq import Groq

# Configuração inicial da página
st.set_page_config(
    page_title="Studio ArchViz — Motor de Prompts",
    page_icon="🏛️",
    layout="wide"
)

# Estilização visual minimalista
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1rem; color: #64748B; margin-bottom: 2rem; }
    .stTextArea textarea { font-family: 'Courier New', monospace; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 1. AUTENTICAÇÃO SEGURA VIA STREAMLIT SECRETS
# -----------------------------------------------------------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ ERRO DE CONFIGURAÇÃO: A chave 'GROQ_API_KEY' não foi encontrada nos Secrets do Streamlit.")
    st.info("Adiciona a chave no painel do Streamlit Cloud em Settings > Secrets.")
    st.stop()

# -----------------------------------------------------------------------------
# 2. BIBLIOTECA DE PROMPTS BASE (PORTUGUÊS DE PORTUGAL)
# -----------------------------------------------------------------------------
st.sidebar.title("📚 Biblioteca de Prompts Base")
st.sidebar.markdown("Copia estes modelos predefinidos para realizar a análise no Gemini ou parametrizar o resultado.")

PROMPT_ANALISE_RIGOROSA = """Atua como Fotógrafo Principal de Arquitetura e Diretor Técnico de ArchViz. Realiza uma análise arquitetónica meticulosa e ultra-detalhada desta imagem para criar uma base estrutural inalterável.

Analisa e especifica os seguintes parâmetros em termos técnicos de arquitetura (em inglês):

1. ESPECIFICAÇÕES DE CÂMARA E BLOQUEIO DE PERSPETIVA:
   - Altura da câmara (nível dos olhos, drone, ângulo baixo).
   - Características da lente (ex.: lente tilt-shift de 24mm, zero distorção vertical).
   - Geometria da perspetiva (1 ponto, 2 pontos ou 3 pontos de fuga).
   - Posicionamento da linha do horizonte e limites do enquadramento.

2. VOLUMETRIA, MASSAS E GEOMETRIA:
   - Volumes geométricos primários e secundários, consolas, recuos e número de pisos.
   - Grelha estrutural exata, alinhamento de pilares e paredes mestras.
   - Geometria da cobertura (plana, inclinada, borboleta, cobertura vegetal, palas).
   - Padrões de fenestração: Proporção vidro/parede, perfis de caixilharia, fachadas cortina.

3. CONTEXTO E ENVOLVENTE:
   - Topografia do terreno, vegetação imediata, pavimentos e afastamentos aos limites.
   - Azimute solar, elevação, orientação das sombras e qualidade da luz natural (ex.: luz solar direta 5500K, nublado suave, crepúsculo).

4. MAPEAMENTO DE MATERIAIS EXISTENTES:
   - Identifica cada acabamento de superfície: revestimentos de fachada, especificações de vidros, aço estrutural, textura de betão, estereotomia de pavimentos.

Fornece uma descrição técnica denso-estrutural focada em preservar todas as coordenadas geométricas para reconstrução exata."""

st.sidebar.subheader("1. Prompt de Análise de Imagem (Gemini)")
st.sidebar.text_area("Copia este prompt para enviar ao Gemini com a foto original:", value=PROMPT_ANALISE_RIGOROSA, height=240)

st.sidebar.divider()

# -----------------------------------------------------------------------------
# 3. INTERFACE PRINCIPAL DA APLICAÇÃO
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🏛️ Studio ArchViz — Motor de Prompts</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ferramenta de alta precisão para manter a geometria original do imóvel e aplicar novos materiais e acabamentos.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Descrição Geométrica da Imagem Original")
    descricao_original = st.text_area(
        "Cola a análise técnica obtida na Fase 1 (do Gemini):",
        height=220,
        placeholder="Exemplo: A two-story minimalist residence shot with a 24mm tilt-shift lens in 2-point perspective. The building features a ground-floor cantilevered volume over a recessed glass curtain wall..."
    )

with col2:
    st.subheader("2. Modificações de Materiais & Design")
    novas_alteracoes = st.text_area(
        "Especifica os novos materiais, iluminação e acabamentos pretendidos:",
        height=220,
        placeholder="Exemplo: Substituir o acabamento de betão por ripas verticais de madeira Shou Sugi Ban (madeira queimada), alterar os caixilhos para alumínio anodizado bronze escuro, aplicar iluminação de acentuação 2700K sob as palas..."
    )

# Opções de afinação técnica
st.subheader("3. Parâmetros de Controlo ArchViz")
c1, c2, c3 = st.columns(3)
with c1:
    estilo_render = st.selectbox("Estilo Visual / Iluminação:", [
        "Luz do Dia Fotorrealista (Luz Natural 5500K)",
        "Golden Hour / Atmosfera de Pôr do Sol (Luz Quente 3000K)",
        "Blue Hour Crepúsculo Arquitetónico (Contraste LED Interior)",
        "Luz Nublada Suave de Estúdio (Sombras Neutras)"
    ])
with c2:
    rigidez_geometria = st.select_slider("Rigor de Preservação Estrutural:", options=["Elevado", "Bloqueio Estrito (Recomendado)", "Ancoragem Geométrica ao Pixel"])
with c3:
    qualidade_motor = st.selectbox("Motor de Render / Detalhe:", [
        "Unreal Engine 5.4 ArchViz / Path Tracing",
        "Fotografia Profissional Hasselblad H6D-100c",
        "V-Ray 6 Fotorrealismo / Materiais PBR"
    ])

# -----------------------------------------------------------------------------
# 4. ENGENHARIA DE PROMPTS DO GROQ (SISTEMA DE FUSÃO)
# -----------------------------------------------------------------------------
SYSTEM_PROMPT_ENGINE = f"""
És o Engenheiro Principal de Prompts de Arquitetura e ArchViz do mundo. O teu único objetivo é construir um prompt final expandido, ultra-detalhado e técnico em INGLÊS.

O prompt gerado DEVE FORÇAR os geradores de imagem de IA (Gemini, Midjourney v6, Stable Diffusion XL) a manter um BLOQUEIO ESTRUTURAL RÍGIDO na imagem de referência original, alterando APENAS os materiais de superfície, texturas e iluminação especificados.

ESTRUTURA OBRIGATÓRIA DO PROMPT GERADO (DEVOLVE APENAS O PROMPT FINAL EM INGLÊS):

SECÇÃO 1: BLOQUEIO RÍGIDO DE GEOMETRIA E CÂMARA (INÍCIO OBRIGATÓRIO)
- Escreve um comando explícito de preservação: "STRICT REFERENCE LOCK: Preserve 100% of the reference image's architectural geometry, building massing, spatial layout, 2-point perspective, camera focal length (24mm tilt-shift), horizon line, and exact structural outline. Do not alter building dimensions, window placements, or volume boundaries."

SECÇÃO 2: RECONSTRUÇÃO DA BASE ESTRUTURAL
- Integra a descrição técnica fornecida pelo utilizador, reforçando os elementos estruturais principais, níveis dos pisos e alinhamentos.

SECÇÃO 3: TRANSFORMAÇÃO TÉCNICA DE MATERIAIS
- Traduz os pedidos de alteração do utilizador em especificações precisas de materiais ArchViz PBR (Physically Based Rendering):
  * Especifica os tipos exatos de materiais (ex.: "charred Shou Sugi Ban timber cladding with visible char grain", "honed architectural white concrete", "low-iron ultra-clear triple-glazed glass").
  * Detalha caixilharia, juntas de dilatação e transições entre materiais.

SECÇÃO 4: MOTOR DE ILUMINAÇÃO E ATMOSFERA
- Aplica o estilo selecionado: {estilo_render}.
- Detalha a iluminação global, oclusão ambiental, reflexos ray-traced, rebatimento de luz e temperatura de cor (Kelvin).

SECÇÃO 5: PARÂMETROS DE PRODUÇÃO ARCHVIZ
- Motor selecionado: {qualidade_motor}.
- Finaliza com termos de qualidade: "Architectural Digest featured project, 8k resolution, razor-sharp focus, architectural photorealism, perfectly vertical architectural lines, PBR material maps, zero structural deviation."

Gera um bloco único de texto contínuo, sem introduções nem conclusões conversacionais.
"""

if st.button("🚀 Gerar Master Prompt de Transformação", type="primary"):
    if not descricao_original or not novas_alteracoes:
        st.warning("Preenche a descrição original e as alterações pretendidas antes de gerar.")
    else:
        with st.spinner("A sintetizar o Master Prompt no Groq..."):
            prompt_input = f"GEOMETRIA BASE:\n{descricao_original}\n\nALTERAÇÕES SOLICITADAS:\n{novas_alteracoes}"
            
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_ENGINE},
                    {"role": "user", "content": prompt_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.15,
            )
            
            master_prompt = completion.choices[0].message.content
            
            st.success("Master Prompt Gerado com Sucesso!")
            st.text_area(
                "Copia o Master Prompt abaixo. No Gemini, anexa a foto original e cola este texto:",
                value=master_prompt,
                height=280
            )
