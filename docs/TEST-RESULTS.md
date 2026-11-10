# DISK TELEVISION 0.1 — validação executada

Data: 10 de novembro de 2026. Ambiente real: Windows 11; Node v24.20.0; Chrome instalado, modo headless; Python da `.venv`; Playwright 1.65.0 e Pillow 13.0.0. Não houve publicação remota nem teste em Smart TV física.

## Resultado reproduzível

Comando executado na pasta do projeto:

    .venv/Scripts/python.exe tools/check.py --browser --live

**28 testes determinísticos passaram**, sem falhas, mais um diagnóstico de reprodução real do YouTube aprovado:

| Grupo | Testes | Resultado |
|---|---:|---|
| Motor, playout e dados de produção (Node) | 14 | passou |
| PNG/SVG, recursos relativos e catálogo (Python/Pillow) | 4 | passou |
| Servidor local usado pelo inicializador | 1 | passou |
| Integração no Chromium com API YouTube explicitamente simulada | 9 | passou |
| Diagnóstico de rede/player oficial, sem mídia simulada | execução separada | passou |

Saída integral real, comandos, códigos de saída e timestamp: `evidence/test-run.json`. Diagnóstico do player: `evidence/live-player.json`. As evidências são registros de execução, não dados inventados para demonstração.

## Player real

`tests/live_player.py` carregou a API e o iframe oficiais pela internet, a partir de uma página HTTP local no subcaminho `/disk-television/`:

1. Entrou no slot de **Tears of Steel**, ID `R6MlUcmOul8`, com offset solicitado de 22 segundos. A API retornou estado `1` (reproduzindo) e duas amostras de tempo crescentes. Os valores exatos da última execução ficam em `evidence/live-player.json`.
2. Avançou o relógio do teste para a fronteira da grade e observou a vinheta de continuidade.
3. Observou a vinheta “A seguir” com o título **Elephants Dream**.
4. Avançou à próxima fronteira: o mesmo player carregou **Elephants Dream**, ID `TLkA0RELQ1g`, automaticamente, sem clique ou escolha de programa. A API retornou estado `1` e duas amostras de tempo crescentes, registradas no mesmo JSON.
5. `playbackConfirmed`, `stationTransitionObserved` e `automaticNextPlaybackConfirmed` retornaram `true`.

O relógio foi controlado apenas pelo teste, por injeção externa; o aplicativo publicado usa `Date.now()` normalmente e não tem seletor de programas nem relógio fictício. Este diagnóstico não assistiu aos filmes inteiros: os limites de slot foram acelerados para validar a sequência. Não há prova de reprodução ininterrupta por 24 horas. Áudio audível não foi aferido no modo headless.

## Cobertura efetiva

- Aplicação estática servida por HTTP, inclusive sob caminho de repositório.
- Seleção temporal e posição do vídeo, reabertura determinística e ciclos anteriores à época.
- Cobertura de cada um dos **86400 segundos** da grade; comparação com reabertura e dia seguinte.
- Meia-noite, limites exatos de slots, guia atravessando o ciclo e vídeos completos sem truncamento editorial.
- Grade de **579 slots**, com **191 exibições de vídeo** e **388 slots de vinheta/continuidade**, em seis blocos. O acervo contém dez obras e as reprises são deliberadas.
- Vinhetas de identificação, próximo programa e noturna; guia com destaque para o slot atual.
- Erro de incorporação 150 simulado: continuidade entra e o próximo vídeo retoma no horário.
- Falha de rede da API simulada: nova atração tenta reconectar automaticamente.
- Player que nunca inicia e buffering prolongado: timeout finito, sem paralisar a grade.
- Autoplay bloqueado simulado: mensagem acionável e ressintonia.
- Regressão de viewport 640 × 320: nenhum novo vídeo é carregado automaticamente com metade ou menos do player visível. Ao retornar à imagem, o vídeo correto entra no offset atual. O foco após sintonia não rola a página.
- Termos e privacidade acessíveis antes da sintonia e por link permanente; links oficiais presentes. Não houve requisição à API YouTube antes da interação inicial.
- Guia interrompe e esconde o player; ao fechar, volta ao offset atual, não ao ponto de pausa.
- Navegação por setas, Tab, G e Esc; foco contido no guia.
- Viewport móvel 390 × 844 sem transbordamento horizontal; modo de movimento reduzido exercitado.
- Catálogo inválido apresenta erro de configuração em vez de habilitar transmissão incorreta.
- IDs malformados são rejeitados sem “corrigir” tokens automaticamente.
- PNG com assinatura binária válida, 2400 × 1050, RGBA, alpha 0–255; SVGs parseáveis, com paths editáveis e sem imagens/fontes remotas.
- Inicializador local reserva a porta antes de servir a página. O teste não abriu uma janela visual por associação do Windows; validou o mesmo servidor Python com navegador automático desabilitado.

