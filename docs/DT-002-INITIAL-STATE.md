# DISK TELEVISION — DT-002: estado inicial e reversão

Inspeção em 10 de novembro de 2026. Projeto encontrado em `C:/Users/padoka77/disk-television`, sem diretório `.git`.

## Estado preservado

- Catálogo inicial: 10 vídeos Blender.
- Grade: 86400 segundos, seis blocos; epoch `2026-01-01T03:00:00Z`.
- Antes de editar o projeto, foi criado e validado um ZIP dos 47 arquivos de fonte/documentação, excluindo `.venv`, caches, `.git` e pacotes `dist`.
- Backup: `C:/Users/padoka77/disk-television-backups/DT-002-before-20261110-102715/project.zip`.
- Manifesto SHA-256: `C:/Users/padoka77/disk-television-backups/DT-002-before-20261110-102715/manifest.json`.
- Cada membro do ZIP foi comparado ao hash do arquivo original. A integridade foi confirmada antes de qualquer alteração no projeto.

## Baseline executada

Executado `.venv/Scripts/python.exe tools/check.py --browser --live`: 14 testes Node, 4 de assets, 1 de servidor e 9 de integração passaram. O teste de rede confirmou Tears of Steel e Elephants Dream reais, com vinhetas e avanço automático. Essa é a baseline anterior à expansão.

## Escopo de preservação

Não alterar `assets/`, `styles.css`, `index.html`, `legal.html`, `src/app.js`, `src/playout.js` ou o motor `src/schedule.js` sem uma necessidade comprovada. A missão deve se concentrar em JSON de catálogo/grade, ferramentas de pesquisa/verificação, testes editoriais e documentação. Ao final, comparar os hashes desses arquivos protegidos ao manifesto.

## Reverter

1. Feche o servidor local e faça uma cópia da pasta atual se quiser guardar a edição DT-002.
2. Extraia o ZIP de backup em uma pasta vazia para restaurar exatamente a fonte da 0.1. A `.venv` não foi incluída porque não é fonte nem runtime publicado.
3. Abra a pasta restaurada com um servidor HTTP, ou copie os arquivos restaurados por cima do projeto depois de guardar a edição atual.
4. Para reverter somente programação, restaure `data/catalog.json` e `data/schedule.json` do ZIP e regenere os exports da grade. Restaure os testes DT-001 junto com os dados se também quiser reproduzir o conjunto original.

Nenhuma publicação remota está autorizada nesta missão.
