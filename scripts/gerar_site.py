#!/usr/bin/env python3
"""Gera as partes de SEO do site da OL3 Aquecedores.

- Atualiza no index.html: <title>, canonical, dados estruturados (JSON-LD)
  e a lista de cidades da seção "Onde atendemos".
- Cria uma página por cidade principal (ex.: aquecedor-a-gas-barueri/).
- Cria sitemap.xml e robots.txt.

Para trocar o endereço do site (ex.: quando o domínio próprio estiver pronto),
mude SITE_URL abaixo e rode:  python3 scripts/gerar_site.py
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

SITE_URL = "https://mfo-magnuslion.github.io/ol3-aquecedores/"
ROOT = Path(__file__).resolve().parent.parent

WHATSAPP = "5511972360424"
TELEFONE_VISIVEL = "(11) 97236-0424"
TELEFONE_SCHEMA = "+55-11-97236-0424"
CNPJ = "26.618.197/0001-10"
MARCAS = ["Rinnai", "Bosch", "Komeco", "Lorenzetti", "Rheem", "Heliotek"]
PAGAMENTO = "Crédito, débito, Pix e dinheiro"

# Ordem = da mais próxima para a mais distante de Jandira.
# "pagina": True gera uma página própria para a cidade.
CIDADES = [
    {"nome": "Jandira", "slug": "jandira", "pagina": True, "tempo": None,
     "intro": "Jandira é a base da OL3. É onde chegamos mais rápido, inclusive nas emergências.",
     "detalhe": "Atendemos todos os bairros de Jandira."},
    {"nome": "Barueri", "slug": "barueri", "pagina": True, "tempo": "10 minutos",
     "intro": "Barueri faz divisa com Jandira, então o deslocamento é curto.",
     "detalhe": "Atendemos todo o município, incluindo Alphaville e Tamboré, em casas e apartamentos."},
    {"nome": "Itapevi", "slug": "itapevi", "pagina": True, "tempo": "10 minutos",
     "intro": "Itapevi faz divisa com Jandira, então o deslocamento é curto.",
     "detalhe": "Atendemos todos os bairros de Itapevi."},
    {"nome": "Carapicuíba", "slug": "carapicuiba", "pagina": True, "tempo": "15 minutos",
     "intro": "Carapicuíba fica a poucos minutos de Jandira.",
     "detalhe": "Atendemos todos os bairros de Carapicuíba, em casas e apartamentos."},
    {"nome": "Santana de Parnaíba", "slug": "santana-de-parnaiba", "pagina": True, "tempo": "20 minutos",
     "intro": "Chegamos a Santana de Parnaíba pela Castello Branco.",
     "detalhe": "Atendemos o município, incluindo os residenciais de Alphaville."},
    {"nome": "Osasco", "slug": "osasco", "pagina": True, "tempo": "20 minutos",
     "intro": "Chegamos a Osasco pela Castello Branco.",
     "detalhe": "Atendemos todos os bairros de Osasco, em casas e apartamentos."},
    {"nome": "Cotia", "slug": "cotia", "pagina": True, "tempo": "20 minutos",
     "intro": "Cotia fica a cerca de 20 minutos de Jandira.",
     "detalhe": "Atendemos o município, incluindo a Granja Viana."},
    {"nome": "Araçariguama", "slug": "aracariguama", "pagina": False},
    {"nome": "Vargem Grande Paulista", "slug": "vargem-grande-paulista", "pagina": False},
    {"nome": "São Paulo", "slug": "sao-paulo", "pagina": True, "tempo": "25 a 30 minutos",
     "intro": "Atendemos a capital. A zona oeste (Butantã, Jaguaré, Rio Pequeno e Lapa) fica a cerca de 25 a 30 minutos de Jandira.",
     "detalhe": "Para outras regiões da cidade, consulte a disponibilidade pelo WhatsApp."},
    {"nome": "Embu das Artes", "slug": "embu-das-artes", "pagina": False},
    {"nome": "Taboão da Serra", "slug": "taboao-da-serra", "pagina": False},
    {"nome": "Cajamar", "slug": "cajamar", "pagina": False},
    {"nome": "Pirapora do Bom Jesus", "slug": "pirapora-do-bom-jesus", "pagina": False},
    {"nome": "São Roque", "slug": "sao-roque", "pagina": False},
    {"nome": "Itapecerica da Serra", "slug": "itapecerica-da-serra", "pagina": False},
]


def pasta(c):
    return f"aquecedor-a-gas-{c['slug']}"


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={quote(texto)}"


def esc(t):
    return html.escape(t, quote=True)


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


EMPRESA_ID = SITE_URL + "#empresa"


def empresa_schema():
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "@id": EMPRESA_ID,
        "name": "OL3 Aquecedores",
        "description": "Instalação e manutenção de aquecedores a gás de passagem (GLP e gás natural) conforme a ABNT NBR 13103. Técnico formado pelo SENAI.",
        "url": SITE_URL,
        "logo": SITE_URL + "assets/logo-fundo-claro.svg",
        "image": SITE_URL + "assets/logo-fundo-claro.svg",
        "telephone": TELEFONE_SCHEMA,
        "taxID": CNPJ,
        "address": {"@type": "PostalAddress", "addressLocality": "Jandira", "addressRegion": "SP", "addressCountry": "BR"},
        "areaServed": [{"@type": "City", "name": c["nome"]} for c in CIDADES],
        "paymentAccepted": "Cartão de crédito, cartão de débito, Pix, dinheiro",
        "knowsAbout": ["Aquecedor a gás de passagem", "ABNT NBR 13103", "GLP", "Gás natural"] + MARCAS,
        "contactPoint": {"@type": "ContactPoint", "telephone": TELEFONE_SCHEMA, "contactType": "customer service",
                         "availableLanguage": "Portuguese", "contactOption": "WhatsApp"},
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Instalação de aquecedor a gás"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Manutenção de aquecedor a gás"}},
        ],
    }


def faq_schema(perguntas):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in perguntas],
    }


def faq_da_home(texto):
    pares = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", texto)
    return [(html.unescape(q), html.unescape(re.sub(r"<.*?>", "", a))) for q, a in pares]


def bloco_seo(*objs):
    return "<!-- seo:inicio (gerado por scripts/gerar_site.py) -->\n" + "\n".join(jsonld(o) for o in objs) + "\n<!-- seo:fim -->"


def substituir_bloco(texto, inicio, fim, novo, antes_de=None):
    padrao = re.compile(re.escape(inicio) + r".*?" + re.escape(fim), re.S)
    if padrao.search(texto):
        return padrao.sub(lambda _: novo, texto, count=1)
    return texto.replace(antes_de, novo + "\n" + antes_de, 1)


def chips(prefixo):
    linhas = []
    for c in CIDADES:
        if c["pagina"]:
            linhas.append(f'      <li><a href="{prefixo}{pasta(c)}/">{esc(c["nome"])}</a></li>')
        else:
            linhas.append(f"      <li>{esc(c['nome'])}</li>")
    return "\n".join(linhas)


def atualizar_home():
    arq = ROOT / "index.html"
    t = arq.read_text(encoding="utf-8")
    t = re.sub(r"<title>.*?</title>", "<title>Aquecedor a Gás em Jandira e Região | OL3 Aquecedores</title>", t, count=1)
    t = re.sub(r'\n<link rel="canonical"[^>]*>', "", t)
    t = re.sub(r'\n<meta property="og:url"[^>]*>', "", t)
    t = t.replace('<meta property="og:type" content="website">',
                  f'<meta property="og:type" content="website">\n<meta property="og:url" content="{SITE_URL}">\n<link rel="canonical" href="{SITE_URL}">', 1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">',
               '<meta property="og:title" content="OL3 Aquecedores: aquecedor a gás em Jandira e região">', t, count=1)
    t = substituir_bloco(t, "<!-- seo:inicio", "<!-- seo:fim -->",
                         bloco_seo(empresa_schema(), faq_schema(faq_da_home(t))), antes_de="</head>")
    t = re.sub(r'(<ul class="cities">\n).*?(\n    </ul>)', lambda m: m.group(1) + chips("") + m.group(2), t, count=1, flags=re.S)
    arq.write_text(t, encoding="utf-8")


ICONES = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="i-wa" viewBox="0 0 24 24"><path d="M21 12a9 9 0 0 1-13.5 7.8L3 21l1.3-4.4A9 9 0 1 1 21 12z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5" fill="none" stroke="#15803D" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
    <symbol id="i-flame" viewBox="0 0 64 64"><path d="M32 4c4 9 15 15.5 15 29a15 15 0 0 1-30 0c0-7.5 3.8-12.3 7.5-15.5 0 6.4 2.7 9.6 6.4 10.7C29.8 19.6 29.8 12 32 4z" fill="#FACC15"/><path d="M32 32c2.6 4.2 6.4 6.8 6.4 11.6a6.4 6.4 0 0 1-12.8 0c0-3.2 1.6-5.3 3.2-6.9 0 2.7 1.1 4.3 3.2 4.8 0-3.2-.3-6.4 0-9.5z" fill="#12263A"/></symbol>
  </defs>
</svg>"""

