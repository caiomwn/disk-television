# DT-002 — Acervo Nozomi / Right Stuf: pesquisa de reserva

Verificado em 2026-11-10T10:39:22-03:00. Catálogo e grade **não foram alterados**. Nenhuma mídia foi baixada.

## Resultado e decisão

Foram registrados **30 candidatos oficiais**, em **5 séries**, com episódios **1–6 consecutivos de cada série**: Galaxy Angel, ARIA The ANIMATION, Revolutionary Girl Utena, Boogiepop Phantom e Magic User's Club (OVA). A tabela abaixo identifica cada fonte individual. São candidatos de pesquisa/reserva, **não 30 episódios liberados para exibição nesta conexão**.

Os estados regionais individuais foram: {'BLOCKED_BY_REGION': 18, 'UNAVAILABLE_OR_RESTRICTED': 7, 'METADATA_FORMATS_AVAILABLE': 5}. **Nenhum candidato foi aprovado para a grade**: os episódios iniciais apresentaram restrições/indisponibilidade, quebrando a continuidade utilizável. Magic User's Club OVA 3–6 apresentou metadados mais favoráveis, mas isso não libera 1–2. A resposta `playable_in_embed=false` em Boogiepop 2 também deve ser respeitada. Consulte os registros individuais na tabela e no JSON.

## Identidade e legitimidade

O canal original é **Nozomi Entertainment**, `@nozomient`, ID `UCUlvYyW7UVtNJQ1KTv_Bsdg`. A página About associa os domínios Nozomi e Right Stuf; cada descrição individual selecionada identifica o lançamento Nozomi da respectiva obra. A prova usada combina canal original, playlist e descrição do publicador, não somente palavras como “official” no título.[31][32]

Isso sustenta tratar os uploads como publicações do distribuidor; **não** concede licença de download, reupload, redistribuição ou disponibilidade mundial. `creator` registra direção/estúdio da obra, não confunde o distribuidor com o criador.

## Método e limitações

- Extração individual com a `.venv` do projeto: `python.exe -m yt_dlp --skip-download --dump-single-json --ignore-no-formats-error --no-playlist URL`.
- `--ignore-no-formats-error` foi usado somente para obter metadados de vídeos restritos; não contorna a restrição. Nenhuma VPN, proxy ou mudança de região foi usada.
- Requisição oEmbed individual para cada candidato. HTTP 200 pode coexistir com geobloqueio; não aprova reprodução. HTTP 401 foi registrado sem o reinterpretar como licença revogada.
- Inspeção adicional das páginas originais de Utena 1, Galaxy Angel 1, ARIA 1 e Magic User's Club OVA 1 encontrou `availableCountries: [CA, US]`; as páginas negaram reprodução na conexão disponível. Magic OVA 3 retornou status `OK` e `playableInEmbed: true` na página original, sem teste de iframe.
- **Não houve teste de iframe**, Smart TV ou sincronização. Nenhum ensaio audiovisual completo foi realizado.
- Durações vêm do `dump-single-json` **individual**, não de suposição de 24 minutos ou de oEmbed. As playlists às vezes diferem em 1 segundo; ambos os valores são preservados no JSON e prevalece o individual.
- O aviso de ausência de runtime JavaScript do yt-dlp foi preservado em `rawWarnings`. Metadados recuperados não são prova de playback.

## Idiomas, legendas e íntegra

Galaxy Angel e Boogiepop foram selecionados em versões **Dub/inglês**. ARIA, Utena e Magic User's Club foram selecionados em versões **Sub**, com japonês indicado editorialmente e inglês anunciado pelas tags/descrição do publicador. **Não foi possível confirmar visualmente a legenda inglesa de cada episódio**. Nenhuma faixa de legenda PT foi confirmada; a lista vazia de faixas selecionáveis não prova ausência de legendas gravadas na imagem.

O JSON distingue essa declaração editorial de confirmação técnica em `subtitleAssessment` e `audioLanguageEvidence`. Não houve auditoria por escuta. Os uploads são apresentados como episódios numerados completos pelo publicador, com durações compatíveis e continuidade; a integridade audiovisual de ponta a ponta continua **PARTIAL**, não verificada integralmente.

## Ano original — fontes e ressalvas

