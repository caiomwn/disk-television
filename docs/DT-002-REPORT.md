# DISK TELEVISION 0.2 — DT-002 concluída

Edição editorial integrada em 10 de novembro de 2026. Não houve publicação remota. O receptor, o motor, a identidade, o layout e as vinhetas da 0.1 foram preservados por comparação SHA-256; a mudança é de conteúdo, programação, metadados e QA.

## Resumo conferido por código

| Medida | Resultado |
|---|---:|
| Vídeos anteriores | 10 |
| Adicionados | 38 |
| Catálogo integrado | 48 |
| Novos com reprodução real incorporada observada | 38 |
| Total com reprodução real incorporada observada | 48 |
| Vídeos distintos na grade atual | 46 |
| Novos vídeos distintos na grade atual | 36 |
| Animação japonesa no catálogo | 36 |
| Destes: episódios/longa comerciais japoneses | 26 |
| Destes: curtas acadêmicos japoneses | 10 |
| Animação japonesa distinta no ar | 34 |
| Títulos/séries diferentes no catálogo | 30 |
| Títulos/séries diferentes no ar | 29 |
| Conteúdo único no catálogo | 14:52:10 |
| Conteúdo único utilizado nesta grade | 14:03:28 |
| Animação japonesa sobre todas as 24h, incluindo vinhetas | 89,0394% |
| Animação japonesa sobre o tempo de vídeos | 91,5648% |
| Animação japonesa na faixa 18h–24h, incluindo vinhetas | 97,6806% |
| Vídeos japoneses estritamente datados de 1995–2008 | 17 |
| Slots da grade / exibições de vídeo / continuidade | 256 / 83 / 173 |

Contagem de títulos: episódios agrupados por série; filmes e curtas completos contam individualmente. GEIDAI/Seika não foram tratados como uma única série narrativa. Origem JP dos curtas significa produção acadêmica no Japão, não nacionalidade presumida do autor. Métricas completas: `evidence/dt002/editorial-metrics.json`.

Não escondemos os limites do recorte: Rayearth é de 1994; Char’s Counterattack, de 1988; os dez curtas acadêmicos são contemporâneos. O núcleo televisivo dos anos 1990–2000 é complementado por esses clássicos e descobertas, não por uma alegação falsa de que todo o acervo seja Y2K.

## Direção editorial e escolhas

- **Magic Knight Rayearth 1–8:** eixo magical-girl/shoujo e fantasia CLAMP, em edição oficial dublada em inglês. Episódios 1–4 aparecem antes de 5–8; o encore noturno repete a janela inteira em ordem. A fonte TMS foi vinculada ao site corporativo, não admitida apenas por escrever “official” no nome.[11]
- **Magic User’s Club TV 1–2:** descoberta de 1999 com comédia escolar e cultura magical/otaku. A numeração do publicador chama a TV de Season 2 e a OVA de Season 1. É uma janela TV curta; não apresentamos o trecho como série completa nem como substituto da OVA anterior. Os episódios seguintes não foram colocados no ar sem a mesma confirmação.[14]
- **Sonic X 1–6:** aventura, tecnologia e nostalgia de 2003 para a manhã; reprises 1–4 reaparecem em ordem, repartidas entre faixas. É complemento de anime Y2K, não uma alegação de moe.[11]
- **Kenichi 1–3:** comédia escolar e ação de 2006, dentro de ANIME ARCHIVE; sequência de estreia completa desta janela.[11]
- **Gundam SEED HD Remaster 1–3 e Gundam 00, episódio 1:** núcleo mecha/tecnologia de CYBERIA. Os anos são os da obra original, não os do remaster. O piloto 00 é apresentado como descoberta, não como temporada completa.[10]
- **Char’s Counterattack:** longa japonês integral da sessão CINE DISK. A edição publicada tem 7213 segundos e faixas EN/PT-BR listadas na auditoria individual. É um clássico de franquia que se beneficia de contexto prévio, não um filme independente dos anos 2000.[10]
- **GEIDAI e Kyoto Seika:** dez curtas de memória, percepção, absurdo e alienação digital. Add to Stories, Suma-oji, The Hole e Echoes of Memory aproximam as faixas noturnas e tecnológicas do gosto surreal/psicológico sem fingir que são episódios de anime comercial retrô. As instituições apontam para os respectivos canais.[9][13]
- **Best Friend e o piloto de The Amazing Digital Circus:** complementos internacionais delimitados, respectivamente francês e australiano. Não entram na contagem japonesa. A edição DUST de Best Friend não foi duplicada como outra obra.[12][15]
- **Os dez vídeos anteriores:** preservados e revalidados; aparecem uma vez cada como contrapontos, não mais como o centro do canal.

