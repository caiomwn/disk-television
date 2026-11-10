# DT-002 — edição simples da programação

O site continua estático. Não existe painel ou rebuild obrigatório.

## Adicionar uma obra

1. Pesquise uma publicação integral em canal de autor, estúdio ou distribuidor comprovado. Não confunda trailer, review, AMV ou compilação de cenas com episódio.
2. Registre primeiro fora da grade, em um JSON de pesquisa: `id`, `youtubeId` original de 11 caracteres, título correto, criador/canal, ano da obra, duração real inteira, idioma/legendas, `kind`, `series`, `season`, `episodeNumber`, origem e evidência de legitimidade.
3. Verifique metadados individualmente, sem baixar mídia. `yt-dlp --skip-download --dump-single-json URL` não substitui o ensaio incorporado.
4. Rode `.venv/Scripts/python.exe tools/verify_embeds.py caminho/para/candidatos.json --out docs/evidence/dt002/playback-results.json`. O comando acrescenta resultados ao registro e não publica nada. `--retry-failed` reavalia os não confirmados; `--force` reavalia todos os candidatos passados.
5. Só admita na grade principal resultados `actualPlayback: true`. A verificação é de desktop e da conexão observada, não de Samsung/região mundial/direitos novos.
6. Acrescente o objeto aprovado a `data/catalog.json`, com a mesma estrutura dos novos itens, prova correspondente e `broadcastEnabled: true` quando realmente o agendar.
7. Insira o `id` em uma `rotation` de `data/schedule.json`, preservando episódio anterior, seguinte e limites do bloco.

## Editar a grade

`start` é contado em segundos desde meia-noite de Brasília. Cada bloco termina no início do próximo, e o último em 86400. Mantenha `epoch`, ciclo e durações das vinhetas, a menos que você queira deliberadamente deslocar a emissora.

A `rotation` é uma sequência editorial, não uma escolha do espectador. O compilador tenta repeti-la até fechar o bloco. Por isso a edição DT-002 monta listas quase do tamanho do bloco: não deixe sobras maiores que o primeiro programa se não quiser uma nova volta da rotação. Um filme precisa caber completo; não estime sua duração ou corte os créditos para encaixar.

`explicitReprises` documenta quais séries podem reiniciar no episódio 1. Rayearth progride de 1–4 em ANIME ARCHIVE para 5–8 em MOE SIGNAL; o bloco noturno é uma reprise declarada de 1–8. A rotina de testes detecta saltos e retrocessos não declarados. O limite `editorialMaxDailyPlays` evita repetição excessiva.

## Remover ou reservar

Remova o `id` de todas as rotações, depois marque `broadcastEnabled: false` e escreva `offAirReason`. O campo é inventário editorial, **não um filtro automático do motor**: só trocar essa flag sem retirar a referência da grade não basta. Da mesma forma, `verification.status` documenta a checagem estática; o site não faz pesquisa de disponibilidade em segundo plano. Os testes validam a política, e o fallback cuida de falhas no momento da exibição.

Os dois vídeos de SEED Destiny exemplificam reserva verificada: continuam no catálogo, mas não são transmitidos nesta edição.

## Validar e exportar

Na pasta do projeto:

    node tools/export-schedule.mjs
    .venv/Scripts/python.exe tools/check.py --browser --live
    .venv/Scripts/python.exe tools/report_dt002.py
    .venv/Scripts/python.exe tools/package.py

Neste ambiente, se `node` direto apresentar erro de TTY, chame o executável via Python subprocess; `tools/check.py` já faz isso para os testes. A exportação deve acontecer antes do relatório para que o JSON compilado corresponda à grade atual.

O relatório DT-002 também compara a identidade ao backup inicial. Depois de uma missão audiovisual autorizada, esse comparador histórico não deve ser interpretado como veto às alterações autorizadas dessa missão.

O script `integrate_dt002.py --apply` reconstrói especificamente a seleção desta missão a partir da pesquisa/provas. **Não o use para manutenção cotidiana depois de editar os JSON manualmente**, pois ele sobrescreve as alterações com o plano editorial registrado da DT-002.

Envie os JSON alterados ao repositório autorizado ou gere o ZIP atualizado. Não é preciso manter o servidor local nem Python em execução depois de publicar no GitHub Pages. Revalide fontes temporárias, especialmente Gundam, antes de depender da grade por longos períodos.
