# Revisão de lançamento — 2026-11-10

## Veredito e severidade

Revisão independente, read-only e limitada a quatro minutos. **P0: 0; P1: 0 defeitos críticos reproduzidos no stage atual. P2: 1 observação de entrega**, abaixo. Não é garantia de ausência de defeitos, certificação legal ou aprovação de direitos de conteúdo. Não publicar com base neste documento sem a autorização operacional separada.

### P2 — ZIPs antigos não representam o stage atual

`dist/disk-television-0.1-pages.zip` e `dist/disk-television-0.2-pages.zip` existem e passam a integridade ZIP, mas têm arquivos divergentes do `_site` atual, inclusive HTML, dados e scripts ESM antigos. Não foi encontrado ZIP Pages 0.3 nesta inspeção. Não bloqueia publicar diretamente o `_site` validado; não distribuir esses ZIPs como versão atual. `tools/package.py:15-20` calcula o nome pela versão corrente e empacota o stage, mas não remove releases anteriores. Nenhuma execução de empacotamento foi feita nesta revisão.

Reprodução read-only, a partir da raiz, com `.venv/Scripts/python.exe -c`:

```python
from pathlib import Path
import zipfile
for p in Path('dist').glob('*pages.zip'):
    with zipfile.ZipFile(p) as z:
        print(p, z.testzip(), [n for n in z.namelist()
              if not Path('_site', n).is_file()
              or z.read(n) != Path('_site', n).read_bytes()])
```

## Resolução posterior pelo coordenador

Os pacotes 0.3 foram gerados após esta inspeção. O coordenador verificou integridade do ZIP Pages e comparou seus 21 membros byte a byte com `_site`: zero divergências. O ZIP source inclui esta revisão. As versões 0.1/0.2 foram preservadas como históricas, não são os artefatos de lançamento atual. A observação P2 fica resolvida para a distribuição explícita da versão 0.3.

Após a inspeção também foi acrescentada e validada a regressão de teclado `key='Unidentified'` com keyCode de seta e Voltar 10009. A suíte integrada foi reexecutada: 69 testes e ambos os diagnósticos reais aprovados. Essa atualização do coordenador não amplia o escopo original da revisão independente nem declara teste Samsung.

## Execução efetiva nesta revisão

- Node invocado exclusivamente via `.venv/Scripts/python.exe` / `subprocess.run`, expandindo `tests/*.test.mjs` em Python: **46 testes, 46 passaram, zero falhas/skip**, exit 0. Inclui compilação opt-in, abertura/link, localização de cada segundo do dia, pré-época/meia-noite/reload e ciclo sem lacunas; áudio usa mock Web Audio explicitamente identificado.
- `PYTHONDONTWRITEBYTECODE=1 .venv/Scripts/python.exe tests/production_browser_test.py`: **1 teste passou**, exit 0, Chrome headless, subpath `/disk-television/`, bundle de produção real e API YouTube simulada declaradamente. Exercitou remoção dos três métodos polyfilled, reload/offset, erro 150, recuperação automática no próximo vídeo, guia e página legal. Não é teste de Chrome 69 real.
- Manifesto `_site/release.json`: **zero hashes divergentes**; stage com **21 arquivos**. `data/catalog.json` e `data/schedule.json` do stage são byte a byte iguais às fontes.
- Esbuild executado **em memória**, via API `build({write:false, entryPoints:['src/app.js'], bundle:true, format:'iife', target:'chrome69', charset:'utf8', legalComments:'inline', banner:{js:...compat...}})`: saída byte a byte igual a `_site/app.bundle.js`. Não recompilou nem alterou `_site`.
- Não rodou `tests/build_test.py`: ele chama o builder e reescreve `_site` (`tests/build_test.py:8`), proibido pelo escopo. Não rodou testes que regravam evidências.

## Inspeção dirigida

- `src/app.js:19-25,120-143,209-223,258-260,276-287`: gate de visibilidade com tamanho mínimo e fração visível; guia e seletor param YouTube e áudio antes de esconder; retorno recompõe o horário corrente, não um offset congelado. Decorações estão fora do iframe nos estilos inspecionados. Não se reproduziu obstrução ou reprodução oculta; essa conclusão é limitada à inspeção e às evidências abaixo, não cobre todas as corridas de eventos possíveis.
- `src/station-audio.js:49-97`: mute/diálogos cortam a fonte; natural `onended` conserva `playedKey`; callback antigo não apaga fonte nova; stop explícito permite retomada no offset corrente. Os testes de áudio cobrem essas distinções, falhas de decode/fetch/start e fallback MP3/WAV sem fazer passar silêncio por reprodução real.
- `src/schedule.js:19-22,45-64,82-92`: modo opt-in separado do legado, programas integrais, abertura seguida diretamente do primeiro vídeo, links entre programas e sobra explícita. Dados atuais usam `block-opening-short-links`. Boot busca JSON com `cache:'no-cache'`; alterações são carregadas ao recarregar a página, não por hot reload durante uma sessão (`src/app.js:264-274`). Meia-noite usa cálculo do ciclo por relógio absoluto.
- `tools/build.py:17-35`, `src/compat.js`: bundle IIFE preserva JSON editável e adiciona shims selecionados; alvo de sintaxe não implica suporte de toda API DOM/CSS em televisores antigos. Não foi identificado bypass de teste no código examinado.

## Honestidade das evidências e limites

`tests/production_live.py:11-17,23-25,30-50` usa YouTube real e wrapper observacional de `YT.Player`, não uma implementação fake. O relógio externo é simulado e os limites de slot são avançados artificialmente: não constitui soak test de 24 horas. Exige duas amostras crescentes, estado playing, ID e duração compatíveis, três modos e próxima atração automática no modo B; uma exceção torna o resultado negativo. A proximidade ao offset solicitado é registrada, mas não possui assert explícito de tolerância temporal.

A evidência preexistente `docs/evidence/launch/presentation-live.json` registra os três modos confirmados e próxima atração no B confirmada, sem pageErrors, com amostras reais crescentes e teste de cinco pontos descobertos do iframe. Foi lida, **não regenerada nem reexecutada**. Cinco pontos não provam ausência de qualquer obstrução em toda a superfície ou em todos os viewports. A alegação anterior de FFmpeg e áudio real não foi reexecutada nesta revisão; os 46 testes Node, isoladamente, não a provam.

**Samsung física não testada. Chrome 69 físico não testado. Não há certificação legal, de direitos, de política YouTube ou de dispositivo.** A inspeção confrontou o comportamento com referências oficiais de Required Minimum Functionality, Developer Policies Guide e parâmetros do player; análise técnica não substitui revisão jurídica. Git informou que este diretório não é repositório Git: sem comparação histórica via diff. Nenhum código, dado, build, dependência ou evidência foi editado; única entrega autorizada: este documento.
