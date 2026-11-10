# DISK TELEVISION — pesquisa técnica e decisões

**Consulta:** 10 de novembro de 2026. **Escopo:** emissora fictícia **CH 99**, executada no navegador, publicável no GitHub Pages, sem backend próprio. Esta é pesquisa documental: **nenhuma demo foi testada**, nenhum player foi executado e nenhum vídeo teve disponibilidade/reprodução verificada. Não foi copiado código dos projetos.

## Resultado executivo

**Decisão de projeto:** implementar do zero HTML/CSS/JavaScript e um catálogo estático de programas, com grade determinística ancorada numa época UTC. Usar a YouTube IFrame Player API para vídeos do YouTube, sem baixar, retransmitir ou transcodificar. Isso mantém a aplicação compatível com hospedagem estática; GitHub Pages serve HTML, CSS e JavaScript de um repositório.[40][44]

Os sete candidatos existem na API pública. `f00d4tehg0dz/retroarr` resolve para **f00d4tehg0dz/surfarr**. Os mais próximos da arquitetura desejada são **myrtv**, **InterDemTV** e **TV-From-Childhood**; apenas o último possui licença MIT confirmada por arquivo entre esses três.[1][4][7]

**Restrição decisiva:** não colocar logo CH 99, scanlines, vidro CRT, ruído, legenda própria, moldura ou cartão de carregamento por cima de nenhuma parte do iframe YouTube. A política proíbe sobreposições inclusive sobre controles. A identidade deve ficar fora do retângulo do player; bumper próprio deve substituir o player após sua remoção, não cobri-lo.[41]

## Método e limites

Consulta direta por HTTPS à API GitHub: metadados, README, árvore recursiva da branch padrão e endpoint `/license`; leitura pontual de arquivos relevantes via `raw.githubusercontent.com`; documentação oficial Google/YouTube e GitHub. O JSON irmão registra URLs, respostas, branch e SHA da árvore consultada. A árvore não é um teste executável nem prova de que todas as dependências funcionem. O timestamp `pushed_at` não demonstra manutenção ou qualidade.

As arquiteturas abaixo são observações de README/árvore e, quando indicado, código inspecionado. **“Adequado ao Pages” é inferência de arquitetura, não deploy validado.** Todos os endereços de demo são somente os declarados pelos mantenedores. Não foram abertos nem testados.

Ausência de licença é tratada explicitamente: repositório público não implica autorização geral para copiar/modificar/distribuir; a documentação do GitHub explica que, sem licença, aplicam-se os direitos autorais padrão. Licença do código também não concede direitos sobre vídeos, marcas, fontes ou imagens de terceiros.[45]

## 1. Sete candidatos

### 1. myrtv/myrtv.github.io

- **Existência:** confirmada; branch `master`; homepage declarada: https://myrtv.github.io/ — **demo não testada**.[1]
- **Licença:** **ausente para a aplicação**. API sem licença reconhecida, `/license` respondeu 404 e não há LICENSE raiz na árvore. A licença de jQuery UI encontrada em dependência não licencia o projeto.[1][3]
- **Arquitetura:** HTML/CSS/JS com jQuery/Moment e playlists JSON. README descreve pseudo-live por época e ciclo; `js/site.js` confirma cálculo temporal e seek. Suporta YouTube, Dailymotion e links diretos.[2][47]
- **Relevância/decisão:** referência conceitual principal para “entrar no meio do programa”, sem transmissão contínua. Reimplementar algoritmo e identidade próprios; não importar código sem permissão.

### 2. jumpjumptiger007/interdimensional-cable — InterDemTV

- **Existência:** confirmada; branch `main`; demo declarada: https://tv.yliu.tech/ — **não testada**.[4]
- **Licença:** **ausente**; API sem licença e nenhum arquivo de licença na árvore; `/license` respondeu 404.[4][6]
- **Arquitetura:** HTML/CSS/JS puros, IFrame API, `videos.json`, Three.js/WebGL opcional e service worker. README apresenta receptor CRT, remoto, teclado, modos aleatório/sequencial e ponto inicial aleatório em vídeos longos; `app.js` confirma API e seleção aleatória.[5][48]
- **Relevância/decisão:** boa referência de interação e fallback visual; “surf aleatório” não é o mesmo que emissora com grade global. Não copiar código/arte; não reproduzir efeitos sobre o iframe.

