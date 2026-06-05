"""
trends.py — Google Trends + Google Autocomplete por nicho.
Classifica: evergreen / trending / sazonal / declinando.
Autocomplete: frases exatas que as pessoas digitam no Google agora.
Uso: python trends.py "termo1" "termo2" "termo3" [--geo BR] [--period "today 3-m"]
"""

import sys
import io
import time
import argparse
import statistics
import urllib.request
import urllib.parse
import json

# Fix encoding no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pytrends.request import TrendReq


def autocomplete(termo, hl="pt-BR", gl="br"):
    """Busca sugestões do Google Autocomplete para um termo."""
    try:
        termo_encoded = urllib.parse.quote(termo)
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&hl={hl}&gl={gl}&q={termo_encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            sugestoes = data[1] if len(data) > 1 else []
            return [s for s in sugestoes if s.lower() != termo.lower()]
    except Exception:
        return []


def classificar_comportamento(serie):
    if serie is None or len(serie) < 4:
        return "insuficiente", None

    valores = list(serie)
    media = statistics.mean(valores)
    if media == 0:
        return "insuficiente", None

    n = len(valores)
    inicio = statistics.mean(valores[:n//3]) if n >= 3 else valores[0]
    fim = statistics.mean(valores[-(n//3):]) if n >= 3 else valores[-1]
    variacao = statistics.stdev(valores) / media if media > 0 else 0
    crescimento = (fim - inicio) / inicio if inicio > 0 else 0

    if crescimento > 0.5 and fim > media:
        return "trending", f"+{crescimento*100:.0f}% nos ultimos meses"
    elif crescimento < -0.4:
        return "declinando", f"{crescimento*100:.0f}% de queda"
    elif variacao < 0.25:
        return "evergreen", f"volume estavel (~{media:.0f}/100)"
    else:
        return "sazonal", f"variacao de {variacao*100:.0f}% — picos periodicos"


def buscar_trends(termos, geo="BR", period="today 3-m"):
    pytrends = TrendReq(hl="pt-BR", tz=-180)
    termos = termos[:5]

    output = []
    output.append(f"# Pesquisa de Demanda — {', '.join(termos)}")
    output.append(f"Regiao: {geo} | Periodo: {period}\n")

    output.append("## Google Autocomplete — frases exatas que as pessoas digitam")
    output.append("Use essas frases como headlines de anuncio, titulo de LP e gancho de carrossel.\n")

    for termo in termos:
        sugestoes = autocomplete(termo)
        if sugestoes:
            output.append(f'"{termo}":')
            for s in sugestoes[:8]:
                output.append(f"- {s}")
            output.append("")
        else:
            output.append(f'"{termo}": sem sugestoes\n')

    try:
        pytrends.build_payload(termos, cat=0, timeframe=period, geo=geo)
        time.sleep(1.5)
        interest_curto = pytrends.interest_over_time()
        if not interest_curto.empty and "isPartial" in interest_curto.columns:
            interest_curto = interest_curto.drop(columns=["isPartial"])
    except Exception:
        interest_curto = None

    try:
        pytrends.build_payload(termos, cat=0, timeframe="today 12-m", geo=geo)
        time.sleep(1.5)
        interest_longo = pytrends.interest_over_time()
        if not interest_longo.empty and "isPartial" in interest_longo.columns:
            interest_longo = interest_longo.drop(columns=["isPartial"])
    except Exception:
        interest_longo = None

    output.append("## Classificacao de comportamento (12 meses)")
    output.append("Evergreen = demanda constante | Trending = explosao recente | Sazonal = picos periodicos | Declinando = queda\n")

    if interest_longo is not None and not interest_longo.empty:
        for termo in termos:
            if termo in interest_longo.columns:
                tipo, detalhe = classificar_comportamento(interest_longo[termo])
                media = interest_longo[termo].mean()
                detalhe_str = f"— {detalhe}" if detalhe else ""
                output.append(f"- {termo}: {tipo} {detalhe_str} | volume medio {media:.0f}/100")
    else:
        output.append("Dados de longo prazo indisponiveis")
    output.append("")

    if interest_curto is not None and not interest_curto.empty:
        output.append("## Volume relativo (ultimos 3 meses, 0-100)")
        medias_curto = interest_curto.mean().sort_values(ascending=False)
        for termo, val in medias_curto.items():
            barra = "#" * max(1, int(val / 10))
            output.append(f"- {termo}: {val:.0f}/100  {barra}")
        output.append("")

    for termo in termos:
        try:
            pytrends.build_payload([termo], cat=0, timeframe=period, geo=geo)
            time.sleep(1.5)
            related = pytrends.related_queries()
            data = related.get(termo, {})

            output.append(f'## "{termo}" — queries relacionadas')

            top = data.get("top")
            if top is not None and not top.empty:
                output.append("Top (volume consolidado):")
                for _, row in top.head(8).iterrows():
                    output.append(f"- {row['query']} [{row['value']}]")
            else:
                output.append("Sem dados top")
            output.append("")

            rising = data.get("rising")
            if rising is not None and not rising.empty:
                output.append("Rising (crescimento recente — oportunidade agora):")
                for _, row in rising.head(8).iterrows():
                    crescimento = f"+{row['value']}%" if row["value"] < 5000 else "Breakout"
                    output.append(f"- {row['query']} [{crescimento}]")
            else:
                output.append("Sem dados rising")
            output.append("")

        except Exception as e:
            output.append(f"Erro em \"{termo}\": {e}\n")

    output.append("---")
    output.append("## Como usar esses dados\n")
    output.append("Autocomplete: copie como titulo de anuncio, H1 da LP, gancho de carrossel.")
    output.append("Evergreen: campanha Google sempre ligada. Volume previsivel, CPL estavel.")
    output.append("Trending: entrar agora custa menos. Lancao ainda barato.")
    output.append("Rising: gancho de Reel e carrossel. A pergunta que o publico faz essa semana.")
    output.append("Top: vocabulario da LP. Use nos titulos e subheadlines.")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Google Trends + Autocomplete para pesquisa de demanda")
    parser.add_argument("termos", nargs="+", help="Termos de busca (max 5)")
    parser.add_argument("--geo", default="BR", help="Regiao (padrao: BR)")
    parser.add_argument("--period", default="today 3-m", help="Periodo (padrao: today 3-m)")
    args = parser.parse_args()

    resultado = buscar_trends(args.termos, geo=args.geo, period=args.period)
    print(resultado)


if __name__ == "__main__":
    main()