NAV = [("quem-somos", "Quem somos"), ("como-funciona", "Como funciona"), ("instalacao", "Instalação"),
       ("manutencao", "Manutenção"), ("regioes", "Onde atendemos"), ("clientes", "Clientes"), ("duvidas", "Dúvidas")]


def check(texto):
    return f'<li><svg width="20" height="20" aria-hidden="true"><use href="#i-check"/></svg>{texto}</li>'


def pagina_cidade(c):
    nome = c["nome"]
    url = SITE_URL + pasta(c) + "/"
    texto_wa = f"Olá! Preciso de atendimento para aquecedor a gás em {nome}."
    distancia = (f"A cerca de {c['tempo']} de Jandira, sem trânsito." if c["tempo"]
                 else "Nossa base: atendimento mais rápido da região.")
    titulo = f"Aquecedor a Gás em {nome} | Instalação e Manutenção | OL3"
    descricao = (f"Instalação e manutenção de aquecedor a gás em {nome}, conforme a ABNT NBR 13103. "
                 f"Técnico formado pelo SENAI. Orçamento pelo WhatsApp {TELEFONE_VISIVEL}.")
    resp_atende = f"Sim. {c['detalhe']} {distancia if c['tempo'] else 'Jandira é a nossa base.'}"
    perguntas = [
        (f"Vocês atendem em {nome}?", resp_atende),
        ("Posso instalar o aquecedor no banheiro?",
         "Não. A NBR 13103 proíbe aquecedores a gás em banheiros e dormitórios, por risco de monóxido de carbono. O local certo costuma ser a área de serviço ou outro ambiente ventilado."),
        ("Vocês atendem gás de botijão e gás encanado?",
         "Sim, GLP e gás natural. O aparelho precisa ser compatível com o gás do imóvel. Se tiver dúvida, mande o modelo pelo WhatsApp que conferimos."),
        ("Quais as formas de pagamento?", "Cartão de crédito, cartão de débito, Pix e dinheiro."),
    ]
    outras = [o for o in CIDADES if o["pagina"] and o is not c]
    servico = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"Instalação e manutenção de aquecedor a gás em {nome}",
        "serviceType": "Instalação e manutenção de aquecedor a gás",
        "provider": {"@id": EMPRESA_ID, "@type": "HVACBusiness", "name": "OL3 Aquecedores", "telephone": TELEFONE_SCHEMA, "url": SITE_URL},
        "areaServed": {"@type": "City", "name": nome},
        "url": url,
    }
    trilha = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": f"Aquecedor a gás em {nome}", "item": url},
        ],
    }
    nav = "\n".join(f'      <a href="../#{a}">{t}</a>' for a, t in NAV)
    faq_html = "\n".join(f"      <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in perguntas)
    outras_html = "\n".join(f'      <li><a href="../{pasta(o)}/">{esc(o["nome"])}</a></li>' for o in outras)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titulo)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(descricao)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(f'Aquecedor a gás em {nome} | OL3 Aquecedores')}">