### 3. f00d4tehg0dz/retroarr → f00d4tehg0dz/surfarr

- **Existência:** URL antiga resolve para **surfarr**; branch `main`; homepage declarada: https://www.surfarr.tv — **não testada**.[7]
- **Licença:** **GPL-3.0** reconhecida e LICENSE recuperado; não é licença permissiva equivalente a MIT.[10]
- **Arquitetura:** frontend React/Vite e backend Node/Express, Docker, FFmpeg e yt-dlp; M3U, XMLTV e HDHomeRun; catálogo/API separados. Não é só uma página estática.[8][9][49]
- **Relevância/decisão:** usar apenas ideias de guia, canais e fillers; rejeitar stack de servidor, downloads e transcodificação para este escopo.

### 4. reedylab/channelarr

- **Existência:** confirmada; branch correta **`master`**, não `main`; sem homepage de demo declarada no metadado consultado. Nenhuma demo testada.[11]
- **Licença:** **ausente/incompleta**. README diz MIT, mas API não reconhece licença, `/license` respondeu 404 e a árvore não contém LICENSE. Não registrar “MIT confirmada”.[11][12][13]
- **Arquitetura:** FastAPI/Uvicorn/Jinja2, FFmpeg/HLS, yt-dlp e agenda materializada; pré-download de vídeos do YouTube. README descreve armazenamento JSON sem banco, mas requirements atual inclui SQLAlchemy/psycopg2 e a árvore contém módulos de banco: documentação e implementação divergem; persistência exata não auditada.[12][13][51]
- **Relevância/decisão:** referência de agenda e bumps. Rejeitar runtime e cache/download; não cabe no Pages e não transferir práticas de download para integração YouTube.

### 5. samjhill/channel

- **Existência:** confirmada; branch `main`; sem homepage de demo no metadado; nenhuma demo testada.[14]
- **Licença:** **ausente**. README mantém placeholder de licença; API sem licença, `/license` 404 e árvore sem LICENSE.[14][15][16]
- **Arquitetura:** geração de playlist e bumpers em Python, FFmpeg/HLS, nginx, FastAPI e painel React, execução Docker e arquivos de mídia locais.[15][16]
- **Relevância/decisão:** inspiração de intervalos, “a seguir” e identidade de emissora; não usar infraestrutura. A sobreposição de marca descrita para stream próprio não autoriza overlay sobre player YouTube.

### 6. work-partner/TV-From-Childhood

- **Existência:** confirmada; branch `main`; demo declarada: https://tv-from-childhood.vercel.app — **não testada**.[17]
- **Licença:** **MIT confirmada** por API e arquivo LICENSE. Não houve reutilização de código.[20]
- **Arquitetura:** um `index.html` com CSS/JavaScript e IFrame API. Código inspecionado contém catálogo de durações, época global e resolução do programa/offset pelo relógio.[19][46]
- **Relevância/decisão:** maior proximidade estrutural ao Pages. Porém contém camada que cobre iframe fora do estado playing para esconder interface nativa: não reproduzir; conflita com a decisão conservadora de conformidade. Alegação de “fair use” do README/HTML não valida direitos sobre o catálogo.[41][46]

### 7. jpsilvashy/channel-surfer

- **Existência:** confirmada; branch `main`; sem homepage de demo no metadado. Nenhuma demo testada.[21]
- **Licença:** **ausente/incompleta**. README afirma MIT e remete a LICENSE inexistente na árvore; API sem licença e `/license` respondeu 404.[21][22][23]
- **Arquitetura:** React/Vite/Tailwind no frontend; Express serve diretório de vídeos; README/árvore incluem componentes Rust. Não foi verificada a integração entre esses componentes.[22][23][50]
- **Relevância/decisão:** referência de guia visual anos 1990, não base sem backend; não copiar implementação nem fonte tipográfica sem licença específica.

## 2. Alternativas verificadas

