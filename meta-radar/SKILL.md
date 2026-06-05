---
name: meta-radar
description: >
  Varre a Biblioteca de Anúncios do Meta para um nicho e retorna os criativos
  ativos com links diretos, padrões de copy dominantes e sugestões de gancho
  para carrossel. Usa o Meta MCP — requer integração com Meta Ads configurada.
  Triggers: "/meta-radar", "o que está rodando no Meta", "criativos de concorrentes",
  "inspiração de anúncios", "o que os concorrentes anunciam", "biblioteca de anúncios".
argument-hint: '"nicho ou termo" [--pais BR]'
---

# /meta-radar — Biblioteca de Anúncios do Meta

Descobre o que os concorrentes estão **pagando para veicular** no Meta.
Anúncio ativo = dinheiro sendo gasto = está funcionando.
Output: links diretos dos criativos, padrões de copy, ângulos dominantes, sugestões de gancho.

Complementa o `/trends`: enquanto trends mostra o que o público **busca**, o meta-radar mostra o que os anunciantes já **testaram e mantêm no ar**.

---

## Quando invocar

- Antes de `/carrossel` — para ver que ângulos já estão convertendo no nicho
- Antes de criar criativos para campanha — para não reinventar o que já foi testado
- Para benchmark de concorrentes — ver quem anuncia, com que frequência e com que copy
- Para qualquer nicho regulamentado (saúde, direito) — ver o que passa e o que não passa na moderação
- Complementa `/trends`: use os dois juntos para ter demanda + criativo validado

---

## Protocolo de execução

### Passo 1 — Identificar termos de busca

Se o usuário passou argumentos, usar diretamente.
Se não passou, perguntar:

> "Qual é o nicho? (ex: 'harmonização orofacial', 'nutricionista emagrecimento', 'clínica odontológica') — 1 a 3 termos."

Dica: começar com o termo mais específico do serviço. Se retornar poucos resultados, ampliar para o nicho geral.

### Passo 2 — Buscar na Biblioteca de Anúncios

Fazer **2 buscas** com variações do termo para cobrir mais ângulos:

**Busca 1 — termo principal (serviço específico):**
Usar `ads_library_search` com:
- `search_terms`: termo principal (ex: "harmonização orofacial")
- `ad_active_status`: ACTIVE
- `countries`: ["BR"]
- `ad_type`: ALL
- `limit`: 30

**Busca 2 — termo amplo (nicho geral):**
Usar `ads_library_search` com:
- `search_terms`: variação mais ampla (ex: "harmonização facial botox")
- `ad_active_status`: ACTIVE
- `countries`: ["BR"]
- `ad_type`: ALL
- `limit`: 20

### Passo 3 — Analisar e apresentar

Não listar os anúncios brutos. Extrair padrões e apresentar assim:

---

**Panorama do nicho:**
Quantos anúncios ativos encontrados, quantas páginas diferentes anunciando, qual o formato dominante (imagem / vídeo / carrossel).

**Ângulos de copy dominantes:**
Agrupar os anúncios pelos ângulos que aparecem mais. Exemplos de ângulos comuns:
- Transformação (antes/depois implícito ou explícito)
- Autoridade (tempo de experiência, especialização, registro)
- Dor + solução ("cansada de..." / "sem precisar de...")
- Resultado específico ("lábios naturais", "sorriso harmonioso em X sessões")
- Urgência/escassez ("vagas limitadas", "agenda aberta")
- Educativo ("você sabia que...")
- Prova social (depoimento, número de pacientes — observar conformidade com conselhos)

Para cada ângulo identificado: quantos anúncios usam, exemplo de copy, se tem link disponível.

**Links dos criativos mais relevantes:**
Listar os `ad_snapshot_url` dos anúncios mais representativos — mínimo 5, máximo 15.
Formato:
- [Página] Trecho do copy → link

**Formato de creative mais usado:**
Qual formato domina: imagem estática, vídeo curto ou carrossel. Isso informa o formato a priorizar.

### Passo 4 — Sugerir ganchos para carrossel

Com base nos padrões encontrados, sugerir 3 ganchos de carrossel prontos para usar:

Formato de cada sugestão:
- **Ângulo:** [nome do ângulo]
- **Slide 1 (gancho):** [texto exato sugerido]
- **Por que funciona:** [1 linha explicando o padrão que valida esse gancho]

---

## Regras

- Sempre priorizar anúncios **ACTIVE** — anúncio inativo não valida nada
- Sempre filtrar por **BR** — benchmark de outro país não se aplica diretamente
- Incluir os `ad_snapshot_url` — o link é o que permite ver o criativo real, não só o texto
- Se o nicho for área regulamentada (saúde, direito, finanças), sinalizar quais ângulos encontrados podem ter problemas de conformidade com o conselho correspondente
- Nunca recomendar copiar copy diretamente — usar como referência de ângulo e tom, não de texto
- Se retornar menos de 5 anúncios ativos, ampliar o termo e rodar nova busca antes de apresentar

---

## Integração com outras skills

- `/trends` — use antes: trends diz o que o público busca, meta-radar diz o que já converte em anúncio. Juntos definem estratégia completa de conteúdo e mídia paga
- `/carrossel` — use depois: leve os ganchos sugeridos pelo meta-radar direto para o carrossel
- `/anuncio-google` — use junto: ângulos que funcionam no Meta geralmente funcionam no Google com adaptação de intenção
