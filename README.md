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

## Como usar juntas

```
/trends "harmonização orofacial" "botox facial"
→ descobre o que o público busca no Google

/meta-radar "harmonização orofacial"
→ descobre o que os concorrentes estão veiculando no Meta

/carrossel [com gancho definido pelas duas pesquisas]
→ cria conteúdo ancorado em demanda real e criativo validado
```

---

## Instalação

**Requisito:** [Claude Code](https://claude.ai/code) instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/vitorhugoeu/marketing-skills.git /tmp/marketing-skills

# 2. Copie as skills para a pasta do Claude Code
cp -r /tmp/marketing-skills/trends ~/.claude/skills/
cp -r /tmp/marketing-skills/meta-radar ~/.claude/skills/

# 3. Instale a dependência do /trends
pip install pytrends
```

No Windows (PowerShell):
```powershell
git clone https://github.com/vitorhugoeu/marketing-skills.git $env:TEMP\marketing-skills
Copy-Item "$env:TEMP\marketing-skills\trends" "$env:USERPROFILE\.claude\skills\" -Recurse
Copy-Item "$env:TEMP\marketing-skills\meta-radar" "$env:USERPROFILE\.claude\skills\" -Recurse
pip install pytrends
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