Os dois episódios de **SEED Destiny** também reproduziram e estão no catálogo, porém ficam fora da grade. A reserva evita abrir uma continuação antes de oferecer uma janela narrativa adequada de SEED. Nenhum arquivo bloqueado foi substituído por reupload de fã.

## Grade diária — Brasília

| Horário | Bloco | Função editorial |
|---|---|---|
| 00:00–03:00 | AFTER HOURS | Curtas autorais japoneses, surrealismo digital e complementos adultos. |
| 03:00–06:30 | MORNING FREQUENCY | Sonic X 1–6, Magic User’s Club TV 1–2 e contrapontos leves. |
| 06:30–10:00 | ANIME ARCHIVE | Kenichi 1–3 e Rayearth 1–4. |
| 10:00–13:30 | MOE SIGNAL | Rayearth 5–8; reprises declaradas de Magic TV 1–2 e Sonic 1–2. |
| 13:30–18:00 | CYBERIA | SEED 1–3, piloto 00, Sonic 3–4 da reprise e curtas de tecnologia/percepção. |
| 18:00–21:30 | MOE SIGNAL / ENCORE | Rayearth 1–8 em ordem, com continuidade. |
| 21:30–24:00 | CINE DISK | Char’s Counterattack completo e curtas de encerramento. |

A grade compila em exatamente 86400 segundos, sem lacunas/sobreposições. As sobras de bloco são identificações originais de 19 a 141 segundos; não são filmes truncados. Repetição máxima: duas exibições de episódios, uma do longa e até três de alguns curtas japoneses distribuídos pelo dia. Os programas completos não viraram trailers ou AMVs para preencher horários.

Grade integral com cada vinheta e atração: `GRADE.csv` e `GRADE.md`. Os rótulos de AGORA, A SEGUIR e do guia continuam derivados do mesmo motor.

## Verificação: o que realmente foi observado

`tools/verify_embeds.py` abriu um único player oficial visível por página HTTP local, sem baixar mídia. Cada um dos 48 vídeos passou por observação com:

1. ID do vídeo efetivamente carregado igual ao candidato;
2. estado playing;
3. duração compatível com a duração individual verificada;
4. pelo menos duas amostras consecutivas com tempo avançando;
5. ausência de evento de erro de incorporação.

Registros individuais, horários, amostras e capturas representativas: `evidence/dt002/playback-results.json` e `evidence/dt002/embed-*.png`. Não se assistiu a cada obra inteira, nem se comprovou a reprodução contínua por 24h. Não se homologou Smart TV nem áudio audível em headless. O país de saída da conexão não foi geolocalizado: esta é prova da conexão de execução, não certificação geral “funciona no Brasil” ou “funciona nos EUA”.

Estados usados:

- **VERIFICADO / `VERIFIED`:** houve reprodução real no embed, no escopo acima.
- **PARCIALMENTE VERIFICADO / `PARTIAL`:** metadados/origem confirmados, mas embed não comprovado. Candidatos desta classe permanecem em `research/dt002`, fora da programação principal.
- **NÃO VERIFICADO:** pista de pesquisa sem evidência suficiente; não admitida no catálogo operacional como se fosse conteúdo reproduzível.

`DT-002-VERIFICATION.csv` é a tabela consultável dos 48 integrados. Bloqueios e candidatos de reserva da pesquisa estão nos três relatórios específicos de distribuidores, Nozomi e alternativas.

### Idioma e legendas