- **Galaxy Angel: 2001**, ano de estreia da obra, não do upload.[34]
- **ARIA The ANIMATION: 2005**, ano de estreia da obra, não do upload.[35]
- **Revolutionary Girl Utena: 1997**, ano de estreia da obra, não do upload.[13]
- **Boogiepop Phantom: 2000**, ano de estreia da obra, não do upload.[36]
- **Magic User's Club: 1996**, ano de estreia da obra, não do upload.[37]

Para Magic User's Club OVA, ANN registra 25/05/1996–25/10/1997; MAL também registra 1996. A página Bandai Channel possui uma tag 1995, divergente; adotou-se a data de lançamento documentada por ANN/MAL, deixando a divergência explícita.[37][38][39]

## Tabela dos candidatos de reserva

Todos: canal Nozomi acima, país de origem JP, `kind=episode`, `status=PARTIAL`. `True` na coluna embed é somente metadado; `None` é desconhecido, não permissão.

| Série | Temporada | Ep. | YouTube ID | Segundos | Resultado regional do yt-dlp | Embed metadata | oEmbed HTTP | Fonte |
|---|---:|---:|---|---:|---|---|---:|---|
| Galaxy Angel | 1 | 1 | `mXzdXR7YTIE` | 821 | BLOCKED_BY_REGION | None | 200 | [1] |
| Galaxy Angel | 1 | 2 | `-ivS85ysThE` | 822 | BLOCKED_BY_REGION | None | 200 | [2] |
| Galaxy Angel | 1 | 3 | `lL6L_SyOsV4` | 821 | BLOCKED_BY_REGION | None | 200 | [3] |
| Galaxy Angel | 1 | 4 | `N7wHo-qv7D8` | 821 | BLOCKED_BY_REGION | None | 200 | [4] |
| Galaxy Angel | 1 | 5 | `gDdR9zZZizE` | 820 | BLOCKED_BY_REGION | None | 200 | [5] |
| Galaxy Angel | 1 | 6 | `jw0Q7DQJg_4` | 821 | BLOCKED_BY_REGION | None | 200 | [6] |
| ARIA The ANIMATION | 1 | 1 | `y0sZ3-B5Phw` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [7] |
| ARIA The ANIMATION | 1 | 2 | `iwrQGt5I2j4` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [8] |
| ARIA The ANIMATION | 1 | 3 | `JN18AvcHXA8` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [9] |
| ARIA The ANIMATION | 1 | 4 | `LAqApKnHPYs` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [10] |
| ARIA The ANIMATION | 1 | 5 | `3-2kS-Mr4lk` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [11] |
| ARIA The ANIMATION | 1 | 6 | `LXIcAf9TVKM` | 1415 | UNAVAILABLE_OR_RESTRICTED | None | 200 | [12] |
| Revolutionary Girl Utena | 1 | 1 | `6TQFlVcPyUA` | 1407 | BLOCKED_BY_REGION | None | 401 | [13] |
| Revolutionary Girl Utena | 1 | 2 | `_7yheJgimEA` | 1409 | BLOCKED_BY_REGION | None | 401 | [14] |
| Revolutionary Girl Utena | 1 | 3 | `8XsGNSRyYIc` | 1409 | BLOCKED_BY_REGION | None | 401 | [15] |
| Revolutionary Girl Utena | 1 | 4 | `8Fdf8hVGF8w` | 1409 | BLOCKED_BY_REGION | None | 401 | [16] |
| Revolutionary Girl Utena | 1 | 5 | `yqftBAuFYsk` | 1407 | BLOCKED_BY_REGION | None | 401 | [17] |
| Revolutionary Girl Utena | 1 | 6 | `ogvTPJCgasM` | 1408 | BLOCKED_BY_REGION | None | 401 | [18] |
| Boogiepop Phantom | 1 | 1 | `pi0MBAjkPW4` | 1439 | UNAVAILABLE_OR_RESTRICTED | None | 401 | [19] |
| Boogiepop Phantom | 1 | 2 | `CABiEmYU6MY` | 1438 | METADATA_FORMATS_AVAILABLE | False | 401 | [20] |
| Boogiepop Phantom | 1 | 3 | `kOHrNGwr0UQ` | 1448 | BLOCKED_BY_REGION | None | 401 | [21] |
| Boogiepop Phantom | 1 | 4 | `7ZpYw4dbFDM` | 1450 | BLOCKED_BY_REGION | None | 401 | [22] |
| Boogiepop Phantom | 1 | 5 | `yH69ZJ8qsVo` | 1448 | BLOCKED_BY_REGION | None | 401 | [23] |
| Boogiepop Phantom | 1 | 6 | `BF16O65qds4` | 1448 | BLOCKED_BY_REGION | None | 401 | [24] |
| Magic User's Club | 1 | 1 | `EhtJvAzIhfw` | 1672 | BLOCKED_BY_REGION | None | 200 | [25] |
| Magic User's Club | 1 | 2 | `OagV-8YuST4` | 1639 | BLOCKED_BY_REGION | None | 200 | [26] |
| Magic User's Club | 1 | 3 | `aI3X8908K2A` | 1686 | METADATA_FORMATS_AVAILABLE | True | 200 | [27] |
| Magic User's Club | 1 | 4 | `k399XSLKc8E` | 1787 | METADATA_FORMATS_AVAILABLE | True | 200 | [28] |
| Magic User's Club | 1 | 5 | `6mEjQ2EB5CQ` | 1770 | METADATA_FORMATS_AVAILABLE | True | 200 | [29] |
| Magic User's Club | 1 | 6 | `iclKa89FSmU` | 1720 | METADATA_FORMATS_AVAILABLE | True | 200 | [30] |

