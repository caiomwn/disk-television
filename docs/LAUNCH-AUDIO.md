# CH 99 — áudio de lançamento

## Entrega e autoria

Três composições instrumentais originais, sintetizadas offline pelo código e pela partitura editável de `tools/generate_station_audio.py`. Assinatura melódica F#–A–E–D, pads senoidais, parciais de vidro, reflexões estéreo finitas e fades. Não há samples, soundfonts, transcrição de referência, voz, serviço de IA, downloads ou dependência paga. O trabalho parcial de síntese foi preservado e executado; não foi substituído por sons de biblioteca.

Copyright (c) 2026 DISK TELEVISION contributors. O script, sua partitura e os seis arquivos de áudio originais são disponibilizados sob MIT (texto abaixo). Isso não concede direitos sobre vídeos ou outros materiais de terceiros da emissora.

Arquivos em `assets/audio/`:

| Variante | WAV original | MP3 de distribuição | Duração decodificada |
| --- | --- | --- | --- |
| station | `ident-station.wav` | `ident-station.mp3` | 8,0 s |
| next | `ident-next.wav` | `ident-next.mp3` | 2,6 s |
| night | `ident-night.wav` | `ident-night.mp3` | 11,0 s |

O som não precisa preencher toda a vinheta visual: a abertura pode durar 18 s e o link 4 s. Continuidade longa usa `night` uma única vez, sem loop. Sem piloto CYBERIA e sem locução nesta entrega.

## Reprodução e contrato

`src/station-audio.js` exporta `StationAudio` como ESM, mantendo injeção de `contextFactory`, `fetcher` e `baseUrl`:

- `prepare()`: promessa reutilizada; cria contexto sem tocar nem chamar resume, carrega as três variantes em paralelo. Para cada variante tenta MP3 e depois WAV em caso de falha HTTP, rede ou decode; falha de uma não impede as outras.
- `unlock()`: chamar diretamente no gesto do usuário. Cria o contexto e chama `resume()` antes do primeiro await; falhas não escapam.
- `update(clock, { enabled })`: recebe `{ slot: { id, type, variant, duration }, elapsed, startMs }`, com tempos em segundos exceto `startMs`. Chamar em cada tick do relógio público, inclusive depois de `prepare()` terminar. Só inicia com contexto `running` e buffer pronto. Uma decodificação tardia espera o próximo tick e usa o `elapsed` desse tick, não o offset antigo.
- A chave absoluta é `JSON.stringify([startMs, slot.id])`. Ticks da mesma chave e fim natural não reiniciam a fonte. Um novo ident corta o anterior antes de criar outra fonte. `continuity` seleciona o buffer `night`.
- A janela termina no menor valor entre duração do buffer, duração do slot e limite de 4 s (`next`) ou 18 s (demais). Entrada após essa janela permanece silenciosa.
- `stop()`: idempotente; corta/desconecta a fonte e permite retomar após gesto/GUI no offset corrente. Usar ao abrir guia, ocultar a estação ou interromper intencionalmente. Vídeo e `enabled: false` também chamam stop. O controlador não altera a programação nem tenta controlar o player de vídeo.
- `getState()`: `readyVariants`, `activeKey`, `contextState`, `starts`, `errorCount`. Erros de contexto, resume, fetch, decode e criação/conexão/início de fonte ficam contidos; falhas não marcam a chave como tocada.

A integração de GUI/mute/visibilidade é responsabilidade de quem chama o contrato. Estes arquivos não modificam o aplicativo, HTML, CSS ou a grade.

## Regenerar e verificar

Na raiz do projeto, usando Python local e FFmpeg/ffprobe já instalados:

```sh
python tools/generate_station_audio.py
python tools/generate_station_audio.py --verify-only
```

Se necessário, passar `--ffmpeg CAMINHO` e `--ffprobe CAMINHO`; também aceita as variáveis `FFMPEG` e `FFPROBE`. Não instala nem baixa ferramentas. Só sobrescreve os seis arquivos `assets/audio/ident-*`. As notas, envelopes, pans e amplitudes estão em `SCORES` e `PALETTE`; WAV é PCM 16-bit estéreo, 44.100 Hz; MP3 usa libmp3lame 192 kbit/s. A geração é determinística com a mesma versão de Python/FFmpeg; versões de encoder diferentes podem mudar bytes do MP3.

No Git Bash/Windows, executar Node via Python evita o problema de TTY:

```sh
python -c "import subprocess,shutil; p=subprocess.run([shutil.which('node'),'--test','tests/station-audio.test.mjs'],capture_output=True,text=True); print(p.stdout); print(p.stderr); raise SystemExit(p.returncode)"
```

## Evidência real de execução — 10 de novembro de 2026

Geração concluída e os **seis arquivos decodificados integralmente** por FFmpeg com `-xerror`, inspecionados por ffprobe e medidos com `volumedetect`. Todos: 44.100 Hz, dois canais, amostras finitas, estéreo não idêntico, começo/fim suaves e pico abaixo de −3 dBFS. Medições do PCM efetivamente decodificado:

| Arquivo | Codec | Segundos | Pico dBFS | RMS dBFS | volumedetect mean / max dB |
| --- | --- | ---: | ---: | ---: | --- |
| ident-station.wav | pcm_s16le | 8,0 | −7,6178 | −20,0003 | −20,0 / −7,6 |
| ident-station.mp3 | mp3 | 8,0 | −7,8759 | −20,2648 | −20,3 / −7,9 |
| ident-next.wav | pcm_s16le | 2,6 | −7,3511 | −20,0003 | −20,0 / −7,4 |
| ident-next.mp3 | mp3 | 2,6 | −7,6162 | −20,2648 | −20,3 / −7,6 |
| ident-night.wav | pcm_s16le | 11,0 | −8,7102 | −20,0003 | −20,0 / −8,7 |
| ident-night.mp3 | mp3 | 11,0 | −8,9732 | −20,2647 | −20,3 / −9,0 |

**24 testes de áudio Node passaram, zero falhas**, incluindo regressões observadas em vermelho antes das correções: contexto ausente/suspenso, fallback MP3→WAV, independência entre variantes, corte entre idents, offset corrente, continuidade sem loop, limites de duração, erros de fonte e unlock sem prepare. As operações Web Audio desses testes usam um contexto duplo; não equivalem a decode/playback de navegador. A decodificação real dos arquivos foi a de FFmpeg acima.

Uma segunda geração preservou exatamente os SHA-256 dos seis arquivos (4.334.331 bytes no total); `--verify-only` também validou os seis novamente. A suíte completa naquele momento executou 46 testes: 45 passaram e um falhou fora do escopo de áudio, em `tests/launch-schedule.test.mjs` (`launch never repeats the identical work back-to-back`, repetição adjacente de `dt002-alt-blink-in-the-desert`). Grade e dados não foram alterados nesta tarefa.

Não houve escuta humana documentada, teste físico Samsung/Smart TV ou promessa de compatibilidade com todos os navegadores. Políticas de autoplay, dispositivo de saída e integração do app continuam exigindo verificação no ambiente de destino.

## MIT License — código, partitura e áudio originais desta entrega

Copyright (c) 2026 DISK TELEVISION contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
