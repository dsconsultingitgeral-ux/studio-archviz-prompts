if st.button("🚀 Gerar Master Prompt de Transformação", type="primary"):
    if not descricao_original or not novas_alteracoes:
        st.warning("Preenche a descrição original e as alterações pretendidas antes de gerar.")
    else:
        with st.spinner("A comunicar com o Groq..."):
            prompt_input = f"GEOMETRIA BASE:\n{descricao_original}\n\nALTERAÇÕES SOLICITADAS:\n{novas_alteracoes}"
            
            master_prompt = None
            erro_ultimo = None

            try:
                # Procura dinamicamente os modelos disponíveis na tua conta
                modelos_disponiveis = [m.id for m in client.models.list().data if "whisper" not in m.id and "guard" not in m.id]
            except Exception as e:
                # Se falhar a listagem, usa nomes padrão atualizados
                modelos_disponiveis = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]

            for modelo in modelos_disponiveis:
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT_ENGINE},
                            {"role": "user", "content": prompt_input}
                        ],
                        model=modelo,
                        temperature=0.15,
                    )
                    master_prompt = completion.choices[0].message.content
                    break  # Teve sucesso, sai do loop
                except Exception as e:
                    erro_ultimo = e
                    continue
            
            if master_prompt:
                st.success("Master Prompt Gerado com Sucesso!")
                st.text_area(
                    "Copia o Master Prompt abaixo. No Gemini, anexa a foto original e cola este texto:",
                    value=master_prompt,
                    height=280
                )
            else:
                st.error(f"Erro na ligação ao Groq: {erro_ultimo}")