<meta property="og:description" content="{esc(descricao)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#12263A">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100,700;100,800;100,900;112,800;112,900&amp;family=IBM+Plex+Mono:wght@500&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="../assets/site.css">
{jsonld(servico)}
{jsonld(trilha)}
{jsonld(faq_schema(perguntas))}
</head>
<body>

{ICONES}

<header class="top">
  <div class="wrap top-bar">
    <a class="brand" href="../" aria-label="OL3 Aquecedores, início">
      <span class="brand-mark"><svg width="26" height="26" aria-hidden="true"><use href="#i-flame"/></svg></span>
      <span class="brand-name"><b>OL3</b><small>AQUECEDORES</small></span>
    </a>
    <nav class="nav" aria-label="Principal">
{nav}
    </nav>
    <a class="btn btn--whats" href="{wa(texto_wa)}" aria-label="WhatsApp {TELEFONE_VISIVEL}">
      <svg width="20" height="20" aria-hidden="true"><use href="#i-wa"/></svg><span>{TELEFONE_VISIVEL}</span>
    </a>
  </div>
  <nav class="subnav" aria-label="Seções">
    <div class="wrap">
{nav}
    </div>
  </nav>
</header>

<main>

<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <nav class="crumbs" aria-label="Você está em"><a href="../">Início</a> <span aria-hidden="true">/</span> {esc(nome)}</nav>
      <h1>Aquecedor a gás em {esc(nome)}: <em>instalação e manutenção.</em></h1>
      <p class="lead">{esc(c['intro'])} Serviço conforme a ABNT NBR 13103, feito por técnico formado pelo SENAI.</p>
      <div class="actions">
        <a class="btn btn--flame" href="{wa(texto_wa)}"><svg width="20" height="20" aria-hidden="true"><use href="#i-wa"/></svg>Pedir orçamento em {esc(nome)}</a>
        <a class="btn btn--ghost" href="#servicos">Ver serviços</a>
      </div>
    </div>
    <aside class="sheet" aria-label="Resumo do atendimento em {esc(nome)}">
      <div class="sheet-title"><h2>Atendimento em {esc(nome)}</h2><span class="label">OL3</span></div>
      <dl>
        <div class="row"><dt>Deslocamento</dt><dd>{esc(distancia)}</dd></div>
        <div class="row"><dt>Técnico</dt><dd>Miquéias Ferreira, formado pelo SENAI</dd></div>
        <div class="row"><dt>Norma</dt><dd>ABNT NBR 13103</dd></div>
        <div class="row"><dt>Gás</dt><dd>GLP (botijão) e GN (encanado)</dd></div>
        <div class="row"><dt>Marcas</dt><dd>{esc(', '.join(MARCAS[:-1]) + ' e ' + MARCAS[-1])}</dd></div>
        <div class="row"><dt>Pagamento</dt><dd>{PAGAMENTO}</dd></div>
      </dl>
    </aside>
  </div>
