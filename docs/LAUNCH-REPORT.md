# DISK TELEVISION 0.3 — OPERAÇÃO CH 99

Data: 10 de novembro de 2026. Projeto preservado em `C:/Users/padoka77/disk-television`.

## Estado de lançamento

**DISK TELEVISION 0.3 — CH 99 ON AIR.** URL pública verificada: https://caiomwn.github.io/disk-television/. Repositório: https://github.com/caiomwn/disk-television. Autenticação confirmada na conta caiomwn; repositório criado vazio, sem sobrescrever trabalho preexistente. Fontes em `main`; runtime em `gh-pages`.

Não houve teste em Samsung física; não há alegação de homologação.

Backup anterior à retomada: `C:/Users/padoka77/disk-television-backups/LAUNCH-before-20261110-185850/project.zip`, com manifesto e integridade verificada. Os backups DT-002 e DT-003 também foram mantidos.

## Entrega funcional

- A / CLEAN: imagem ampliada; barras recolhem após 4,5 segundos de inatividade. Controle de retorno fica fora do player.
- B / BROADCAST FRAME: apresentação padrão, barras mais compactas e informações agora/próximo.
- C / EXPERIMENTAL: composição editorial e marcas externas. Nada depende de acesso aos pixels do YouTube.
- Comparação antes ou depois da sintonia, teclado/setas/Voltar, preferência de sessão da aba. Guia e comparação param vídeo e áudio; o retorno recalcula o horário.
- Grade ancorada à meia-noite de Brasília, ciclo de 86.400 segundos, atualização/reabertura sem reinício.
- Sete aberturas de bloco com 18 segundos, 82 links de quatro segundos e sete sobras explícitas; não há dupla vinheta obrigatória antes de cada episódio.
- 185 slots: 89 exibições completas de vídeo e 96 slots de continuidade. Catálogo com 48 obras/episódios, 46 distintos usados. Nenhuma obra nova foi acrescentada artificialmente.
- No máximo dois episódios consecutivos da mesma série; progressão, reprises declaradas, limites diários e ausência de obras idênticas imediatamente adjacentes validados.
- Logotipo PNG RGBA real e fonte SVG editável; identidade DISK TELEVISION / CH 99 preservada.
- Três composições instrumentais originais: station (8 s), next (2,6 s), night (11 s); MP3 com fallback WAV. Entrada no offset atual, sem reinício por tick nem loop após o fim natural. Áudio para em vídeo, mute, guia, apresentação e perda de visibilidade.
- Falhas de vídeo mantêm a continuidade original até o próximo horário, sem congelar a grade. Bloqueio de autoplay oferece Ressintonizar.

As aberturas são animações web com identificação do bloco e continuidade original. O piloto cinematográfico de CYBERIA com locução permanece pendente e não foi usado como requisito de publicação.

## QA realmente executado

`tools/check.py --browser --live`: **75 testes, todos aprovados**, mais dois diagnósticos reais de rede aprovados. Log integral: `docs/evidence/test-run.json`. Métricas reproduzíveis: `tools/report_launch.py` → `docs/evidence/launch/metrics.json`.

- 52 Node: relógio/grade/player/áudio, contrato legado, modo novo e alinhamento inicial limitado. Varredura de cada segundo das 24 horas; isso não é uma sessão de reprodução com 24 horas de duração.
- 4 assets, 1 launcher, 1 validador de evidência de embed.
- 9 regressões de navegador, 2 integração editorial, 3 apresentações, 1 build, 1 bundle de produção e 1 Web Audio real.
- Testes determinísticos usam um duplo explícito somente da API externa quando necessário. Não são apresentados como reprodução real do YouTube.
- `tests/live_player.py`: player oficial real, Tears of Steel → vinhetas → Elephants Dream, vídeo correto e tempo avançando, sem segundo clique. Esse é o fixture legado DT-001.
- `tests/production_live.py`: build `_site`, dados atuais e player oficial real nos três modos A/B/C, offset solicitado de 30 segundos, duração correta e duas amostras crescentes. Em B, Echoes of Memory → link curto → The Hole sem novo clique. Iframe desobstruído no centro e nos quatro cantos.
- `tests/audio_browser_test.py`: MP3 local realmente decodificado e iniciado no Chrome via Web Audio; offsets 2/5/6/7, mute, guia e comparação. YouTube é duplo nesse teste; o áudio não. Evidência: `docs/evidence/launch/audio-browser.json`.
- Os seis arquivos de áudio também receberam decode integral FFmpeg, ffprobe, volume e verificação determinística de hashes. Medições e limites em `docs/LAUNCH-AUDIO.md`; não houve escuta humana documentada.
- Capturas de produção: `docs/evidence/launch/player-{A,B,C}.png`, `tuning.png` e `programme-link.png`.

## Revisão independente

`docs/LAUNCH-REVIEW.md`: zero P0/P1 reproduzidos no escopo. Revisor executou 46 testes Node e o teste browser de produção, conferiu manifesto e reproduziu o bundle em memória. Observação P2 sobre pacotes antigos foi tratada gerando e comparando o ZIP Pages 0.3 (21 membros idênticos ao stage); arquivos 0.1/0.2 ficam preservados apenas como históricos. Após a revisão, o coordenador também validou setas e Voltar com `key='Unidentified'`/keyCode e reexecutou toda a suíte. Isso não é prova de ausência universal de bugs, conformidade jurídica ou homologação física de TV.

## Build e publicação