## Fontes inadequadas / bloqueadas — separadas

Os registros bloqueados/indisponíveis estão separados em `notSuitableOnCurrentConnection`; não se deve importar automaticamente o array `candidates`. Os seguintes resultados não entram nos 30 episódios:

- **Galaxy Angel — AX2016 Teaser Trailer** — Trailer; não é episódio.[40]
- **ARIA The ANIMATION Trailer** — Trailer; não é episódio.[41]
- **Di Gi Charat ALL episodes (4K, JP VA/ENG SUB)** — Reupload/upscale; não foi encontrada autorização do canal. Excluído, mesmo com episódios completos e legendas anunciadas.[42]
- **Exiled Destiny Nurse Witch Komugi-chan Ep 5 English Dub** — Fansub/reupload; sem cadeia de autorização demonstrada.[43]

**Galaxy Angel 1 Sub** (`Hqjq3K3JimQ`, 821 s) também foi extraído individualmente: mesmo canal original e restrição regional. Trocar Dub por Sub **não resolveu** o bloqueio; oEmbed retornou metadados, sem comprovar playback.[33]

## Desejados sem confirmação utilizável

- **Di Gi Charat** — Nenhum episódio retrô atualmente utilizável foi confirmado. O site oficial documenta sessões especiais gratuitas e temporárias em 2022; isso não prova disponibilidade em 2026. Canal atual mostra material promocional/bastidores.[44]
- **Nurse Witch Komugi** — Busca no canal Nozomi sem resultado; buscas abertas retornaram OPs/AMVs e fansub não autorizado. Nenhum episódio completo oficial confirmado.[45]
- **Azumanga Daioh** — Busca no canal não encontrou episódios; resultado era trailer de Ninja Nonsense, referência promocional a Azumanga não equivale a acervo.[46]

A publicação oficial de Di Gi Charat de 24/08/2022 anunciava especiais antigos por tempo limitado. Não foi encontrada evidência suficiente de episódios retrô oficiais atualmente abertos com legendas English/PT; material Reiwa de 2022 também ficaria fora do recorte 1995–2008.[44][47]

## Descobertas para pesquisa futura

- **Magic User’s Club TV (temporada 2)**: a playlist oficial reúne episódios 1–13, além dos seis OVAs. Extração individual mostrou metadados favoráveis nos episódios 1–2 e restrição nos seguintes; o JSON conserva IDs/durações dessa descoberta, fora dos 30 candidatos principais.[48]
- **ARIA The Natural** e **ARIA The Origination**: playlists Nozomi encontradas por busca aberta, embora omitidas da página de playlists visível nesta região. Só inventário de playlist foi consultado; não foram adicionadas como episódios aprovados.[49][50]

## Arquivos e próxima validação

