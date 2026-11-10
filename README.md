# DISK TELEVISION 0.3 — CH 99

Emissora pessoal estática: a grade depende do relógio, não do momento em que você abre a página. Não há catálogo para selecionar nem servidor de vídeo próprio.

Lançamento 0.3: três apresentações A/B/C, sete blocos, abertura única de 18 segundos e links de quatro segundos entre programas, trilhas originais MP3/WAV e grade reorganizada para no máximo dois episódios seguidos da mesma série. O catálogo permanece com 48 vídeos anteriormente verificados; os oito títulos prioritários receberam nova auditoria sem inclusão de uploads não comprovados. Estado desta entrega: `docs/LAUNCH-REPORT.md`; fontes e pendências: `docs/LAUNCH-CONTENT-AUDIT.md`. Os relatórios DT-001/DT-002 são históricos.

## Abrir localmente

No Windows, dê dois cliques em `ABRIR-LOCAL.cmd`: ele inicia um servidor somente em 127.0.0.1 e abre o navegador depois de reservar a porta. Feche a janela ou use Ctrl+C para desligar. Se a porta 8080 estiver ocupada, rode `python tools/serve.py --port 8081`.

Requer Python 3 apenas para servir os arquivos durante o desenvolvimento. Alternativamente, na pasta do projeto:

    python -m http.server 8080 --bind 127.0.0.1

Abra http://127.0.0.1:8080 e escolha “Sintonizar CH 99”. Não abra index.html por file://: o navegador precisa carregar os JSON por HTTP(S). O servidor local não faz parte da solução publicada e pode ser desligado depois da publicação no GitHub Pages.

Windows: se `python` não estiver disponível, tente `python3` ou `py`. O aplicativo publicado não requer Python, Node, instalação ou computador ligado.

## Como funciona

- HTML, CSS e JavaScript nativos. O desenvolvimento usa módulos; a produção empacota a aplicação com esbuild, alvo de sintaxe Chrome 69 e pequenos fallbacks. O espectador não precisa de Node ou dependências de build; o YouTube continua sendo externo.
- `data/catalog.json`: vídeos e metadados editáveis.
- `data/schedule.json`: época, ciclo de 86400 segundos, blocos editoriais e rotações.
- `src/schedule.js`: compila cada bloco em vinhetas e vídeos completos. O restante vira continuidade original; não cortamos um filme para fechar o bloco.
- `src/playout.js`: estados do player, timeout e recuperação no próximo horário.
- `src/app.js`: player oficial, receptor, guia, controle remoto e vinhetas.
- `assets/logo.svg`: fonte vetorial editável; `assets/logo.png`: exportação transparente real.

A época da grade deve corresponder à meia-noite de Brasília. Os horários se repetem diariamente; o dia é calculado a partir de milissegundos UTC. O relógio do dispositivo é a fonte de tempo. Não há sincronização com relógio remoto. Pausar um vídeo não pausa a emissora; “Ressintonizar” retorna ao momento atual.

## GitHub Pages: publicação autorizada pelo proprietário

O status verificável da publicação fica em `docs/LAUNCH-REPORT.md`. A autorização da conta GitHub é uma etapa de implantação, não login do espectador.

Repositório desta instância: https://github.com/caiomwn/disk-television. Organização de implantação: `main` conserva as fontes e a documentação; `gh-pages` recebe somente o conteúdo de `_site/`. Para alterar dados diretamente no site, edite os JSON da branch `gh-pages`; mantenha as mesmas mudanças em `main` para não perdê-las na próxima geração. O procedimento manual abaixo usa `main` apenas quando o repositório contém exclusivamente o runtime.

1. Crie um repositório no GitHub, ou use um repositório vazio de sua propriedade.
2. Extraia `dist/disk-television-0.3-pages.zip` e envie seu conteúdo ao repositório. Esse pacote já contém apenas o runtime de produção. Alternativamente, envie o conteúdo de `_site/` (não a pasta envolvente). Não envie `.venv/`, `node_modules/`, credenciais ou o ZIP fechado como único arquivo.
3. Em Settings → Pages, selecione “Deploy from a branch”, branch `main`, pasta `/ (root)`, e salve.
4. Aguarde o deploy do GitHub Pages e abra a URL informada nessa tela.
5. Teste a URL HTTPS no computador e depois na TV. Confirme áudio, tela cheia, guia e mudança automática de atração.

Antes da publicação pública, revise `legal.html`, confirme que descreve sua configuração e inclua o canal de contato público do operador. Os termos e a privacidade estão acessíveis antes de sintonizar e permanentemente fora do iframe; isso não constitui certificação jurídica. O site não solicita login ou autorização OAuth.

O GitHub documenta a configuração oficial de publicação.[3] Não é necessário workflow próprio, chave de API, backend ou autenticação para o espectador. Todos os caminhos dos recursos são relativos, para funcionar em `/disk-television/`. Para regenerar `_site/`: instale Node e Python, rode `npm ci`, depois `python tools/build.py`. Para validar e empacotar: `python tools/check.py --browser --live` e `python tools/package.py`; os testes de navegador/PNG precisam de `requirements-dev.txt` e Chrome. Após a publicação, o computador local pode ser desligado.

## Editar conteúdo sem reconstruir o site

