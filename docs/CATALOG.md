# DISK TELEVISION — catálogo verificado

Verificação executada em 10 de novembro de 2026. **10 curtas/episódios completos**, 4850 segundos no total (80:50). Todos os uploads selecionados pertencem aos canais Blender ou Blender Studio. Não há trailers na grade; First Cycle é o piloto completo, não um longa finalizado.[1][5][6]

## Critérios e limites

- `data/catalog.json` é um array de objetos no schema solicitado. `creator` identifica o canal publicador, não pretende atribuir autoria exclusiva a ele. `year` é o ano da obra, não necessariamente o ano do upload.
- IDs foram descobertos em resultados reais do YouTube via busca do yt-dlp; nenhum ID foi recuperado de memória. Para cada selecionado, extração individual sem download e YouTube oEmbed confirmaram título, canal e existência naquele instante.[1][5][6]
- As durações são inteiros do campo `duration` da extração individual, incluindo créditos e vinhetas do upload. Não usamos a duração arredondada do resultado da busca, que divergiu em até um segundo em vários itens.[1][6][8]
- `verification.embeddability`: todos retornaram `playable_in_embed=true` e iframe no oEmbed. Isso comprova permissão nos metadados consultados, **não reprodução efetiva** no domínio GitHub Pages ou em todos os navegadores. Não houve teste do player.[1][5][6]
- `verification.regionalAvailability`: **não comprovada** para todos. `availability=public` na conexão utilizada não demonstra disponibilidade mundial, nem garante Brasil/EUA. Não houve teste em múltiplos países, VPN ou consulta autenticada à YouTube Data API.
- `language=en` indica inglês; `und` é a escolha editorial para narrativa sem dependência de diálogo, não uma garantia automática emitida pela API. Não houve revisão audiovisual integral; essas classificações devem ser revistas editorialmente antes de chamar a grade de totalmente sem fala. Em Spring, a ausência de diálogos é declarada explicitamente na descrição oficial.[6]
- Os idiomas automáticos dos uploads não foram tratados como prova de fala. Gran Dillama retornou `es`; Llamigos e CHARGE retornaram `en`.[7][8][9]
- Coffee Run e Spring não retornaram idioma. Os valores editoriais `und` não são transcrição desses campos.[6][10]
- Não foi baixado vídeo, áudio ou legenda. Só metadados foram consultados. Este catálogo não concede direitos, não licencia redistribuição e não substitui os termos do YouTube nem a análise individual das licenças. Use o player oficial, créditos e links originais.
- Adequação é linguística, não classificação infantil: Tears of Steel informa 12+, Cosmos Laundromat informa 13+ e suicídio, e Spring informa 6+. Não tratar `age_limit=0` do extrator como classificação indicativa editorial.[1][5][6]

## Seleção e evidência por upload

| Obra | Ano da obra | Canal oficial | Duração individual | Idioma editorial | Evidência |
|---|---:|---|---:|---|---|
| Tears of Steel | 2012 | Blender | 734 s (12:14) | en | oEmbed 200; public; embed=true; upload 2012-09-26.[1] |
| Sintel | 2010 | Blender | 888 s (14:48) | en | oEmbed 200; public; embed=true; upload 2010-09-30.[2] |
| Big Buck Bunny | 2008 | Blender | 635 s (10:35) | und | oEmbed 200; public; embed=true; upload 2014-11-10.[3] |
| Elephants Dream | 2006 | Blender | 654 s (10:54) | en | oEmbed 200; public; embed=true; upload 2009-07-14.[4] |
| Cosmos Laundromat: First Cycle | 2015 | Blender | 731 s (12:11) | en | oEmbed 200; public; embed=true; upload 2015-08-10.[5] |
| Spring | 2019 | Blender Studio | 464 s (7:44) | und | oEmbed 200; public; embed=true; upload 2019-04-04.[6] |
| Caminandes 2: Gran Dillama | 2013 | Blender | 146 s (2:26) | und | oEmbed 200; public; embed=true; upload 2013-11-22.[7] |
| Caminandes 3: Llamigos | 2016 | Blender | 150 s (2:30) | und | oEmbed 200; public; embed=true; upload 2016-01-30.[8] |
| CHARGE | 2022 | Blender Studio | 263 s (4:23) | und | oEmbed 200; public; embed=true; upload 2022-12-15.[9] |
| Coffee Run | 2020 | Blender Studio | 185 s (3:05) | und | oEmbed 200; public; embed=true; upload 2020-05-29.[10] |

