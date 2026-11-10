# DISK TELEVISION — MISSÃO DT-003
## Evolução audiovisual, vinhetas sonoras e experimento de apresentação A/B/C

### INSTRUÇÃO DE EXECUÇÃO

Esta é uma missão adicional para a DISK TELEVISION.

**Não interrompa a missão DT-002, atualmente em execução.**

Registre esta missão como próxima etapa. Quando a DT-002 terminar, seus resultados forem integrados e os testes estiverem concluídos, inicie automaticamente a DT-003.

Não solicite uma nova autorização apenas para começar o desenvolvimento local.

Se a DT-002 terminar com problemas, preserve seus resultados, identifique os bloqueios e só prossiga quando houver uma base funcional estável.

Projeto:
`C:\Users\padoka77\disk-television`

### 1. OBJETIVO

Evoluir a apresentação audiovisual da DISK TELEVISION, aproximando-a da experiência de uma emissora japonesa retrofuturista dos anos 1990–2000.

A missão possui três objetivos:

1. Implementar três modos de apresentação para comparação.
2. Adicionar identidade sonora original às vinhetas.
3. Refinar a identidade visual usando novas referências.

O objetivo não é adicionar funcionalidades de streaming ou alterar a programação editorial.

Preserve o catálogo e a grade entregues pela DT-002.

### 2. EXPERIMENTO DE PLAYER A/B/C

Na tela inicial de sintonia, adicionar três opções claramente identificadas:

**PLAYER A — CLEAN**

- Vídeo ocupando a maior área possível.
- Interface externa discreta.
- Informações de programa e controles exibidos temporariamente.
- Sem sobreposições sobre o player do YouTube.

**PLAYER B — BROADCAST FRAME**

- Vídeo com uma moldura audiovisual discreta.
- Logotipo e informações posicionados fora da área do iframe.
- Aparência de canal de televisão.
- Preservação integral da área do player oficial.

**PLAYER C — EXPERIMENTAL**

- Investigar uma apresentação visual mais próxima de uma transmissão convencional, com elementos de identidade sobrepostos.
- Testar tecnicamente o comportamento de camadas HTML, fullscreen, navegação e controles.
- Não presumir que overlays sobre vídeos do YouTube sejam permitidos.
- Consultar as políticas oficiais do YouTube antes da implementação.
- Se o overlay direto conflitar com essas políticas, implementar uma alternativa visual equivalente e conforme, documentando a diferença.

O modo C não deve bloquear anúncios, controles, avisos ou interações obrigatórias do YouTube.

### 3. REGRAS DO EXPERIMENTO

Os três modos devem:

- Utilizar a mesma grade.
- Reproduzir o mesmo programa correspondente ao relógio.
- Compartilhar o mesmo catálogo.
- Preservar as vinhetas.
- Permitir troca de modo sem perder a continuidade temporal.
- Funcionar com mouse e teclado.
- Ser navegáveis por controle remoto, quando o navegador permitir.

O objetivo é comparar exclusivamente a apresentação e a experiência de uso.

Não construir três motores de transmissão independentes.

Criar uma seleção simples na tela inicial e permitir retornar à seleção durante os testes.

A escolha do modo deve persistir durante a sessão, mas deve ser fácil de alterar.

Não selecionar um vencedor automaticamente.

### 4. COMPATIBILIDADE COM SMART TV

O usuário testará os três modos no computador e, posteriormente, numa Smart TV Samsung.

Preparar a aplicação para esses testes.

Investigar:

- Navegação com setas e Enter.
- Botão Voltar.
- Fullscreen.
- Restrições do navegador Tizen.
- Reprodução automática.
- Comportamento do iframe.
- Retorno de foco após transições.
- Continuidade após bloqueios de reprodução.

Não declarar compatibilidade com Samsung sem teste real.

Criar um roteiro curto de validação manual para cada modo.

### 5. IDENTIDADE SONORA DAS VINHETAS

As vinhetas atuais devem receber áudio.

Pesquisar referências de:

- Identificações de emissoras japonesas dos anos 1990–2000.
- Interfaces de CD/DVD e videogames da época.
- Música eletrônica japonesa Y2K.
- Synthpop.
- Future funk.
- Ambient eletrônico.
- Jingles curtos de televisão.

A identidade sonora deve combinar com a DISK TELEVISION: futurista, delicada, ligeiramente nostálgica, com brilho digital.

Evitar sons genéricos de glitch, alarmes e efeitos excessivamente agressivos.

#### Entregáveis sonoros

Criar ou obter legalmente:

- Um jingle principal de identificação, aproximadamente 5–10 segundos.
- Um som curto para "A seguir".
- Uma vinheta sonora noturna mais atmosférica.