## Inspeção visual

Capturas locais de 1920 × 1080:

- `evidence/receiver.png`: tela inicial e logotipo original.
- `evidence/ident-station.png`: identificação da emissora.
- `evidence/ident-next.png`: anúncio com título real.
- `evidence/ident-night.png`: identificação noturna.
- `evidence/live-player.png`: player oficial com vídeo real.

As capturas das vinhetas usaram API simulada e conteúdo gráfico original local; a captura de reprodução usou o YouTube real. A tela inicial e a vinheta de próximo programa foram inspecionadas visualmente; não apresentaram recortes ou overflow no viewport principal. A assinatura fica fora do iframe durante vídeos, e os controles oficiais permanecem acessíveis.

## O que não foi comprovado

- Samsung/Tizen, LG/webOS ou outra Smart TV física e seus controles remotos.
- Firefox, Safari e navegadores antigos.
- Reprodução efetiva dos outros oito vídeos: eles tiveram metadados individuais e oEmbed verificados, não reprodução visual nesta validação.
- Disponibilidade regional fora desta conexão, classificação jurídica, licenças individuais das obras ou estabilidade futura do YouTube.
- Reprodução por 24 horas reais, comportamento em todos os formatos de anúncio, consentimento/cookies em todas as regiões ou falhas reais de cada código da API.
- GitHub Pages remoto/HTTPS publicado. A compatibilidade de subcaminho foi testada localmente; o deploy depende da autorização do proprietário.
- Tecla Voltar física de TV, tela cheia e liberação de áudio em todos os aparelhos.

## Reexecutar

O runtime publicado não exige instalação. Para desenvolvimento/QA:

    python -m venv .venv
    .venv/Scripts/python.exe -m pip install -r requirements-dev.txt
    .venv/Scripts/python.exe tools/check.py --browser --live

Os testes de browser deste ambiente usam o Chrome instalado em `C:/Program Files/Google/Chrome/Application/chrome.exe`. Em outro sistema, ajuste o caminho nos scripts de teste ou use o Chromium do Playwright. Não confundir esse caminho de QA com uma dependência do site.

O diagnóstico `--live` precisa de rede e pode falhar futuramente por indisponibilidade do YouTube. O grupo de browser normal usa um test double identificado e não prova disponibilidade externa.

Para atualizar a grade de referência, rode `node tools/export-schedule.mjs`. Para gerar ZIPs locais, rode `python tools/package.py`. O empacotamento verifica CRC e presença dos arquivos de runtime antes de declarar o arquivo válido.

## Próximos passos recomendados

1. Publicar o ZIP mínimo no repositório autorizado e repetir o diagnóstico na URL HTTPS.
2. Testar na TV de destino: foco/OK/Voltar, áudio inicial, tela cheia e ao menos duas mudanças automáticas.
3. Expandir a curadoria com fontes oficiais em português e obras mais longas; preservar os limites da API e a rastreabilidade de cada item.
4. Fazer uma sessão prolongada real para observar anúncios, latência, suspensão e retomada.
