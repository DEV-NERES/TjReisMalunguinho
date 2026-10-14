# Modelos de Homepage Institucional — Tenda de Jurema Reis Malunguinho

Etapa 1 do projeto da plataforma: **site institucional público** (RF-001 a RF-007, RF-015).
Cinco protótipos navegáveis, construídos a partir da logo oficial e da paleta extraída dela.

## Como abrir

Abra **`index.html`** — ele traz o comparador com as prévias dos cinco modelos, a paleta
documentada, a tabela comparativa e o checklist do que falta definir.

Ou abra cada modelo diretamente:

| # | Modelo | Arquivo | Tom |
|---|---|---|---|
| 1 | **Altar** | `modelo-1-altar/index.html` | Clássico sóbrio, heráldico, fundo escuro |
| 2 | **Jurema Viva** | `modelo-2-jurema-viva/index.html` | Orgânico, claro, acolhedor |
| 3 | **Editorial** | `modelo-3-editorial/index.html` | Revista / jornal cultural |
| 4 | **Portal** | `modelo-4-portal/index.html` | Funcional, acesso rápido, ponte para a plataforma |
| 5 | **Cerimonial** | `modelo-5-cerimonial/index.html` | Imersivo, cinematográfico, capítulos numerados |

Todos são responsivos (celular, tablet, desktop), funcionam sem servidor e não têm dependências
de framework. As únicas requisições externas são as fontes do Google Fonts — sem internet, o
navegador usa as fontes de sistema equivalentes.

## Estrutura

```
tenda-jurema/
├── index.html                    comparador + paleta + checklist
├── README.md                     este arquivo
├── assets/
│   ├── logo.jpg                  logo recebida (640×640)
│   └── paleta.css                tokens de design reutilizáveis
├── modelo-1-altar/index.html
├── modelo-2-jurema-viva/index.html
├── modelo-3-editorial/index.html
├── modelo-4-portal/index.html
├── modelo-5-cerimonial/index.html
└── _tools/
    ├── palette.py                extração da paleta da logo
    └── validar.py                validação de HTML, refs e CSS
```

## Paleta

Extraída da logo por quantização de 68.085 amostras de pixel (ignorando o fundo preto dos cantos).

| Família | Ocorrência na logo | Cor de referência | Papel no layout |
|---|---|---|---|
| Marrom terra | 48,8% | `#5A4230` | Áreas grandes, fundos |
| Sombra | 34,1% | `#241A12` / `#0B0806` | Fundos profundos |
| Verde folha | 8,4% | `#4A6340` | Blocos institucionais |
| Areia / creme | 5,8% | `#E2D3B8` | Texto e superfícies claras |
| Ouro / bronze | 2,5% | `#C9A45C` | **Apenas acento** |

A regra aplicada em todos os modelos: **o ouro ocupa menos de 10% da área visível.** Isso é o que
mantém a fidelidade à logo — ela também é predominantemente terrosa, com ouro só nas letras e na moldura.

Os tokens estão em `assets/paleta.css`, prontos para virar a fonte única de verdade das cores
na implementação real.

## O que é conteúdo de exemplo

**Tudo.** Nenhum texto, data, evento, valor ou dado de contato foi obtido de fonte real —
foram escritos apenas para dar forma ao layout. Itens que a Direção precisa fornecer:

1. História, apresentação, missão e valores da Tenda
2. Endereço completo da sede
3. Telefone, e-mail e redes oficiais
4. Agenda real de eventos (data, horário, local, descrição)
5. Fotos e vídeos autorizados, com a classificação de acesso de cada mídia
6. Dados para doação (Pix, conta ou outra via)
7. Documentos institucionais: estatuto, atas, política de privacidade
8. **Logo em alta resolução** — a imagem disponível tem só 640×640 px; para telas grandes e
   impressão é necessário o arquivo original, idealmente vetorial

## Decisões que os modelos levantam

Pontos do documento de requisitos que a escolha do modelo força a definir:

- **Modelo escolhido** (ou combinação de seções de modelos diferentes — é perfeitamente possível,
  por exemplo, usar a capa do Cerimonial com os módulos do Portal)
- **Quem publica o quê**: quais funções da Direção terão permissão de criar, editar e publicar
  conteúdo (RF-010 a RF-013)
- **Fluxo rascunho → publicado** precisa de estados visíveis na administração (RF-014)
- **Classificação dos conteúdos restritos** — item 9 dos pontos pendentes da especificação
- **Prestação de contas pública**: relatórios no site aberto ou apenas na área de membros?
- **Formulário de contato**: envio real por e-mail? Quem recebe? Proteção anti-spam?
- **Indexação** (RNF-011): confirmar que o site público é indexável e a área de membros não

## Validação

`_tools/validar.py` confere, em cada página: balanceamento de tags, ids duplicados, âncoras
internas quebradas, referências a arquivos locais inexistentes e consistência do CSS
(chaves e variáveis).

```powershell
python _tools\validar.py
```

Resultado atual: **6 páginas, 0 problemas.**

> A verificação visual automatizada (screenshot headless) não foi possível neste ambiente —
> o sandbox bloqueia a inicialização do navegador. A conferência visual foi feita por inspeção
> do código; recomenda-se abrir os cinco modelos no navegador antes de decidir.