Big Buck Bunny: a seleção é o upload UHD/60 fps de 2014, cuja duração é 635 segundos; o ano da obra, 2008, é também explicitado no título do upload histórico do Blender Studio encontrado na busca. Não confundir com a edição de 597 segundos.[3][13]
Elephants Dream: a própria descrição do upload identifica o filme como de 2006, embora o upload seja de 2009.[4]

## Prioridades avaliadas, mas excluídas

- **Agent 327: Operation Barbershop** (`mN0zPOpADL4`): existe, 232 s, canal Blender Studio, oEmbed 200 e embed permitido nos metadados. Porém a própria descrição o chama de teaser de três minutos para um longa. Excluído para cumprir o requisito de obras completas; não vendido como longa/curta autônomo completo.[11]
- **Caminandes 1: Llama Drama** (`JOhiWY7XmoY`), canal Pablo Vazquez: apareceu na busca, mas a extração individual falhou com `This video is not available`. Excluído; não inferimos remoção global, motivo jurídico ou bloqueio regional a partir dessa mensagem.[12]
- CHARGE e Coffee Run completam a seleção com uploads integrais dos canais oficiais, sem recorrer a reuploads de terceiros.[9][10]

## Reproduzir a verificação

Necessita rede e yt-dlp. Execute por URL do catálogo; não inclui download de mídia:

```bash
uv tool run --from yt-dlp yt-dlp --skip-download --dump-single-json "https://www.youtube.com/watch?v=WhWc3b3KhnY"
curl --fail --get "https://www.youtube.com/oembed" --data-urlencode "url=https://www.youtube.com/watch?v=WhWc3b3KhnY" --data-urlencode "format=json"
```

Conferir `id`, `title`, `channel`, `channel_id`, `upload_date`, `duration`, `availability` e `playable_in_embed`; oEmbed deve informar o mesmo título/canal e um iframe. Repetir para cada `sourceUrl`. Se falhar, retirar temporariamente o item; não substituir duração por palpite. O resultado é uma fotografia no instante de `checkedAt`, não monitoramento contínuo.

Para a grade 24h, repetir/ciclar os itens com os tempos medidos e permitir falha de reprodução, erro de incorporação, publicidade, restrições de autoplay e deriva do player. A soma do catálogo não constitui uma transmissão contínua de 24 horas.

## Sources

[1] https://www.youtube.com/watch?v=R6MlUcmOul8 — Tears of Steel - Blender VFX Open Movie
[2] https://www.youtube.com/watch?v=eRsGyueVLvQ — Sintel - Open Movie by Blender Foundation
[3] https://www.youtube.com/watch?v=aqz-KE-bpKQ — Big Buck Bunny 60fps 4K - Official Blender Foundation Short Film
[4] https://www.youtube.com/watch?v=TLkA0RELQ1g — Elephants Dream
[5] https://www.youtube.com/watch?v=Y-rmzh0PI3c — Cosmos Laundromat - First Cycle. Official Blender Foundation release.
[6] https://www.youtube.com/watch?v=WhWc3b3KhnY — Spring - Blender Open Movie
[7] https://www.youtube.com/watch?v=Z4C82eyhwgU — "Caminandes 2: Gran Dillama" - Blender Animated Short
[8] https://www.youtube.com/watch?v=SkVqJ1SGeL0 — Caminandes 3: Llamigos
[9] https://www.youtube.com/watch?v=UXqq0ZvbOnk — CHARGE - Blender Open Movie
[10] https://www.youtube.com/watch?v=PVGeM40dABA — Coffee Run - Blender Open Movie
[11] https://www.youtube.com/watch?v=mN0zPOpADL4 — Agent 327: Operation Barbershop
[12] https://www.youtube.com/watch?v=JOhiWY7XmoY — Caminandes 1: Llama Drama
[13] https://www.youtube.com/watch?v=brLbwajyGNI — 2008 - Big Buck Bunny - by Blender Institute