- `research/dt002/nozomi-candidates.json`: 30 objetos com schema solicitado, evidência individual, avisos, bloqueios, rejeições e descobertas separados.
- `docs/DT-002-NOZOMI.md`: este relatório.
- Não foram editados catálogo, grade, player ou dependências. O agente principal deve decidir a elegibilidade regional e testar iframe antes de qualquer inclusão. A meta de 15–30 episódios **utilizáveis nesta conexão** não foi atingida por este acervo; entregar IDs oficiais restritos como se fossem livres seria incorreto.

## Sources

[1] https://www.youtube.com/watch?v=mXzdXR7YTIE
[2] https://www.youtube.com/watch?v=-ivS85ysThE
[3] https://www.youtube.com/watch?v=lL6L_SyOsV4
[4] https://www.youtube.com/watch?v=N7wHo-qv7D8
[5] https://www.youtube.com/watch?v=gDdR9zZZizE
[6] https://www.youtube.com/watch?v=jw0Q7DQJg_4
[7] https://www.youtube.com/watch?v=y0sZ3-B5Phw
[8] https://www.youtube.com/watch?v=iwrQGt5I2j4
[9] https://www.youtube.com/watch?v=JN18AvcHXA8
[10] https://www.youtube.com/watch?v=LAqApKnHPYs
[11] https://www.youtube.com/watch?v=3-2kS-Mr4lk
[12] https://www.youtube.com/watch?v=LXIcAf9TVKM
[13] https://www.youtube.com/watch?v=6TQFlVcPyUA
[14] https://www.youtube.com/watch?v=_7yheJgimEA
[15] https://www.youtube.com/watch?v=8XsGNSRyYIc
[16] https://www.youtube.com/watch?v=8Fdf8hVGF8w
[17] https://www.youtube.com/watch?v=yqftBAuFYsk
[18] https://www.youtube.com/watch?v=ogvTPJCgasM
[19] https://www.youtube.com/watch?v=pi0MBAjkPW4
[20] https://www.youtube.com/watch?v=CABiEmYU6MY
[21] https://www.youtube.com/watch?v=kOHrNGwr0UQ
[22] https://www.youtube.com/watch?v=7ZpYw4dbFDM
[23] https://www.youtube.com/watch?v=yH69ZJ8qsVo
[24] https://www.youtube.com/watch?v=BF16O65qds4
[25] https://www.youtube.com/watch?v=EhtJvAzIhfw
[26] https://www.youtube.com/watch?v=OagV-8YuST4
[27] https://www.youtube.com/watch?v=aI3X8908K2A
[28] https://www.youtube.com/watch?v=k399XSLKc8E
[29] https://www.youtube.com/watch?v=6mEjQ2EB5CQ
[30] https://www.youtube.com/watch?v=iclKa89FSmU
[31] https://www.youtube.com/@nozomient/about
[32] https://www.youtube.com/@nozomient/playlists
[33] https://www.youtube.com/watch?v=Hqjq3K3JimQ
[34] https://www.b-ch.com/titles/152
[35] https://www.crunchyroll.com/series/GR2P9ZQ2R/aria-the-animation
[36] https://myanimelist.net/anime/369/Boogiepop_wa_Warawanai
[37] https://www.animenewsnetwork.com/encyclopedia/anime.php?id=345
[38] https://myanimelist.net/anime/629/Mahoutsukai_Tai
[39] https://www.b-ch.com/titles/191
[40] https://www.youtube.com/watch?v=8AgwV9-BKR8
[41] https://www.youtube.com/watch?v=NraaWUZxWZw
[42] https://www.youtube.com/watch?v=7iGG9iijpcA
[43] https://www.youtube.com/watch?v=UEm0unoakCI
[44] https://digicharat-reiwa.com/news/post-57
[45] https://www.youtube.com/@nozomient/search?query=Komugi
[46] https://www.youtube.com/@nozomient/search?query=Azumanga
[47] https://www.youtube.com/@digicharat_r
[48] https://www.youtube.com/playlist?list=PLrrh84y760v-07h6z6XgXtUgLCZgQkGT8
[49] https://www.youtube.com/playlist?list=PLrrh84y760v_4ER9JIJG2EVNnjYYYTMV7
[50] https://www.youtube.com/playlist?list=PLrrh84y760v_sGL16wsuJQfHMqJFttGew
