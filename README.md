# Marketing Skills — Claude Code

Skills de pesquisa de mercado para o Claude Code. Descobrem demanda real e criativos validados antes de criar qualquer conteúdo, anúncio ou landing page.

## Skills disponíveis

### /trends
Pesquisa Google Trends + Google Autocomplete para um nicho.
Retorna: frases exatas que o público digita, classificação de comportamento (evergreen/trending/sazonal/declinando), queries em ascensão e volume consolidado.

**Quando usar:** antes de criar carrossel, anúncio, LP ou roteiro. Para saber o que o público está buscando agora.

### /meta-radar
Varre a Biblioteca de Anúncios do Meta e retorna os criativos ativos no nicho, com links diretos, padrões de copy e sugestões de gancho para carrossel.

**Quando usar:** antes de criar criativos para campanha. Para ver o que os concorrentes já testaram e mantêm no ar — anúncio ativo = dinheiro sendo gasto = está funcionando.

**Requer:** Meta MCP configurado no Claude Code.

---

## Antes de rodar as skills — o passo que a maioria ignora

As skills pesquisam pelos termos que você passa. O resultado depende de quão bons são esses termos.

O erro mais comum: pesquisar como especialista. "Harmonização orofacial", "toxina botulínica", "recomposição corporal" — são termos técnicos que o público raramente digita.

**O que funciona:** pedir pro Claude pensar como o paciente que está com o problema, não como o profissional que resolve.

Antes de rodar qualquer skill, faça isso:

```
Você é uma pessoa de 35 anos que quer melhorar a aparência do rosto
mas não sabe os termos técnicos. Como você pesquisaria isso no Google?
Me dá 5 termos que você digitaria.
```

Os termos que aparecem — "botox lábios", "deixar rosto mais jovem", "tirar bigode chinês" — são o que o público realmente busca. Esses são os termos que você passa para `/trends` e `/meta-radar`.

O Claude ajuda a potencializar a pesquisa, mas quem sabe o que o paciente sente é o especialista. Use esse conhecimento para guiar os termos — a skill faz o resto.

---

## Como usar juntas

```
/trends "botox facial" "harmonizar rosto" "bigode chinês"
→ descobre o que o público busca no Google agora

/meta-radar "harmonização orofacial" "botox facial"
→ descobre o que os concorrentes estão veiculando no Meta

/carrossel [com gancho definido pelas duas pesquisas]
→ cria conteúdo ancorado em demanda real e criativo validado
```

---

## Instalação

**Requisito:** [Claude Code](https://claude.ai/code) instalado — funciona igual no terminal, no VS Code (extensão Claude Code) e no app desktop.

**Windows (cole no terminal e pressione Enter):**

```powershell
git clone https://github.com/vhpoliv/marketing-skills.git $env:TEMP\mkt-skills; Copy-Item "$env:TEMP\mkt-skills\trends" "$env:USERPROFILE\.claude\skills\" -Recurse -Force; Copy-Item "$env:TEMP\mkt-skills\meta-radar" "$env:USERPROFILE\.claude\skills\" -Recurse -Force; Remove-Item "$env:TEMP\mkt-skills" -Recurse -Force; pip install pytrends
```

**Mac/Linux:**

```bash
git clone https://github.com/vhpoliv/marketing-skills.git /tmp/mkt-skills && cp -r /tmp/mkt-skills/trends ~/.claude/skills/ && cp -r /tmp/mkt-skills/meta-radar ~/.claude/skills/ && rm -rf /tmp/mkt-skills && pip install pytrends
```

Depois de instalado, acione diretamente no Claude Code:

```
/trends "seu nicho aqui"
/meta-radar "seu nicho aqui"
```

---

## Notas

- `/trends` funciona sem configuração adicional além do `pip install pytrends`
- `/meta-radar` requer o Meta MCP configurado — sem ele, o Claude Code não tem acesso à Biblioteca de Anúncios
- Ambas as skills funcionam para qualquer nicho, não só saúde ou odontologia
