# DISK TELEVISION — revisão independente e resolução

Revisão somente leitura por agente separado em 10 de novembro de 2026. Os testes citados pelo revisor pertencem ao snapshot intermediário; a execução integrada final está em `TEST-RESULTS.md` e `evidence/test-run.json`.

## Achado alto: termos e privacidade ausentes da interface

Confirmado por inspeção e por teste que inicialmente falhou: não havia aviso antes da sintonia nem link permanente. As Developer Policies exigem termos e política de privacidade acessíveis com referência aos serviços YouTube e à política do Google.[4]

Resolvido na implementação:

- `legal.html` contém termos próprios, referência e link aos termos do YouTube, política de privacidade, informações sobre cookies/anúncios/terceiros, estados mantidos em memória e ausência de login/OAuth/backend próprio.
- A tela inicial informa a aceitação dos termos ao sintonizar e permite ler o aviso antes de iniciar conexões com o player.
- Há acesso permanente fora do iframe e navegação de volta à emissora.
- O teste de regressão verifica presença, navegação, URLs oficiais e ausência de solicitação à IFrame API antes de sintonizar.

O aviso ainda deve ser revisado pelo publicador para sua configuração e contato público. Esta correção técnica não representa certificação jurídica ou avaliação de todas as obrigações aplicáveis.

## Achado médio: início automático com player fora da área visível

Confirmado em teste reproduzível no Chrome, viewport 640 × 320. O teste primeiro confirma que metade ou menos da imagem está visível; na versão anterior, a troca de horário ainda chamava `loadVideoById`. A regra oficial exige mais da metade do player visível antes de iniciar reprodução automática.[2]

Resolvido na implementação:

- `pictureVisible()` mede a interseção do retângulo do iframe com o viewport; usa a posição do palco quando o player ainda está oculto.
- O motor continua consultando o relógio, mas adia novos loads quando a proporção visível é menor ou igual a 0,5; reprodução existente é interrompida.
- Ao voltar à imagem, a grade é recalculada e o vídeo correto entra no offset atual.
- `focus({preventScroll:true})` evita rolagem involuntária ao mover o foco para os controles após sintonia.
- O parâmetro inicial `autoplay` do iframe é zero; o início via `loadVideoById` passa pelo controle geométrico.
- O teste que inicialmente falhou passou com retorno automático a Elephants Dream no offset de 2 segundos.

## Resultado após correções

28 testes determinísticos passaram, e o teste de rede confirmou reprodução real de Tears of Steel, vinhetas e início automático de Elephants Dream. Não restou achado conhecido bloqueante desta revisão. Não foram testadas Smart TVs físicas ou todas as condições de anúncios e consentimento.

## Sources

[2] https://developers.google.com/youtube/terms/required-minimum-functionality
[4] https://developers.google.com/youtube/terms/developer-policies