Pages relido com status `built`, branch `gh-pages`, raiz `/`, HTTPS ativo. Workflow do commit de produção `aef4fefbc5f8e1250951816e94513d6449b6c24d` concluído com sucesso: https://github.com/caiomwn/disk-television/actions/runs/42925160223. A URL HTTPS respondeu; manifesto e 20 hashes de recursos corresponderam ao build local.

Teste adicional na origem pública, sem relógio simulado nem API falsa: Rayearth episódio 7 (`E6R2j2cablI`) carregado na posição correspondente ao horário real, com duas amostras crescentes e posição compatível com a grade. Guia e retorno confirmados; três variantes de áudio prontas e zero pageErrors. Evidência atual: `docs/evidence/launch/public-site.json` e `public-on-air.png`. Reprodução posterior: `python tools/verify_public_site.py`; aceita `gh` no PATH/variável `GH_EXECUTABLE`. Nesta execução, a consulta anônima da API de CI retornou 404, então o verificador de manutenção utilizou `gh` autenticado; os arquivos HTTPS e o player foram acessados sem login do espectador. O repositório público também respondeu HTTP 200.

Correção de implantação: o Git normalizava CRLF→LF em sete recursos textuais, invalidando hashes calculados no Windows. A diferença foi reproduzida byte a byte; o builder passou a canonicalizar LF antes de calcular hashes, com regressão validada. Também foi observada uma tentativa em que o YouTube reiniciou no zero apesar do offset. Há uma única tentativa limitada de alinhamento inicial quando o primeiro estado coerente de conteúdo começa no zero após pedido de entrada no meio; ela não faz correção periódica, não identifica/remove anúncios e não altera pausas/seeks posteriores do espectador. Anúncios e comportamento do provedor ainda impedem garantia de sincronismo em todas as tentativas.

`python tools/build.py` gera `_site/` com 21 arquivos estáticos, bundle IIFE alvo Chrome 69, caminhos relativos e manifesto SHA-256 `release.json`. Há fallbacks para globalThis, Array.at, replaceChildren e Promise.allSettled, e foco visível em motores sem :focus-visible. Esse alvo é preparo técnico, não emulação nem teste Samsung.

O build não leva `.venv`, `node_modules`, ferramentas de autenticação, pesquisa ou credenciais. Uma varredura detecta padrões de tokens e chaves privadas. Nenhum backend, computador ligado, API de IA ou serviço pago é necessário na reprodução.

`python tools/package.py` gera os ZIPs `dist/disk-television-0.3-pages.zip` (runtime) e `dist/disk-television-0.3-source.zip` (fontes). O ZIP Pages deve ser extraído na raiz da branch escolhida; não publicar a pasta envolvente `_site` nem apenas o ZIP fechado. Instruções de publicação e edição no README.

A confirmação acima incluiu leitura remota de Pages, HTTP 200 da URL, conferência de `release.json` e teste real do player nessa origem HTTPS, não apenas `git push`.

## Curadoria e direitos

Os 48 itens existentes conservam evidências anteriores de reprodução no desktop; não foram reensaiados integralmente e simultaneamente nesta retomada. Fontes e cadeias de publicador oficial/institucional estão documentadas na DT-001/DT-002. A incorporação usa exclusivamente o player oficial e não constitui download, retransmissão, licença comercial de emissora ou parecer jurídico sobre direitos.

Oito playlists-semente foram auditadas: Galaxy Angel, Azumanga Daioh, Hellsing, Dandadan, Nokotan, Slayers, Tenchi Muyo! e xxxHOLiC. **Nenhum upload novo foi publicado.** Foram separados descoberta, possibilidade técnica e evidência de autorização. Nokotan E1 tem fonte REMOW corroborada e amostra real de embed, mas permanece proposta com idioma/território/uso a confirmar; os demais uploads não tiveram autorização evidenciada. Introduções e compilação longa foram excluídas como episódios. O token Tenchi fornecido foi preservado literalmente.

Detalhes: `docs/LAUNCH-CONTENT-AUDIT.md`, `research/launch/seeds-audit.json`. Isso evita trocar qualidade e autorização por quantidade.

## Abrir na Samsung quando a URL estiver publicada

1. Conectar a TV à internet e deixar data/hora automáticas corretas; o relógio da TV determina a posição na programação.
2. Abrir o navegador Internet da Samsung e digitar a URL HTTPS confirmada do GitHub Pages.
3. Escolher B inicialmente e ativar “Sintonizar CH 99” com OK/Enter ou cursor. Se o navegador bloquear reprodução/áudio, usar Ressintonizar ou o controle oficial do player.
4. Comparar A/B/C em “Comparar A/B/C”; abrir Guia e usar Voltar para retornar ao ponto atual.
5. Ativar Tela cheia se o modelo permitir; caso contrário usar o modo de tela cheia/zoom adequado do próprio navegador, sem recortar os controles.
6. Confirmar uma mudança de atração, áudio, guia e retorno. Informar modelo/ano da TV e comportamento observado se algo falhar. Não há necessidade de manter o PC ligado depois da publicação.

## Limitações e próximos passos

- Autenticação GitHub concluída por dispositivo, sem credenciais no projeto ou nos pacotes. Códigos temporários foram mantidos fora deste relatório/site.
- Contato público real configurado em `legal.html`: conta caiomwn e Issues do repositório verificado. Privacidade descreve a preferência A/B/C de sessão.
- Samsung física, longa duração e outras redes/regiões continuam sem homologação.
- YouTube pode inserir anúncios, mudar disponibilidade ou aproximar o seek; não existe sincronização de quadro. Não há bypass regional nem ocultação de anúncios/controles.
- Depois de publicar: testar no aparelho; depois ampliar conteúdo autorizado e produzir piloto CYBERIA, sem reestruturar o núcleo funcional.
