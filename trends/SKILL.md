---
name: trends
description: >
  Pesquisa Google Trends para um nicho ou conjunto de termos e retorna
  queries top, queries em ascensão e tópicos relacionados no Brasil.
  Deve ser invocada ANTES de criar carrossel, anúncio, LP ou roteiro —
  para ancorar o conteúdo em demanda real, não em intuição.
  Triggers: "/trends", "pesquisa tendências", "o que as pessoas buscam sobre",
  "o que está em alta sobre", "tendências do nicho".
argument-hint: '"termo1" "termo2" "termo3" [--geo BR] [--period "today 3-m"]'
---

# /trends — Pesquisa de tendências Google Trends

Descobre o que as pessoas **realmente buscam** no Google sobre um nicho.
Output: queries top, queries em ascensão, tópicos relacionados e classificação de comportamento.
Uso recomendado antes de criar qualquer conteúdo, LP ou anúncio.

---

## Quando invocar

- Antes de `/carrossel` — para escolher tema com demanda real
- Antes de `/anuncio-google` — para escolher palavras-chave e ângulo
- Antes de escrever ou reescrever uma LP — para alinhar copy com buscas reais
- Quando quiser entender o que o público de um nicho está perguntando agora
- Complementa o `/meta-radar`: trends = demanda no Google, meta-radar = criativos que estão rodando no Meta

---

## Protocolo de execução

### Passo 1 — Identificar termos-semente

Se o usuário passou argumentos, usar diretamente.
Se não passou, perguntar:

> "Quais termos definem o nicho? (ex: 'harmonização orofacial', 'nutricionista', 'emagrecimento') — máx 5 termos."

Dica: misturar 1 termo amplo + 1-2 termos de especialidade + 1 termo de intenção (ex: "como emagrecer") dá o melhor resultado.

### Passo 2 — Rodar script

```bash
python ~/.claude/skills/trends/scripts/trends.py "TERMO1" "TERMO2" "TERMO3"
```

Para outra região ou período:
```bash
python ~/.claude/skills/trends/scripts/trends.py "TERMO1" --geo BR --period "today 12-m"
```

O script faz duas consultas internamente: 3 meses (tendência recente) + 12 meses (classificação evergreen/trending/sazonal/declinando). Não precisa rodar duas vezes.

**Dependência:** `pip install pytrends` (instalar uma vez na máquina).

### Passo 3 — Interpretar e apresentar

Não jogar o output bruto. Apresentar assim:

**Oportunidades imediatas (rising):**
Lista os 5 termos com maior crescimento — esses são os que estão explodindo agora.

**Volume consolidado (top):**
Lista os 5 termos de maior volume — esses são o mainstream do nicho.

**Onde usar cada termo:**
Para cada oportunidade identificada, sugerir:
- Se é gancho de carrossel
- Se é headline de anúncio
- Se é título de LP
- Se é tema de Reel/roteiro

### Passo 4 — Salvar resultado (opcional)

Se estiver dentro de um projeto com `dados/`, salvar em:
```
dados/trends-[nicho]-[YYYY-MM-DD].md
```

---

## Regras

- Nunca apresentar o output bruto do script — sempre interpretar
- Priorizar sempre os **rising** sobre os **top** — rising = oportunidade, top = commodity
- Máx 5 termos por consulta (limite do Google Trends)
- Se retornar vazio em algum termo, tentar com termo mais curto ou genérico
- Período padrão: últimos 3 meses (`today 3-m`) — suficiente para detectar tendências atuais
- Para sazonalidade usar `today 12-m`

---

## Integração com outras skills

- `/meta-radar` — use junto: trends mostra o que o público busca, meta-radar mostra o que os concorrentes estão veiculando
- `/carrossel` — usa os termos rising como base para gancho e tema
- `/anuncio-google` — usa os termos top como palavras-chave de campanha
