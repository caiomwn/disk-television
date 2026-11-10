# DISK TELEVISION — CH 99

## Conceito: sinal gravado, não interface de streaming

Uma assinatura de emissora com presença de objeto: letras largas, cortes geométricos e inclinação para a frente. **DISK** e **TELEVISION** permanecem sempre empilhados e escritos por inteiro. O pequeno disco remete à mídia física; o reflexo gelo/lilás/rosa sugere iridescência sem arco-íris, glow ou cromado ostensivo.

A transmissão é protagonista. O quadro de aplicação é preto, 16:9, com espaço negativo. Não usar cards de catálogo, dashboards, terminal, estética hacker, grades neon, scanlines ou glitch.

## Arquivos entregues

| Arquivo | Formato e uso |
|---|---|
| `assets/logo.svg` | Mestre editável, `viewBox="0 0 960 420"`, fundo transparente. Letras construídas com paths próprios, sem fontes ou imagens incorporadas. |
| `assets/logo.png` | Raster RGBA, **2400 × 1050 px**, transparência real. Não contém um retângulo preto nem um padrão xadrez. |
| `assets/favicon.svg` | Prancheta quadrada `960 × 960`, tamanho intrínseco `96 × 96`, base preta de cantos arredondados e assinatura completa. |
| `docs/IDENTITY.md` | Direção, regras de aplicação e três propostas CSS, sem modificar o app. |

### Edição do SVG

Grupos nomeados: `disk`, `television`, `channel`, `disc`; paths de letras possuem IDs individuais. Os gradientes editáveis são `alloy` e `disc-sheen`. A posição e escala das duas linhas estão nos respectivos `transform`. O título acessível é **DISK TELEVISION — CH 99**. Os contadores internos das letras usam `fill-rule="evenodd"`.

Todos os desenhos de letras, disco e grafismos foram construídos para esta entrega. Não foram usados logotipos, fontes, imagens, ícones ou desenhos de terceiros. Ferramentas de rasterização não são assets incorporados à arte. Isso descreve a origem do desenho, não constitui busca de anterioridade de marca.

## Ambiente de geração

Além da `.venv` local de QA, a etapa de arte instalou Pillow 13.0.0 e resvg-py 0.5.0 no site-packages do usuário do Python 3.13. Essa instalação fora da pasta foi confirmada ao final; não é dependência do site nem dos ZIPs de publicação. Não foi feita desinstalação automática, para não remover ferramentas de que outro trabalho possa depender. Nenhum outro projeto foi editado.

## Paleta

| Token sugerido | Hex | Papel |
|---|---|---|
| `--disk-television-black` | `#08090C` | Quadro principal, fundo do favicon |
| `--disk-television-ice` | `#EFF5F7` | Leitura e corpo da assinatura |
| `--disk-television-purple` | `#A998CE` | Identificação do canal e detalhe do disco |
| `--disk-television-alloy` | `#CEC2EC` | Transição do reflexo |
| `--disk-television-pink` | `#DFA4C2` | Índice horizontal e reflexo do disco |
| `--disk-television-pink-light` | `#E4AAC8` | Extremidade suave do gradiente das letras |

O preto é campo de aplicação, não preenchimento do PNG. A assinatura clara foi desenhada para fundo escuro; não usá-la sobre branco sem uma versão escura redesenhada.

## Regras de aplicação

- Preservar proporção de **16:7** do arquivo da assinatura; o **quadro de transmissão**, não o logo, é 16:9.
- Não condensar, esticar, separar as palavras, substituir por iniciais ou escrever somente DISK como assinatura.
- A inclinação faz parte da construção. Não adicionar outra inclinação ao arquivo completo.
- Manter o respiro já incorporado ao SVG e não cortar o disco ou o índice inferior.
- Para um quadro 1920 × 1080, usar inicialmente a imagem com largura de 768 px em uma vinheta. Durante obras do YouTube, manter a identificação exclusivamente na faixa externa ao iframe, nunca como sobreposição ao player, seus controles ou anúncios.
- Evitar o logo completo abaixo de 240 px de largura em áreas de conteúdo; a identificação pequena do canal é secundária.
- O favicon preserva deliberadamente o nome completo, sem monograma. Em 16–32 px, o navegador exibirá sua silhueta, não todas as letras de forma legível. Não prometer leitura nominal nesse tamanho; 96 px ou mais favorece a leitura.
- Sem brilho externo, sombra colorida, contorno neon, pulsação contínua ou flash branco.
- A marca não deve ficar animando sobre a transmissão principal. Rodar a vinheta uma vez em uma transição editorial.

## Vinhetas integradas na versão 0.1

