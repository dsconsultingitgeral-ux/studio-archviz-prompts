import streamlit as st
from groq import Groq

# Configuração da página no Streamlit
st.set_page_config(
    page_title="Studio ArchViz — Master Prompt Engine",
    page_icon="🏛️",
    layout="wide"
)

# Estilização visual customizada
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
    st.info("Adiciona a chave no ficheiro `.streamlit/secrets.toml` localmente ou no painel do Streamlit Cloud.")
    st.stop()

# -----------------------------------------------------------------------------
# 2. PROMPTS BASE ULTRA-DETALHADOS (GARDADOS NA APP)
# -----------------------------------------------------------------------------
st.sidebar.title("📚 Biblioteca de Prompts Base")
st.sidebar.markdown("Use estes modelos para extrair os dados da imagem original e parametrizar o resultado.")

PROMPT_ANALISE_RIGOROSA = """Act as a Senior Architectural Photographer and Lead ArchViz Technical Director. Perform a meticulous, hyper-detailed architectural analysis of this image to build an immutable structural base.

Analyze and specify the following parameters in dense, professional architectural terms (in English):

1. CAMERA SPECIFICATIONS & PERSPECTIVE LOCK:
   - Camera height (eye-level, drone, low angle).
   - Lens characteristics (e.g., 24mm tilt-shift architectural lens, zero vertical distortion).
   - Perspective geometry (1-point, 2-point, or 3-point perspective).
   - Horizon line placement, vanishing points, and frame boundary constraints.

2. VOLUMETRY, MASSING & GEOMETRY:
   - Primary and secondary geometric volumes, cantilevers, setbacks, and floor count.
   - Exact structural grid, structural column spacing, and load-bearing wall alignment.
   - Roofline geometry (flat, pitched, butterfly, green roof, overhang depths).
   - Fenestration patterns: Window-to-wall ratio, mullion profiles, curtain wall structures.

3. CONTEXT & ENVIRONMENT:
   - Surrounding landscape topography, immediate vegetation, ground cover, neighbor setbacks.
   - Sun azimuth, elevation angle, shadow orientation, and daylight quality (e.g., 5500K direct sunlight, soft overcast, twilight).

4. EXISTING MATERIAL MAPPING:
   - Identify every surface finish: facade cladding, glazing specifications, structural steel, concrete texture, paving joinery.

Provide a comprehensive, highly technical description focused on preserving every geometric coordinate for reconstruction."""

st.sidebar.subheader("1. Prompt de Análise de Imagem (Gemini)")
st.sidebar.text_area("Copia este prompt para enviar ao Gemini juntamente com a foto original:", value=PROMPT_ANALISE_RIGOROSA, height=220)

st.sidebar.divider()

# -----------------------------------------------------------------------------
# 3. INTERFACE PRINCIPAL DA APLICAÇÃO
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🏛️ Studio ArchViz — Master Prompt Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ferramenta de alta precisão para manter a geometria original do imóvel e aplicar novos materiais e acabamentos.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Descrição Geométrica da Imagem Original")
    descricao_original = st.text_area(
        "Cola a análise técnica obtida na Fase 1 (do Gemini):",
        height=220,
        placeholder="Ex: A two-story minimalist residence shot with a 24mm tilt-shift lens in 2-point perspective. The building features a ground-floor cantilevered volume over a recessed glass curtain wall..."
    )

with col2:
    st.subheader("2. Modificações de Materiais & Design")
    novas_alteracoes = st.text_area(
        "Especifica os novos materiais, iluminação e acabamentos pretendidos:",
        height=220,
        placeholder="Ex: Substituir o acabamento de betão por ripas verticais de madeira Shou Sugi Ban (madeira queimada), alterar os caixilhos para alumínio anonisado bronze escuro, aplicar iluminação de acentuação 2700K sob as palas..."
    )

