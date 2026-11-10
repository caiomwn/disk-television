# DT-003 — Pesquisa técnica: apresentação A/B/C, YouTube e Samsung

**Consulta:** 10 de novembro de 2026. **Escopo:** decisões de apresentação e roteiro de validação; catálogo, grade e motor único DT-002 permanecem congelados. Este documento não implementa nem certifica o aplicativo. **Nenhum teste físico em Samsung foi realizado nesta pesquisa.** As recomendações abaixo são decisões de projeto, não parecer jurídico nem homologação do YouTube.

## 1. Resultado executivo e decisões A/B/C

A documentação vigente proíbe elementos visuais diante de **qualquer parte** do player incorporado, incluindo controles. Isso não se limita a anúncios ou a overlays que interceptam cliques. Portanto, `pointer-events: none`, transparência ou um pequeno logo não tornam uma sobreposição aceitável.[1]

**Decisão:** não implementar o overlay direto inicialmente investigado para C. Usar identidade em moldura/gutters inteiramente externos ao retângulo do iframe, sem cobrir vídeo, anúncios, controles, legendas, avisos, links ou interações obrigatórias. É uma alternativa de intenção visual equivalente, **não uma transmissão convencional com marca sobre o vídeo**. Essa interpretação conservadora orienta A, B e C.[1][2]

| Modo | Decisão acionável de apresentação | Critério de aceite visual |
| --- | --- | --- |
| A — CLEAN | Maximizar o iframe respeitando espaço externo para voltar, som e fullscreen. Informações temporárias aparecem somente nesse espaço reservado. | Maior vídeo possível; nenhum OSD ou botão cruza o iframe, inclusive ao surgir/desaparecer. |
| B — BROADCAST FRAME | Moldura discreta, logo e programa em linhas/colunas irmãs do iframe. | Moldura circunda, mas não invade o player; marca legível com foco de controle remoto. |
| C — EXPERIMENTAL / EXTERNAL FRAME | Composição mais expressiva, órbita/brilho e faixa informativa nos gutters externos. Nada de CRT, scanline, máscara, reflexo ou vinheta visual aplicados sobre o player. | Diferencia-se de B pela composição externa; preserva integralmente o player durante animações e fullscreen. |

**Contrato comum de projeto:** um único player e relógio; trocar modo altera layout, não catálogo, slot ou engine. Não reinstanciar o iframe só para trocar moldura. Se uma transição suspender a transmissão, retornar ao programa/offset do relógio, não ao ponto antigo. Som original é exclusivo das vinhetas próprias, nunca trilha adicional sobre vídeos do YouTube: separar ou modificar os componentes audiovisuais de conteúdo YouTube é proibido.[2]

## 2. YouTube: integração e limites verificáveis

### Área, anúncios e visibilidade

- O mínimo documentado é **200 × 200 px**; com controles é preciso espaço suficiente para exibi-los integralmente. Para 16:9, a recomendação oficial é ao menos **480 × 270 px**. Não reduzir abaixo do mínimo para acomodar gutters.[1]
- Início automático/programático exige player visível e **mais da metade** de sua área visível; apenas um player pode iniciar reprodução automática simultaneamente.[1]
- Reprodução em player de fundo, fora da página/aba/tela que o usuário vê, é proibida. Não ocultar um iframe ainda audível atrás de guia, seleção ou vinheta própria.[2]

**Decisão:** medir interseção real do iframe com viewport, além de `document.visibilityState`. Revalidar em resize, scroll, mudança de modo e retorno à aba; se houver oclusão por UI própria, remover a UI ou parar o player, nunca confiar só na área geométrica. Usar guarda estrita `> 0,5` para iniciar/retomar; na perda de visibilidade suficiente, pausar por política conservadora do projeto. Antes de mostrar uma tela própria substitutiva, parar/pausar e retirar o player da apresentação; só depois exibir a tela. Não ocultar anúncios seletivamente nem usar transições para contorná-los.[1][2]

**Foco não equivale a visibilidade:** foco pode estar em botão externo ou no iframe enquanto o player permanece visível. Não pausar só porque `document.hasFocus()` mudou ou um controle recebeu foco; a especificação diferencia foco e estado de visibilidade.[14]

### API, autoplay, origem e identificação