A aplicação integra três vinhetas funcionais em `styles.css` e `src/app.js`: `station` (identificação), `next` (título real do próximo programa) e `night` (frequência noturna). A forma de continuidade `continuity` reaproveita a composição noturna para fechar blocos sem cortar vídeos. Órbitas discretas, frases e pequenas assinaturas sonoras originais diferenciam as variantes. Capturas verificadas estão em `docs/evidence/ident-*.png`.

As propostas abaixo são estudos auxiliares, não o código executado pelo receptor. A integração final usa slots reais da grade e mantém o iframe oculto e interrompido durante as vinhetas.

## Três vinhetas CSS propostas

**Somente propostas documentadas. Nenhum stylesheet ou arquivo do aplicativo foi criado ou alterado por esta entrega.** Usar uma classe de variante por vez. A integração decide quando inserir e remover o quadro; nenhuma variante muda a reprodução, exige JavaScript ou depende de serviços externos.

### Estrutura comum

O exemplo considera caminhos a partir da raiz pública do aplicativo; ajustar `src` à estrutura real da integração. Não há solicitação para reorganizar o app.

```html
<div class="disk-television-ident disk-television-ident--press">
  <img class="disk-television-ident__logo"
       src="assets/logo.svg"
       width="960" height="420"
       alt="DISK TELEVISION — CH 99">
</div>
```

```css
.disk-television-ident {
  position: relative;
  display: grid;
  place-items: center;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  isolation: isolate;
  background: #08090c;
}
.disk-television-ident__logo {
  display: block;
  width: 40%;
  height: auto;
  transform-origin: center;
}
```

### 1. Prensagem — 1,2 s

Uma aproximação curta e física: a assinatura sobe 8 px e ganha presença sem bounce. A versão mais discreta para abertura de sinal.

```css
.disk-television-ident--press .disk-television-ident__logo {
  animation: disk-television-press 1200ms cubic-bezier(.2,.7,.2,1) both;
}
@keyframes disk-television-press {
  0% { opacity: 0; transform: translateY(8px) scale(.985); }
  45%, 100% { opacity: 1; transform: translateY(0) scale(1); }
}
```

### 2. Leitura óptica — 1,4 s

O nome inteiro é revelado por uma abertura horizontal única, como o início de leitura de um disco. Não há barras sobre o conteúdo nem ruído digital.

```css
.disk-television-ident--read .disk-television-ident__logo {
  animation: disk-television-read 1400ms cubic-bezier(.2,.7,.2,1) both;
}
@keyframes disk-television-read {
  0% { opacity: 0; clip-path: inset(0 100% 0 0); }
  15% { opacity: 1; }
  72%, 100% { opacity: 1; clip-path: inset(0); }
}
```

### 3. Reflexo de borda — 1,8 s

A assinatura aparece inteira; uma faixa translúcida de baixa opacidade atravessa somente sua área uma vez. O reflexo é um elemento de composição, não um filtro permanente no logo.

```css
.disk-television-ident--sheen .disk-television-ident__logo {
  animation: disk-television-arrive 500ms ease-out both;
}
.disk-television-ident--sheen::after {
  content: "";
  position: absolute;
  inset: 31% 28%;
  pointer-events: none;
  opacity: 0;
  background: linear-gradient(110deg,
    transparent 42%, rgb(239 245 247 / .13) 49%,
    rgb(223 164 194 / .09) 53%, transparent 60%);
  transform: translateX(-115%);
  animation: disk-television-sheen 1800ms ease-in-out both;
}
@keyframes disk-television-arrive {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes disk-television-sheen {
  0%, 18% { opacity: 0; transform: translateX(-115%); }
  35%, 65% { opacity: 1; }
  88%, 100% { opacity: 0; transform: translateX(115%); }
}
```

### Movimento reduzido — obrigatório ao integrar

```css
@media (prefers-reduced-motion: reduce) {
  .disk-television-ident .disk-television-ident__logo {
    animation: none;
    opacity: 1;
    transform: none;
    clip-path: none;
  }
  .disk-television-ident::after {
    animation: none;
    display: none;
  }
}
```

As três alternativas terminam com a marca inteira estática e não usam repetição infinita. Os trechos são propostas de integração, não componentes testados dentro do aplicativo.

## Verificação dos assets

- SVGs analisados como XML válido e rasterizados sem fontes do sistema.
- Logo PNG: RGBA, 2400 × 1050, alpha mínimo 0 e máximo 255, pixels transparentes e opacos presentes; contorno visível não encosta na borda.
- Inspeção visual do PNG: DISK e TELEVISION completos, canal e disco sem cortes.
- Nenhuma dependência de rede para exibir os três assets.
