import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(r"C:\Users\NERES\Documents\deepseek-harness\default-workspace\tenda-jurema")

VAZIOS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
          "meta", "param", "source", "track", "wbr"}


class Analisador(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha = []
        self.erros = []
        self.ids = []
        self.refs = []          # (atributo, valor)
        self.ancoras = []       # href="#..."
        self.linhas = {}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        ln = self.getpos()[0]
        if "id" in d:
            self.ids.append((d["id"], ln))
        for chave in ("src", "href"):
            if chave in d:
                self.refs.append((chave, d[chave], ln))
                if chave == "href" and d[chave].startswith("#") and len(d[chave]) > 1:
                    self.ancoras.append((d[chave][1:], ln))
        if tag not in VAZIOS:
            self.pilha.append((tag, ln))
        self.linhas[tag] = ln

    def handle_endtag(self, tag):
        if tag in VAZIOS:
            return
        if not self.pilha:
            self.erros.append(f"linha {self.getpos()[0]}: </{tag}> sem abertura")
            return
        topo, ln = self.pilha.pop()
        if topo != tag:
            self.erros.append(
                f"linha {self.getpos()[0]}: </{tag}> fecha <{topo}> aberto na linha {ln}"
            )

    def fechar(self):
        for tag, ln in self.pilha:
            self.erros.append(f"<{tag}> aberto na linha {ln} nunca fechado")


def checar_css(caminho: Path, texto: str):
    problemas = []
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", texto, re.S):
        css = m.group(1)
        abre, fecha = css.count("{"), css.count("}")
        if abre != fecha:
            problemas.append(f"CSS: {abre} '{{' vs {fecha} '}}'")
        if re.search(r":\s*;", css):
            problemas.append("CSS: valor vazio (':;')")
        for var in set(re.findall(r"var\((--[a-z0-9-]+)", css)):
            if not re.search(re.escape(var) + r"\s*:", css):
                problemas.append(f"CSS: variável {var} usada mas não definida")
    return problemas


def checar_arquivo(caminho: Path):
    texto = caminho.read_text(encoding="utf-8")
    rel = caminho.relative_to(RAIZ)
    problemas = []

    p = Analisador()
    p.feed(texto)
    p.fechar()
    problemas += p.erros

    # ids duplicados
    vistos = {}
    for i, ln in p.ids:
        if i in vistos:
            problemas.append(f"id duplicado '{i}' (linhas {vistos[i]} e {ln})")
        vistos[i] = ln

    # âncoras quebradas
    for alvo, ln in p.ancoras:
        if alvo not in vistos:
            problemas.append(f"linha {ln}: href=\"#{alvo}\" sem destino")

    # assets locais
    for chave, valor, ln in p.refs:
        if valor.startswith(("http://", "https://", "data:", "mailto:", "tel:", "#", "//")):
            continue
        destino = (caminho.parent / valor.split("?")[0].split("#")[0]).resolve()
        if not destino.exists():
            problemas.append(f"linha {ln}: {chave}=\"{valor}\" não encontrado")

    problemas += checar_css(caminho, texto)

    # checagens específicas do projeto
    if "logo.jpg" in texto and "assets/logo.jpg" not in texto:
        problemas.append("referencia a logo sem o caminho ../assets/logo.jpg")

    print(f"\n=== {rel} ===")
    print(f"  {len(texto):,} bytes · {texto.count(chr(10))+1} linhas · "
          f"{len(p.ids)} ids · {len(p.refs)} referências · {len(p.ancoras)} âncoras internas")
    if problemas:
        for x in problemas:
            print("  [X] " + x)
    else:
        print("  [OK] estrutura íntegra: tags balanceadas, refs resolvidas, CSS consistente")
    return problemas


todos = {}
for arq in sorted(RAIZ.glob("**/*.html")):
    if "_preview" in str(arq):
        continue
    todos[str(arq.relative_to(RAIZ))] = checar_arquivo(arq)

total = sum(len(v) for v in todos.values())
print("\n" + "=" * 62)
print(f"RESULTADO: {len(todos)} páginas · {total} problema(s)")
sys.exit(1 if total else 0)