| Alternativa real | Licença confirmada | Arquitetura observada | Decisão para CH 99 |
| --- | --- | --- | --- |
| https://github.com/ErsatzTV/ErsatzTV → https://github.com/ErsatzTV/legacy | Zlib | Servidor de biblioteca, grade, IPTV/EPG e transcodificação.[24][25][27] | Referência de programação; rejeitar runtime no Pages. |
| https://github.com/ErsatzTV/next | MIT | Motor Rust auto-hospedado; playout JSON, HLS/M3U/XMLTV; agendamento/biblioteca fora de escopo.[28][29][31] | Inspira contrato de agenda; não resolve hospedagem estática. |
| https://github.com/vexorian/dizquetv | Zlib | Canais de biblioteca Plex, fillers, guia XMLTV, M3U/HDHomeRun, Docker/binários.[32][33][35] | Referência de fillers e guia; exige servidor. |
| https://github.com/chrisbenincasa/tunarr | Zlib | Servidor auto-hospedado, bibliotecas Plex/Jellyfin/Emby/locais, agenda e transcodificação.[36][37][39] | Alternativa se backend vier a ser permitido; não neste escopo. |

As árvores consultadas de ErsatzTV legacy/next e dizqueTV confirmam a organização dos respectivos projetos.[26][30][34]

A árvore de Tunarr também foi recuperada sem truncamento.[38]

O README de TV-From-Childhood é breve e não detalha a implementação; a análise acima usa o HTML inspecionado.[18]

Todas as alternativas acima tiveram metadados, README, árvore e licença consultados, **sem instalação e sem testes de demo**. Uma tentativa em `Tunarr/tunarr` retornou 404; o endereço efetivamente verificado é `chrisbenincasa/tunarr`. Uma sondagem em `ShaneMcC/YouTubeTV` também retornou 404; não foi promovida a alternativa existente. HTTP 404 isolado não prova inexistência universal de um projeto: pode indicar URL incorreta, renomeada ou acesso indisponível.

**Alternativa escolhida:** aplicação original estática com API oficial. Escolha de escopo, não avaliação de superioridade geral desses projetos.

## 3. YouTube: contrato de reprodução e conformidade

### API, autoplay e identificação

- Usar `https://www.youtube.com/iframe_api`, aguardar `onYouTubeIframeAPIReady` e `onReady`, criar um único `YT.Player`. Controles externos só chamam métodos documentados. Não é necessário adicionar backend para executar esse player no navegador.[40]
- **Autoplay não é garantido.** `onAutoplayBlocked` existe e cobre tentativas por `autoplay`, `playVideo` e funções de load. Decisão: botão explícito **LIGAR / REPRODUZIR**, tentativa inicial muda somente quando permitida e mensagem acionável fora do player; nunca loop infinito de `playVideo`.[40]
- O player precisa estar visível; a regra de autoplay exige mais da metade visível e no máximo um player autoplay simultâneo. Iframe tem mínimo de **200 × 200 px**; para 16:9 a documentação recomenda pelo menos 480 × 270 px.[41]
- Definir `origin: location.origin`, `playsinline: 1`, manter controles oficiais e não suprimir Referer. A política recomenda `strict-origin-when-cross-origin`; `origin` não substitui automaticamente o cabeçalho Referer. Testar em HTTP local e HTTPS publicado, não concluir pelo `file://`.[40][41][42]

### Seek e grade pseudo-live

`loadVideoById({videoId, startSeconds})` permite entrada no ponto da grade. `seekTo(segundos, true)` admite nova busca fora do buffer; a posição pode cair no keyframe anterior, portanto não há sincronismo frame-exato. `getDuration()` pode retornar zero antes dos metadados; em live retorna tempo transcorrido, não duração fechada. Não construir a grade inicial esperando esse valor.[40]

**Decisão de algoritmo original:** catálogo versionado com `videoId`, título, duração validada, ponto inicial/final e origem; época UTC fixa; posição igual ao tempo desde época módulo duração total do ciclo. Localizar intervalo por acumulados e calcular offset do trecho. Validar durações positivas e nunca usar duração ausente como zero. Isso é especificação a implementar, não código copiado.

Ao voltar de aba suspensa ou atravessar fronteira de programa, recalcular pelo relógio atual, não apenas contar timers. Definir tolerância para drift e não disputar cada ajuste manual do usuário. Uma página estática usa o relógio do dispositivo: sincronismo entre espectadores é aproximado, sem garantia de horário autoritativo. Buffer, anúncios, keyframes e políticas do navegador também impedem promessa de broadcast contínuo sem interrupções.[40][42]

### Erros: não confundir falha com autoplay bloqueado