</section>

<section id="servicos" class="band">
  <div class="wrap">
    <div class="head">
      <span class="label">Serviços em {esc(nome)}</span>
      <h2>O que fazemos em {esc(nome)}</h2>
      <p class="lead">{esc(c['detalhe'])}</p>
    </div>
    <div class="service">
      <div class="panel">
        <h3>Instalação de aquecedor a gás</h3>
        <ul class="list">
          {check('Aparelho novo ou troca do antigo')}
          {check('Troca de chuveiro elétrico por aquecedor a gás')}
          {check('Avaliação de ventilação e exaustão do local')}
          {check('Ligação de água e gás, chaminé e teste de vazamento')}
          {check('Serviço com garantia')}
        </ul>
        <a class="btn btn--whats" href="{wa(f'Olá! Quero um orçamento de instalação de aquecedor em {nome}.')}"><svg width="20" height="20" aria-hidden="true"><use href="#i-wa"/></svg>Orçar instalação</a>
      </div>
      <div class="panel">
        <h3>Manutenção e conserto</h3>
        <ul class="list">
          {check('Revisão preventiva anual e limpeza')}
          {check('Aquecedor que não acende ou apaga sozinho')}
          {check('Água que não esquenta ou oscila')}
          {check('Chama amarelada ou queima ruim')}
          {check('Atendimento de emergência')}
        </ul>
        <a class="btn btn--whats" href="{wa(f'Olá! Quero agendar uma manutenção de aquecedor em {nome}.')}"><svg width="20" height="20" aria-hidden="true"><use href="#i-wa"/></svg>Agendar manutenção</a>
      </div>
    </div>
  </div>