- Separar `onReady`, `onStateChange`, `onError` e `onAutoplayBlocked`. Estar pronto não prova reprodução. Autoplay bloqueado tem evento próprio e não significa vídeo removido.[3]
- Erro **153** significa ausência de `HTTP Referer` ou identificação equivalente. Usar `origin` com esquema e domínio/porta reais; `origin` não é o caminho `/repositorio/` e não substitui o Referer.[1][3]
- Para hospedagem estática normal, preservar Referer com `strict-origin-when-cross-origin`, recomendação oficial; evitar `no-referrer` e integrações que suprimam a identidade.[1]
- Parâmetros `controls`, `disablekb`, `fs`, `enablejsapi` e `origin` são documentados. `modestbranding` está obsoleto; `rel=0` não elimina todos os vídeos relacionados. Não prometer player sem marcas ou avisos.[4]

**Decisões:** player oficial HTTPS, JS API habilitada, controles e teclado nativos preservados; delegar `autoplay` e `fullscreen` no iframe, sem tratar essa permissão como garantia de execução. Oferecer “Retomar reprodução” fora do iframe se bloqueado; se o navegador exigir interação direta com o player, orientar o usuário a usar o controle oficial. Registrar estado/erro, não fazer tentativas infinitas ou classificar todo bloqueio como indisponibilidade. Não usar download, proxy ou captura de mídia para evitar políticas.[2][3]

## 3. Fullscreen: dois caminhos diferentes

`requestFullscreen()` é assíncrono, depende de ativação transitória e das permissões aplicáveis. A promessa pode falhar; existem `fullscreenchange`, `fullscreenerror` e `document.fullscreenElement`. Fullscreen de conteúdo filho exige permissão específica no iframe.[6]

**Decisão preferencial para A/B/C:** botão externo pede fullscreen do **contêiner do receptor**, contendo iframe e gutters como regiões irmãs sem sobreposição. Recalcular dimensões ao entrar/sair. Se o usuário usar fullscreen nativo do YouTube, aceitar que a moldura externa desapareça: não tentar reconstruí-la sobre o vídeo.[6]

**Fallback:** detectar API/capacidade, tratar rejeição e manter modo janela utilizável. “Tela ampla” por CSS, se oferecida, deve ser rotulada como tal, não como fullscreen real. Não disparar fullscreen automaticamente ao sintonizar e não encadear depois de uma espera de rede: a ativação pode ter expirado. Disponibilizar saída externa e respeitar a saída do navegador/sistema; não capturar Esc para prender o usuário.[6]

## 4. Samsung/Tizen: o que a fonte prova e o que não prova

A Samsung documenta para **aplicativos Web de TV** setas 37/38/39/40, Enter 13 e Back **10009**, detectados sem registro individual. Outras teclas usam `tizen.tvinputdevice` e podem exigir privilégio no `config.xml`.[15]

**Limite importante:** essa documentação não prova que uma página HTTPS aberta no navegador Internet da TV recebe os mesmos eventos ou dispõe das APIs privilegiadas de um aplicativo Tizen instalado. GitHub Pages não é um pacote Tizen. Não chamar `registerKey` incondicionalmente, não exigir instalação e não prometer que Back/10009 seja capturável no navegador.[15]

A tabela de engines varia por ano: exemplos atuais incluem Tizen 10.0/Chromium M130 (2026), 9.0/M120 (2025), 5.5/M69 (2020), e WebKit em 2016. Assim, “Samsung” não identifica uma única engine; a tabela de suporte de aplicativos não substitui teste do navegador real, firmware e modelo do usuário.[12]

### Navegação e iframe cross-origin

O isolamento de origem impede inspecionar/modificar o DOM interno do iframe YouTube. A cadeia de foco pode passar para um documento filho; um listener `keydown` do documento pai não oferece controle confiável dos eventos enquanto o usuário opera o player.[10][14]

**Decisões de projeto:**