| Evento/código oficial | Significado | Decisão de interface |
| --- | --- | --- |
| `onAutoplayBlocked` | Navegador bloqueou início automático/scriptado. | Pedir clique; não declarar vídeo removido. |
| `2` | Parâmetro inválido, incluindo ID inválido. | Reportar erro de catálogo; limitar retentativas. |
| `5` | Falha de player HTML5/conteúdo. | Oferecer tentar novamente e abrir no YouTube. |
| `100` | Vídeo removido/não encontrado ou privado. | Sinalizar indisponibilidade; oferecer próximo item. |
| `101` / `150` | Proprietário proibiu embed. | Não contornar; abrir página original ou outro item. |
| `153` | Referer/identificação do cliente ausente. | Corrigir identificação/política; não tentar proxy/bypass. |

Significados e evento constam na referência oficial; ações são decisões do projeto.[40]

**Fallback proposto:** estado explícito fora do player com diagnóstico e ações “tentar”, “próximo” e “abrir no YouTube”; transições finitas, timeout e opção de abandonar. Se escolher fallback de vídeo, o estado exibido deve informar que saiu da grade — não fingir sincronismo. Se for usar cartão tela inteira, destruir/remover o iframe primeiro.

### Overlay, marca e conteúdo

A política proíbe elementos à frente de **qualquer parte** do player. `pointer-events: none`, transparência, intenção estética ou ausência de monetização não criam exceção. Logo CH 99, relógio, “NO AR”, OSD e guia ficam em áreas externas; CRT e ruído ficam na carcaça/fundo. Não recortar/esticar o iframe para ocultar interface. Os padrões de overlay de outros repositórios não constituem aprovação pelo YouTube.[41]

`modestbranding` foi descontinuado e não resolve marca; `rel=0` não elimina relacionados, apenas restringe ao mesmo canal. Não prometer remover logo, anúncios, recomendações ou interface oficial. Não baixar/cachear audiovisual do YouTube para “estabilizar o sinal”; as políticas restringem download, armazenamento e playback offline sem aprovação.[42][43]

Catálogo público não implica direito de retransmissão ou licença de obra. Privacidade exige revisão: autoplay já provoca compartilhamento de dados; políticas também estabelecem deveres para vídeos “Made for Kids”. Decisão: catálogo curado e revisão de direitos/classificação antes de publicar, sem alegar que um aviso de fã ou “fair use” resolve a questão. Não se verificou a classificação individual de vídeos nesta pesquisa.[43]

## 4. Decisões consolidadas e verificação pendente

1. **Aceitar:** arquivos estáticos, catálogo local versionado, epoch UTC, grade/“agora e a seguir”, teclado e remoto acessíveis, botão de ligar e estados recuperáveis.
2. **Rejeitar:** Docker, FFmpeg, yt-dlp, Express/FastAPI em runtime, API privada, proxy de vídeo, segredo no navegador e promessa de serviço offline para vídeos YouTube.
3. **Identidade DISK TELEVISION / CH 99:** criação original. Bumpers próprios em segmentos separados; nenhuma camada sobre player YouTube. Não copiar logos, fontes, screenshots, código ou catálogos de terceiros.
4. **Se for indispensável aplicar CRT/logomarca sobre o vídeo:** usar material próprio/licenciado reproduzido em HTML5 com os direitos necessários; não tratar iframe YouTube como textura editável. Isso requer revisão específica de mídia e hospedagem.
5. **Antes do lançamento:** executar testes reais em Chrome/Firefox/Safari e celular; autoplay negado, rede ausente, consentimento, anúncios, embed bloqueado, erro 153, retomada de aba, relógio incorreto, troca de programa, subcaminho GitHub Pages, teclado/foco e redução de movimento. Esses testes **não foram executados** nesta pesquisa.
6. **Publicação GitHub Pages não realizada:** nenhuma credencial usada, nenhum deploy, nenhum backend criado. A compatibilidade descrita é uma decisão arquitetural fundamentada, não selo de funcionamento.

## Implementação resultante

A edição 0.1 adotou a arquitetura estática original, o relógio determinístico e as vinhetas separadas. Não reutilizou código dos candidatos. Ao contrário de algumas ações apenas propostas nesta pesquisa, o receptor final não oferece “pular para próximo”: mantém continuidade até o próximo horário para preservar a grade. A reconexão à API é tentada novamente na atração seguinte sem exigir escolha manual. Os testes de aplicação e player realizados depois da pesquisa estão em `TEST-RESULTS.md`; as ressalvas “não testado” acima descrevem somente as demos e o escopo desta pesquisa documental.