Os agentes podem pesquisar, selecionar e baixar arquivos de áudio de fontes que permitam sua utilização e redistribuição no projeto.

Verificar licenças e atribuições antes de integrar qualquer arquivo.

Não baixar músicas comerciais sem autorização.

Se a pesquisa não encontrar material adequado, produzir áudio original por síntese, composição programática ou ferramentas de geração disponíveis.

O resultado deve ser composto por arquivos reais de áudio, não apenas descrições.

Preferir formatos leves e compatíveis com navegadores.

### 6. INTEGRAÇÃO DO ÁUDIO

O áudio das vinhetas deve:

- Iniciar junto com a animação.
- Terminar naturalmente antes da próxima atração.
- Respeitar o estado de som ligado/desligado.
- Evitar sobreposição com o áudio do programa seguinte.
- Não reiniciar desnecessariamente ao recalcular a grade.
- Respeitar restrições de autoplay.
- Não interromper a transmissão em caso de falha.

Testar transições entre YouTube, vinheta sonora e próximo vídeo.

### 7. IDENTIDADE VISUAL

Existe uma nova referência visual para o logotipo DISK TELEVISION, com:

- Tipografia geométrica inclinada.
- Acabamento branco-prateado iridescente.
- Azul, rosa e violeta.
- Disco óptico.
- Órbita.
- CH 99.
- Referências à cultura audiovisual japonesa Y2K.

O usuário fornecerá o arquivo de referência no diretório do projeto.

Caminho sugerido:
`C:\Users\padoka77\disk-television\references\disk-television-logo-reference.png`

**Antes de usar, verifique se o arquivo realmente existe. Não presuma que foi copiado.**

Se estiver disponível, utilize-o como referência visual para refinar a identidade existente.

Não substitua o logotipo atual por uma imagem rasterizada sem preservar uma fonte editável.

Gerar versões adequadas para:

- Tela de sintonia.
- Vinhetas.
- Identificação compacta.
- Favicon.
- Fundos claros e escuros, quando necessário.

Preservar o nome completo DISK TELEVISION.

### 8. DIREÇÃO ARTÍSTICA

A identidade atual é limpa e funcional, mas ainda bastante sóbria.

Evoluir gradualmente para uma estética mais próxima de uma emissora japonesa alternativa Y2K.

Explorar:

- Reflexos de mídia óptica.
- Movimento orbital.
- Brilho digital.
- Tipografia dinâmica.
- Transições audiovisuais.
- Composições assimétricas.
- Animações suaves e precisas.

Evitar exageros.

Não transformar o canal numa interface de videogame ou num festival permanente de efeitos.

As vinhetas devem ter mais personalidade, mas o conteúdo deve continuar sendo o protagonista.

### 9. PRESERVAÇÃO E SEGURANÇA

Antes de começar:

- Registrar o estado final da DT-002.
- Criar uma forma de reverter as alterações.
- Inspecionar os testes existentes.
- Identificar os componentes afetados.

Não alterar a curadoria nem reconstruir o motor de programação sem necessidade comprovada.

Não modificar repositórios remotos.

Não publicar automaticamente.

### 10. TESTES E ENTREGÁVEIS

Entregar:

1. Tela inicial com seleção A/B/C.
2. Três modos de apresentação funcionais.
3. Áudio integrado às três vinhetas.
4. Arquivos sonoros e respectivas licenças ou documentação de autoria.
5. Identidade visual refinada, caso a referência esteja disponível.
6. Testes automatizados e manuais.
7. Comparação técnica dos modos.
8. Roteiro de testes no PC e na Samsung.
9. Capturas de tela de cada modo.
10. Pacote atualizado preparado para GitHub Pages.

Verificar que os testes da DT-002 continuam passando.

### 11. CRITÉRIO DE SUCESSO

A missão será concluída quando o usuário puder:

- Abrir a DISK TELEVISION.
- Escolher Player A, B ou C.
- Assistir à mesma programação em qualquer modo.
- Ouvir vinhetas originais entre atrações.
- Comparar visualmente as três experiências.
- Testar posteriormente os modos na Smart TV.
- Escolher qual apresentação deverá se tornar definitiva.

**Não remover os modos alternativos até que o usuário escolha um vencedor.**

### 12. EXECUÇÃO

Aguarde a conclusão da DT-002.

Depois, execute a DT-003 com autonomia, delegando tarefas aos agentes disponíveis.

Pesquise antes de tomar decisões que envolvam compatibilidade, políticas do YouTube ou licenças de áudio.

Não interrompa a execução para solicitar preferências estéticas menores.

Entregue resultados funcionais, não apenas propostas.

**DISK TELEVISION — CH 99. A transmissão continua.**