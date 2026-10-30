# OL3 Aquecedores

Site da OL3 Aquecedores: instalação e manutenção de aquecedores a gás de passagem em Jandira e região.

Site estático (HTML + CSS), sem etapa de build. Para ver localmente:

```bash
python3 -m http.server 8000
```

e abra http://localhost:8000.

## Estrutura

- `index.html`: página principal
- `aquecedor-a-gas-<cidade>/`: páginas por cidade (geradas)
- `assets/site.css`: visual compartilhado por todas as páginas
- `sitemap.xml` e `robots.txt`: gerados

## SEO e páginas por cidade

As páginas por cidade, o sitemap, os dados estruturados (JSON-LD) e a lista de cidades da página
principal são gerados por `scripts/gerar_site.py`. Para mudar cidades ou o endereço do site
(ex.: domínio próprio), edite as constantes no topo do script e rode:

```bash
python3 scripts/gerar_site.py
```

## Publicação

Hospedado no GitHub Pages a partir da raiz do ramo `main`.