1. Inclua um objeto em `data/catalog.json`, mantendo o mesmo formato dos demais. Escolha `id` único, `youtubeId` real de 11 caracteres, título, criador, ano, duração em segundos, idioma, descrição e origem verificável.
2. Confirme a duração e teste o vídeo no player incorporado a partir da URL publicada. Um vídeo abrir no YouTube não comprova incorporação ou disponibilidade na TV/região.
3. Acrescente esse `id` à `rotation` de um bloco em `data/schedule.json`.
4. O conteúdo e suas vinhetas precisam caber completos no bloco. A aplicação valida e apresenta erro de configuração se isso não ocorrer.
5. Envie somente os JSON alterados ao repositório; nenhuma recompilação é necessária. Mudanças na duração ou ordem alteram os horários dos programas seguintes a partir do próximo carregamento da página.

`start` é contado em segundos desde meia-noite: por exemplo, 21600 corresponde a 06h. Os blocos devem começar em zero, estar ordenados e preencher o ciclo. No modo `block-opening-short-links`, `blockOpeningSeconds` controla a abertura e `programmeLinkSeconds` o link curto. `idents` preserva o modo legado sem a flag. Repetições declaradas são intencionais; a validação editorial verifica progressão, limites diários e consecutividade.

## Operação

- Enter/OK ativa o botão em foco.
- Setas alternam o foco entre controles; no guia, cima/baixo rolam a grade.
- G abre e fecha o guia; Esc/Voltar fecha o guia.
- Tab continua disponível no computador.
- “Apresentação” permite comparar A (Clean, barras recolhidas após inatividade), B (Broadcast Frame) e C (Experimental, composição externa). A escolha dura a sessão da aba. Setas e Voltar/Esc também funcionam nesse diálogo.
- O foco dentro do iframe pertence ao YouTube: o site não intercepta teclas dentro dele. Use Tab/Shift+Tab ou o cursor da TV para sair.
- “Som ligado/desligado” controla o player e as pequenas assinaturas sonoras originais.
- “Tela cheia” tenta a API do navegador. TVs podem não permitir: nesse caso use o modo da própria TV.

O guia substitui visualmente a transmissão e interrompe o player enquanto está aberto; ao fechar, ressintoniza pelo relógio. Não há reprodução escondida nem interface sobreposta sobre os controles/anúncios do YouTube.[2]

## Vinhetas

As vinhetas ocupam slots reais da grade: cada bloco abre uma vez com animação própria de 18 segundos e identificação do bloco; entre atrações há um único link de quatro segundos. Três composições instrumentais originais (station, next, night) foram sintetizadas offline e distribuídas em MP3 com fallback WAV. Web Audio decodifica os arquivos locais, entra pelo offset atual e para no vídeo, mute, guia ou comparação de apresentações. Falha de áudio não para o canal. O modo de movimento reduzido conserva a identificação estática. Não há locução nem piloto cinematográfico CYBERIA nesta versão; isso não bloqueou o lançamento. Autoria, medições e reprodução: `docs/LAUNCH-AUDIO.md`.

## Limitações importantes

- Browser e YouTube decidem autoplay/áudio; o evento de bloqueio exige uma interação quando necessário.[1]
- Incorporamos vídeos no player oficial. Não baixamos, retransmitimos, removemos anúncios, escondemos controles ou re-hospedamos obras.
- URLs, direitos, região, anúncios, legendas e disponibilidade podem mudar. O catálogo não constitui licença sobre as obras. Não há garantia permanente de incorporação.
- Vídeo que falha ou encerra antes do slot vira continuidade até o próximo horário. A aplicação não pula o relógio para antecipar outra atração.
- YouTube pode inserir anúncios ou atrasar o seek; o início é aproximado, não sincronização de broadcast em nível de quadro. Não corrigimos o playhead continuamente para não interferir em anúncios ou ações do player.
- Não existe garantia de operação offline. As vinhetas são locais, mas os vídeos precisam de internet e acesso ao YouTube.
- Se o player ficar com metade ou menos da área visível, a reprodução é suspensa e novos loads são adiados. Ao voltar à imagem, a emissora ressintoniza o horário atual. Isso também evita reprodução oculta ao rolar telas pequenas.
- Samsung/Tizen e outras Smart TVs não são homologadas sem teste físico. O bundle de produção remove a necessidade de módulos e transpila para sintaxe Chrome 69, mas isso não emula o motor da TV nem garante `fetch`, Intl/timezone, Web Audio ou a API atual do YouTube no seu modelo.
- A edição editorial oferece janelas de estreia e reprises, não temporadas completas. Há 48 vídeos verificados em desktop; a disponibilidade de muitos favoritos retrô permaneceu bloqueada ou insuficientemente comprovada. Veja `docs/DT-002-UNAVAILABLE.md`.

## Documentação adicional

- `docs/RESEARCH.md`: projetos avaliados, licenças e decisões.
- `docs/CATALOG.md`: origem e verificação do acervo.
- `docs/IDENTITY.md`: identidade e arquivos gráficos.
- `docs/TEST-RESULTS.md`: execução real, evidências e limites dos testes.

## Sources

[1] https://developers.google.com/youtube/iframe_api_reference
[2] https://developers.google.com/youtube/terms/required-minimum-functionality
[3] https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