# Opções de afinação técnica
st.subheader("3. Parâmetros de Controlo ArchViz")
c1, c2, c3 = st.columns(3)
with c1:
    estilo_render = st.selectbox("Estilo Visual / Iluminação:", [
        "Photorealistic Daylight (5500K Daylight)",
        "Golden Hour / Sunset Atmosphere (3000K Warm Light)",
        "Blue Hour Architectural Dusk (Interior LED contrast)",
        "Overcast Soft Studio Lighting (Neutral shadows)"
    ])
with c2:
    rigidez_geometria = st.select_slider("Rigor de Preservação Estrutural:", options=["Elevado", "Strict Locking (Recomendado)", "Pixel-level Geometry Anchor"])
with c3:
    qualidade_motor = st.selectbox("Motor de Render / Detalhe:", [
        "Unreal Engine 5.4 ArchViz / Path Tracing",
        "Hasselblad H6D-100c Medium Format Photography",
        "V-Ray 6 Photorealism / PBR Materials"
    ])

# -----------------------------------------------------------------------------
# 4. SYSTEM PROMPT DO GROQ (ENGENHARIA DE PROMPTS AVANÇADA)
# -----------------------------------------------------------------------------
SYSTEM_PROMPT_ENGINE = f"""
You are the World's Leading Architectural Visualization (ArchViz) Prompt Engineer. Your single objective is to construct an extended, hyper-detailed master image generation prompt in technical English.

The generated prompt MUST force AI image generators (Gemini, Midjourney v6, Stable Diffusion XL) to enforce a STRICT STRUCTURAL ANCHOR on the original building while replacing only the specified surface materials, textures, and lighting.

CRITICAL INSTRUCTION STRUCTURE (OUTPUT ONLY THE FINAL MASTER PROMPT):

SECTION 1: HARD GEOMETRY & CAMERA LOCK (MANDATORY START)
- Write an explicit command enforcing absolute structural preservation: "STRICT REFERENCE LOCK: Preserve 100% of the reference image's architectural geometry, building massing, spatial layout, 2-point perspective, camera focal length (24mm tilt-shift), horizon line, and exact structural outline. Do not alter building dimensions, window placements, or volume boundaries."

SECTION 2: DETAILED BASE RECONSTRUCTION
- Integrate the technical structural description provided by the user. Reinforce key load-bearing elements, floor levels, cantilevers, and structural grid alignment.

SECTION 3: HYPER-SPECIFIC MATERIAL TRANSFORMATIONS
- Translate user modification requests into precise ArchViz PBR (Physically Based Rendering) specifications:
  * Specify exact material grades (e.g., "charred Shou Sugi Ban timber cladding with visible char grain", "honed architectural white concrete with tight aggregate", "low-iron ultra-clear triple-glazed glass with subtle reflections").
  * Detail joinery, panel gaps, reveal lines, and material transitions.

SECTION 4: ATMOSPHERIC LIGHTING ENGINE & ENVIRONMENT
- Apply selected render style: {estilo_render}.
- Detail global illumination, ambient occlusion, ray-traced reflections, light bouncing, shadow falloff, and color temperature (Kelvin).

SECTION 5: HIGH-END ARCHVIZ PRODUCTION PARAMETERS
- Render Specs: {qualidade_motor}.
- Finish with key quality anchors: "Architectural Digest featured project, 8k resolution, razor-sharp focus, architectural photorealism, perfectly vertical architectural lines, PBR material maps, zero structural deviation."

Generate a seamless, comprehensive master prompt text block without markdown headers or intro text.
"""

if st.button("🚀 Gerar Master Prompt de Transformação", type="primary"):
    if not descricao_original or not novas_alteracoes:
        st.warning("Preenche a descrição original e as alterações pretendidas antes de gerar.")
    else:
        with st.spinner("A sintetizar o Master Prompt no Groq..."):
            prompt_input = f"BASE GEOMETRY:\n{descricao_original}\n\nTRANSFORMATIONS REQUESTED:\n{novas_alteracoes}"
            
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
                "Copia o Master Prompt abaixo. No Gemini, envia a foto original juntamente com este texto:",
                value=master_prompt,
                height=280
            )