1. Implementar navegação explícita entre controles **externos**, com setas/Enter quando esses eventos chegarem; preferir `event.key`, com fallback de `keyCode` para os códigos documentados. Não consumir todas as teclas globalmente.[15]
2. Exibir foco forte também com `:focus`, sem depender exclusivamente de recursos modernos; manter ordem DOM e Tab coerentes.[12]
3. Após uma transição iniciada pela UI externa, devolver foco ao controle externo adequado, sem scroll involuntário. Não roubar foco continuamente do iframe nem tornar o player inacessível para preservar atalhos.[10][14]
4. Oferecer “Voltar à seleção” visível fora do iframe. Quando Back chegar à aplicação: sair de painel/seleção interna por hierarquia; não criar armadilha de histórico. O sistema pode consumir Back para sair do fullscreen ou navegar antes da página: registrar como resultado do aparelho, não garantir interceptação.[6][15]
5. Se o controle ficar retido no player, testar a saída nativa por Voltar/Tab/ponteiro conforme disponível. Não há prova nesta pesquisa de uma tecla universal que devolva foco do YouTube ao pai. Não criar camada transparente de captura sobre o iframe.

## 5. Áudio original: Web Audio, MP3/WAV e gestos

No Chrome, Web Audio está sujeito a autoplay. Um contexto criado antes da interação pode permanecer `suspended`; a orientação oficial é criá-lo/retomá-lo após interação do usuário. Permissão delegada ao iframe não desbloqueia automaticamente o contexto de áudio da aplicação.[7]

`decodeAudioData()` decodifica um `ArrayBuffer` em `AudioBuffer`, usa formatos aceitos pelo elemento de áudio, detecta o formato e pode rejeitar com `EncodingError`; o resultado pode ser reamostrado para a taxa do contexto. Isso não garante que todo MP3 ou todo arquivo chamado WAV seja decodificável em cada TV.[8]

**Decisões para o engine de áudio:**

- Jingle principal em MP3 e alternativa WAV PCM para teste; fetch dos arquivos próprios completos e decodificação antes da transição quando possível. Testar os bytes reais de ambos no aparelho: extensão e MIME não bastam.[8]
- Uma ação explícita “Sintonizar/ativar som”, por clique ou Enter real, cria/retoma o contexto. Eventos de teclado confiáveis podem ativar a página, mas um evento sintético não representa gesto do usuário. Se Enter do remoto não desbloquear, oferecer nova ativação visível, sem bloquear a programação.[7][14]
- Confirmar estado `running`, tratar falhas/pedido pendente com limite de espera e permitir vinheta silenciosa. O desbloqueio de Web Audio e o de YouTube são estados distintos.[3][7]
- Manter um contexto, buffers reutilizáveis e novo nó de fonte por execução. Identificar a vinheta pelo slot para não reiniciá-la a cada render/resync. Ao retornar no meio dela, usar offset correspondente ou ficar em silêncio se já terminou; nunca começar áudio atrasado sobre o programa seguinte.[8]
- Na fronteira, interromper/desconectar a fonte própria antes de carregar/retomar vídeo. Som desligado deve zerar a trilha própria e silenciar o player pela API. Ao ocultar a aba, suspender áudio próprio; ao voltar, recalcular o relógio, sem reproduzir uma fila atrasada. São decisões conservadoras de continuidade, não promessa de sincronismo frame a frame.[2][3][8]

## 6. Sessão e privacidade

`sessionStorage` associa armazenamento à origem e ao contexto de navegação, distinto de persistência global por `localStorage`. Acesso pode lançar `SecurityError`; escrita pode falhar por quota ou política. Não prometer persistência permanente nem entre aparelhos.[9]

**Decisão:** guardar somente modo A/B/C e preferência de som durante a sessão; validar valores, capturar falhas de leitura/escrita e usar memória como fallback. “Preferência salva” não significa “autoplay autorizado”: após reload verificar novamente contexto e player.[3][7][9]

As políticas YouTube exigem termos e política de privacidade que informem uso dos serviços e tratamento de dados por aplicação/terceiros. Não alegar “sem cookies” ou “nenhum dado é coletado”: mesmo um cliente estático pode carregar o player e serviços do Google.[2]

**Decisão:** antes da sintonia, explicar integração YouTube, terceiros, anúncios/cookies e armazenamento real das preferências; manter acesso a termos/privacidade fora do iframe. Carregar terceiros após a ação informada inicial. Não armazenar histórico de audiência, identificador pessoal ou telemetria remota apenas para comparar A/B/C; registrar evidências manualmente. Privacidade de terceiros não deve ser confundida com a ausência de backend próprio.