A auditoria `research/dt002/caption-audit.json` separa CC manual de legendagem automática. Sonic X listou inglês manual; Rayearth e Kenichi não listaram CC manual nessa consulta, embora a edição seja dublada em inglês. Não interpretamos “English Dub” como prova de legenda. SEED e o longa listaram PT-BR/EN; Gundam 00 listou EN. Magic TV é anunciado como Sub pelo publicador, sem faixa CC manual retornada — a legenda pode estar na imagem. Não foi auditada a tradução integral.

Use o controle CC do player oficial para selecionar as faixas disponíveis. A presença de faixa no metadado não garante sua seleção automática em todo aparelho.

## Desejos não atendidos e reservas

Ver `DT-002-UNAVAILABLE.md`. A ausência da grade não prova inexistência mundial de uma publicação autorizada. Galaxy Angel, ARIA e Utena tinham fontes oficiais, mas as edições investigadas retornaram bloqueio nesta conexão; a variante Sub de Galaxy Angel também falhou. Magic OVA 3–6, sem 1–2 utilizáveis, não foi usada para começar uma história no episódio 3.[1][2][14]

O índice tsuzuki foi investigado como descoberta, não como licença. anime.ad respondeu 403 e não foi contornado.[7][8]

## Testes e preservação

Executado `tools/check.py --browser --live`: **35 testes determinísticos passaram** — 18 Node, 4 assets, 1 servidor, 1 classificador de evidências, 9 cenários legados e 2 cenários da grade nova. O diagnóstico de rede legado também passou. A verificação individual dos 48 é separada desses 35 testes.

Os cenários antigos conservam os dados DT-001 como fixtures; os novos cenários usam os JSON de produção DT-002. Assim, não trocamos uma expectativa “Elephants Dream” por qualquer título só para fazer o teste passar. A fixture inicialmente revelou um erro do callback de rota do teste, corrigido sem alterar o aplicativo.

Foram cobertos: catálogo e referências, duplicatas, cada segundo do dia, meia-noite, ordem narrativa, reprises declaradas, limites de repetição, três tipos de vinheta, offset, reabertura, guia e fallback 150 com retorno automático ao próximo horário. O classificador rejeita prontidão sem playback, vídeo errado, duração de anúncio incompatível e playhead parado.

`evidence/dt002/preservation.json` confirma hashes inalterados de layout, identidade e arquivos centrais. Baseline e reversão: `DT-002-INITIAL-STATE.md`. Saída final arquivada: `evidence/dt002/final-tests.json`.

## Editar e publicar

Veja `DT-002-EDITING.md` para manutenção sem rebuild. Pacotes: `dist/disk-television-0.2-pages.zip` e `dist/disk-television-0.2-source.zip`. O primeiro contém somente o runtime; o segundo contém fonte, pesquisa, testes e evidências. Extraia o pacote Pages na raiz do repositório autorizado e configure GitHub Pages. Nada foi publicado automaticamente.

Limitações: catálogo de estreias, não temporadas completas; muitos favoritos bloqueados; CC/áudio e autoplay dependem do player/browser; conteúdos Gundam são ofertados em campanha temporal e exigem revalidação próxima à expiração; direitos/região podem mudar. O horário depende do relógio do aparelho. Não houve Samsung física, teste remoto HTTPS publicado ou sessão real de 24h.

DT-003 fica autorizada para início local após esta base estável, com novo backup e preservação destes JSON. Seu escopo não altera a curadoria acima.

## Sources

[1] https://www.youtube.com/playlist?list=PLrrh84y760v8_JIjTPgf-0D0MMNHJBlYI
[2] https://www.youtube.com/playlist?list=PLrrh84y760v9xDNuOiG6x1DsCG70LVQi7
[7] https://anime.ad
[8] https://tsuzuki-anime.github.io/en/platform/youtube.html
[9] https://animation.geidai.ac.jp
[10] https://en.gundam-official.com/feature/gwoy
[11] https://tmsanime.com/anime-on-tms-official-channel
[12] https://www.glitchprod.com
[13] https://www.kyoto-seika.ac.jp/edu/manga/animation
[14] https://www.youtube.com/@nozomient/about
[15] https://www.youtube.com/watch?v=j01Hg4QJ6NE