## Evidência estruturada

Ver `../research-evidence.json`: sete candidatos, quatro alternativas verificadas, tentativas malsucedidas, respostas HTTP, URLs primárias, licença e limitações. Não contém implementação copiada dos projetos.

## Sources

[1] https://api.github.com/repos/myrtv/myrtv.github.io
[2] https://api.github.com/repos/myrtv/myrtv.github.io/readme
[3] https://api.github.com/repos/myrtv/myrtv.github.io/git/trees/master?recursive=1
[4] https://api.github.com/repos/jumpjumptiger007/interdimensional-cable
[5] https://api.github.com/repos/jumpjumptiger007/interdimensional-cable/readme
[6] https://api.github.com/repos/jumpjumptiger007/interdimensional-cable/git/trees/main?recursive=1
[7] https://api.github.com/repos/f00d4tehg0dz/retroarr
[8] https://api.github.com/repos/f00d4tehg0dz/surfarr/readme
[9] https://api.github.com/repos/f00d4tehg0dz/surfarr/git/trees/main?recursive=1
[10] https://api.github.com/repos/f00d4tehg0dz/surfarr/license
[11] https://api.github.com/repos/reedylab/channelarr
[12] https://api.github.com/repos/reedylab/channelarr/readme
[13] https://api.github.com/repos/reedylab/channelarr/git/trees/master?recursive=1
[14] https://api.github.com/repos/samjhill/channel
[15] https://api.github.com/repos/samjhill/channel/readme
[16] https://api.github.com/repos/samjhill/channel/git/trees/main?recursive=1
[17] https://api.github.com/repos/work-partner/TV-From-Childhood
[18] https://api.github.com/repos/work-partner/TV-From-Childhood/readme
[19] https://api.github.com/repos/work-partner/TV-From-Childhood/git/trees/main?recursive=1
[20] https://api.github.com/repos/work-partner/TV-From-Childhood/license
[21] https://api.github.com/repos/jpsilvashy/channel-surfer
[22] https://api.github.com/repos/jpsilvashy/channel-surfer/readme
[23] https://api.github.com/repos/jpsilvashy/channel-surfer/git/trees/main?recursive=1
[24] https://api.github.com/repos/ErsatzTV/ErsatzTV
[25] https://api.github.com/repos/ErsatzTV/legacy/readme
[26] https://api.github.com/repos/ErsatzTV/legacy/git/trees/main?recursive=1
[27] https://api.github.com/repos/ErsatzTV/legacy/license
[28] https://api.github.com/repos/ErsatzTV/next
[29] https://api.github.com/repos/ErsatzTV/next/readme
[30] https://api.github.com/repos/ErsatzTV/next/git/trees/main?recursive=1
[31] https://api.github.com/repos/ErsatzTV/next/license
[32] https://api.github.com/repos/vexorian/dizquetv
[33] https://api.github.com/repos/vexorian/dizquetv/readme
[34] https://api.github.com/repos/vexorian/dizquetv/git/trees/main?recursive=1
[35] https://api.github.com/repos/vexorian/dizquetv/license
[36] https://api.github.com/repos/chrisbenincasa/tunarr
[37] https://api.github.com/repos/chrisbenincasa/tunarr/readme
[38] https://api.github.com/repos/chrisbenincasa/tunarr/git/trees/main?recursive=1
[39] https://api.github.com/repos/chrisbenincasa/tunarr/license
[40] https://developers.google.com/youtube/iframe_api_reference
[41] https://developers.google.com/youtube/terms/required-minimum-functionality
[42] https://developers.google.com/youtube/player_parameters
[43] https://developers.google.com/youtube/terms/developer-policies
[44] https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
[45] https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
[46] https://raw.githubusercontent.com/work-partner/TV-From-Childhood/main/index.html
[47] https://raw.githubusercontent.com/myrtv/myrtv.github.io/master/js/site.js
[48] https://raw.githubusercontent.com/jumpjumptiger007/interdimensional-cable/main/app.js
[49] https://raw.githubusercontent.com/f00d4tehg0dz/surfarr/main/server/package.json
[50] https://raw.githubusercontent.com/jpsilvashy/channel-surfer/main/server.js
[51] https://raw.githubusercontent.com/reedylab/channelarr/master/requirements.txt