## 7. Roteiro manual curto — repetir no PC e na Samsung

**Estado deste documento:** roteiro preparado, **não executado aqui**. Toda célula começa como “pendente”, não “aprovada”. No PC, Chrome Windows; na Samsung, navegador real na TV. Registrar modelo, ano, firmware/Tizen quando disponível, navegador/UA, resolução/zoom, URL/versão do app, tipo de controle, data, resultado e evidência. Não anotar tokens ou dados pessoais.

### Preparação comum

1. Abrir a URL hospedada sob o subdiretório real do projeto. Testar sessão nova, autoplay bloqueado e armazenamento indisponível quando o ambiente permitir; não desativar políticas do navegador para obter um falso sucesso.
2. Conferir termos/privacidade, escolher som ligado/desligado e sintonizar por clique no PC e Enter no remoto. Verificar avanço real do vídeo, não apenas `onReady`; anotar dois tempos crescentes quando diagnóstico existir.[3]
3. Em cada modo, observar YouTube → vinheta original → próximo vídeo. Ouvir início/fim, mute, ausência de dupla trilha e não reinício após resync. Se a amostra não atravessar vinheta, registrar “não observado”, nunca concluir aprovação.

| Modo | PC — Chrome Windows | Samsung — controle remoto, sem presumir suporte |
| --- | --- | --- |
| A | Selecionar por mouse e teclado; revelar/recolher informação; redimensionar e entrar/sair de fullscreen. Confirmar controles externos sem invasão e mínimo do player. | Selecionar com setas/Enter; alcançar som/fullscreen/Voltar; observar se a UI discreta continua descobrível. Entrar no iframe e testar saída para UI externa. |
| B | Verificar logo/faixas inteiramente fora; navegar por Tab/setas; fullscreen do receptor deve conservar a moldura sem cobrir player. Testar também fullscreen nativo YouTube, aceitando perda da moldura. | Verificar legibilidade/foco e bordas no tamanho real; repetir fullscreen e retorno, incluindo Voltar curto. Registrar se Back foi recebido pela página ou consumido pelo sistema. |
| C | Inspecionar animações e gutters em viewport estreito, janela normal e fullscreen; garantir zero invasão mesmo nos quadros de transição. Comparar com B sem mudar programa/offset. | Observar fluidez da moldura e se gutters reduzem demais o vídeo; testar setas/Enter/Voltar dentro e fora do iframe. Reduzir animação se prejudicar foco ou desempenho; não substituir por overlay. |

### Fechamento obrigatório para cada modo

- Trocar A → B → C → seleção → modo anterior; confirmar mesma grade e posição correspondente ao relógio. Recarregar na mesma sessão e conferir preferência ou fallback declarado.
- Ocultar aba/minimizar no PC; na TV, abrir menu/trocar de contexto e retornar quando possível. Verificar parada do som em fundo, resync e foco externo recuperável; se evento não chegar, registrar limitação.
- Testar scroll/resize que deixe metade ou menos do player visível, quando possível. Reprodução não deve começar/retomar nesse estado.[1]
- Se surgir anúncio, aviso, legenda ou tela de erro, verificar preservação integral e operação nativa. Não provocar/bloquear anúncios para o teste; se não aparecerem, registrar “não observado”.
- Registrar autoplay bloqueado e recuperação, falha de áudio sem interrupção da grade, rejeição de fullscreen e retorno do foco. Se teste determinístico usar simulação, identificá-la separadamente de reprodução real.

**Liberação:** nenhum vencedor automático. Separar: evidência de fonte, teste automatizado/simulado, teste real no PC e teste físico na Samsung. Só este último autoriza relatar funcionamento **naquele modelo/firmware testado**, sem extrapolar para todas as TVs.

## 8. Limites desta pesquisa

Fontes primárias consultadas diretamente; o extrator configurado falhou e a leitura foi recuperada por HTTP direto. Não foi copiado código de terceiros. Não se verificaram licenças de arquivos sonoros, execução do aplicativo, anúncios reais, suporte de codec no aparelho nem comportamento físico de Back/fullscreen/iframe. Essas verificações permanecem com a integração e o roteiro acima. As políticas e especificações devem ser reconsultadas antes de publicar se houver mudanças relevantes.