</section>

<section class="band band--mist">
  <div class="wrap">
    <div class="head">
      <span class="label">Como funciona</span>
      <h2>Do primeiro contato ao banho quente</h2>
    </div>
    <ol class="steps">
      <li class="step"><h3>Chame no WhatsApp</h3><p>Diga o modelo do aparelho, o tipo de gás e mande uma foto do local.</p></li>
      <li class="step"><h3>Receba o orçamento</h3><p>Valor claro, com o que está incluso, e o melhor dia para você.</p></li>
      <li class="step"><h3>Serviço no local</h3><p>Vamos até você em {esc(nome)}, executamos o serviço e testamos tudo.</p></li>
      <li class="step"><h3>Pronto e garantido</h3><p>Você recebe as orientações de uso, e o serviço tem garantia.</p></li>
    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap faq">
    <div class="head">
      <span class="label">Dúvidas</span>
      <h2>Perguntas sobre o atendimento em {esc(nome)}</h2>
    </div>
    <div class="qa">
{faq_html}
    </div>
  </div>
</section>

<section class="band band--dark">
  <div class="wrap regions">
    <div class="head">
      <span class="label">Outras cidades</span>
      <h2>Também atendemos</h2>
    </div>
    <ul class="cities">
{outras_html}
      <li><a href="../#regioes">Ver todas as cidades</a></li>
    </ul>
  </div>
</section>

<section class="band">
  <div class="wrap cta">
    <div>
      <h2>Precisa de técnico de aquecedor em {esc(nome)}?</h2>
      <p class="lead">Mande uma mensagem e receba o orçamento sem compromisso.</p>
    </div>
    <a class="btn btn--whats" href="{wa(texto_wa)}"><svg width="20" height="20" aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp {TELEFONE_VISIVEL}</a>
  </div>
</section>

</main>

<footer>
  <div class="wrap foot">
    <span>OL3 Aquecedores · Instalação e manutenção de aquecedores a gás</span>
    <a href="https://wa.me/{WHATSAPP}">WhatsApp {TELEFONE_VISIVEL}</a>
    <span class="legal">CNPJ {CNPJ}</span>
  </div>
</footer>

<a class="float" href="{wa(texto_wa)}" aria-label="Falar com a OL3 no WhatsApp"><svg width="30" height="30" aria-hidden="true"><use href="#i-wa"/></svg></a>

</body>
</html>
"""


def main():
    atualizar_home()
    urls = [SITE_URL]
    for c in CIDADES:
        if not c["pagina"]:
            continue
        destino = ROOT / pasta(c)
        destino.mkdir(exist_ok=True)
        (destino / "index.html").write_text(pagina_cidade(c), encoding="utf-8")
        urls.append(SITE_URL + pasta(c) + "/")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc></url>" for u in urls]
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    print(f"{len(urls)} páginas no sitemap")


if __name__ == "__main__":
    main()
