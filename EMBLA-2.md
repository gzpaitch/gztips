# Embla Carousel Guide

Este arquivo documenta dois problemas comuns ao usar Embla Carousel em projetos React/Next.js com Tailwind:

1. `loop` com clones visíveis ou comportamento estranho
2. falta de imersão visual por causa de padding horizontal herdado do layout

Use este guia para diagnosticar rapidamente qual problema você tem e aplicar o padrão correto.

## 1. Loop e Clones

### Problema

Quando `loop: true` é usado com slides menores que 100% da largura, o último slide pode aparecer junto com o primeiro, ou o carousel pode parecer "quebrado" nas extremidades.

### Causa

O Embla cria clones para o loop funcionar. O problema costuma aparecer quando há uma combinação de:

- `loop: true`
- slides com largura parcial, como `flex-[0_0_90%]`
- `gap-*` no track
- opções como `align: 'start'`, `containScroll` ou `dragFree`

### Configuração incorreta

```tsx
const [emblaRef, emblaApi] = useEmblaCarousel({
  align: "start",
  loop: true,
  containScroll: "trimSnaps",
});

<div className="flex gap-4">
  {items.map((item, index) => (
    <div key={index} className="flex-[0_0_90%] min-w-0">
      <Card />
    </div>
  ))}
</div>;
```

### Configuração recomendada

```tsx
const [emblaRef, emblaApi] = useEmblaCarousel({
  loop: true,
  slidesToScroll: 1,
});

<div className="flex">
  {items.map((item, index) => (
    <div key={index} className="flex-[0_0_100%] min-w-0 px-2">
      <Card />
    </div>
  ))}
</div>;
```

### Regras práticas

- Use `slidesToScroll: 1` quando houver loop.
- Evite `align: 'start'`, `containScroll` e `dragFree` até serem realmente necessários.
- Não use `gap-*` diretamente no track.
- Aplique espaçamento no slide individual, não no container flex.
- Se quiser loop estável, prefira `basis-full` ou `flex-[0_0_100%]`.

### Checklist

- `loop: true`
- `slidesToScroll: 1`
- track com `flex`, sem `gap-*`
- slide com `min-w-0`
- slide com largura de 100% quando o objetivo é estabilidade máxima

### Exemplo completo

```tsx
"use client";

import useEmblaCarousel from "embla-carousel-react";
import { useCallback, useEffect, useState } from "react";

export function CarouselComponent({ items }) {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    loop: true,
    slidesToScroll: 1,
  });

  const [selectedIndex, setSelectedIndex] = useState(0);

  const scrollTo = useCallback(
    (index: number) => emblaApi && emblaApi.scrollTo(index),
    [emblaApi]
  );

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setSelectedIndex(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on("select", onSelect);
  }, [emblaApi, onSelect]);

  return (
    <div>
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {items.map((item, index) => (
            <div key={index} className="flex-[0_0_100%] min-w-0 px-2">
              <div className="rounded-2xl border bg-card p-6">{item.content}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 flex justify-center gap-2">
        {items.map((_, index) => (
          <button
            key={index}
            onClick={() => scrollTo(index)}
            className={
              index === selectedIndex
                ? "h-2 w-6 rounded-full bg-primary"
                : "h-2 w-2 rounded-full bg-muted-foreground/30"
            }
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
```

## 2. Full-Bleed / Margem Imersiva

### Problema

O carousel funciona, mas continua com uma margem lateral constante. O slide nunca parece tocar a borda da viewport, então o efeito de "entrar e sair da tela" não acontece.

### Causa

O problema quase sempre está fora do Embla: algum wrapper externo aplica padding horizontal, por exemplo em:

- `main`
- `section`
- `container`
- wrappers de `max-width`
- layouts globais

Exemplo:

```tsx
<main className="px-4">
  <section className="mx-auto max-w-6xl">
    <CarouselSection />
  </section>
</main>
```

Nesse caso, mesmo que o Embla esteja correto, o `px-4` do layout impede o bleed visual.

### Estratégia

Separe duas responsabilidades:

1. conteúdo textual e estrutural continua contido
2. a trilha do carousel pode escapar horizontalmente no breakpoint desejado

Na prática:

- mantenha títulos e descrição dentro do container
- deixe apenas a trilha dos slides compensar o padding externo
- normalmente aplique isso só no mobile

### Padrão recomendado

#### 1. Compense o padding externo

Se o layout pai usa `px-4`, use `-mx-4` no mesmo breakpoint:

```tsx
<section className="-mx-4 sm:mx-auto sm:max-w-6xl">
  <CarouselSection />
</section>
```

Se o padding herdado for outro, a compensação deve usar o mesmo valor.

#### 2. Use `overflow-hidden`

Evite scroll horizontal da página:

```tsx
<div className="overflow-hidden">
  <div ref={emblaRef}>...</div>
</div>
```

#### 3. Não use `gap-*` no track

Se precisar de espaçamento:

- remova `gap-*` do container flex
- use `pl-*` ou `px-*` nos slides
- use margem negativa no track para compensar

Exemplo:

```tsx
<div className="-ml-5 flex">
  {items.map((item, index) => (
    <div key={index} className="min-w-0 flex-[0_0_86%] pl-5">
      <Card />
    </div>
  ))}
</div>
```

#### 4. Use largura parcial quando quiser antecipação visual

Para mostrar um pedaço do próximo slide:

- `flex-[0_0_86%]`
- `flex-[0_0_90%]`
- `basis-[86%]`

Para mostrar um slide por vez:

- `flex-[0_0_100%]`
- `basis-full`

### Regras práticas

- Compense padding externo com margem negativa equivalente.
- A compensação deve acontecer no mesmo breakpoint do bleed.
- Preserve o padding interno do card; ele controla leitura, não o bleed.
- Se o bleed for só mobile, restaure o layout contido em `sm`, `md` ou `lg`.
- Se estiver usando um wrapper utilitário de carousel, revise o espaçamento padrão antes de adicionar novas classes.

### Quando a margem esquerda não abre

Se o carousel continua com respiro visual na esquerda, o problema quase sempre está em uma destas camadas:

- o `padding-left` externo não foi compensado
- o `-mx-*` foi aplicado no nível errado
- o track não tem margem negativa
- o slide usa `px-*` em vez de `pl-*`
- existe um wrapper intermediário com `container`, `max-w-*` ou `padding-left`

Checklist de diagnóstico:

1. identifique qual ancestral aplica o `px-*`
2. compense esse mesmo nível com `-mx-*`
3. garanta `overflow-hidden` no wrapper correto
4. use track com `-ml-*`
5. use slide com `pl-*`
6. remova `gap-*` do track

Padrão confiável:

```tsx
<div className="overflow-hidden">
  <div className="-ml-5 flex">
    {items.map((item, index) => (
      <div key={index} className="min-w-0 flex-[0_0_86%] pl-5">
        <Card />
      </div>
    ))}
  </div>
</div>
```

Padrão que costuma falhar:

```tsx
<div className="overflow-hidden">
  <div className="flex gap-4">
    {items.map((item, index) => (
      <div key={index} className="basis-[86%] px-4">
        <Card />
      </div>
    ))}
  </div>
</div>
```

Motivo: `gap-*` no track e `px-*` bilateral no slide costumam reintroduzir margem visual na borda inicial.

### Exemplo genérico

```tsx
<section className="overflow-hidden py-12">
  <div className="mx-auto max-w-6xl px-4 sm:px-6">
    <SectionHeader />
  </div>

  <div className="px-4 sm:px-0">
    <div className="-mx-4 sm:mx-auto sm:max-w-6xl sm:px-6">
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="-ml-5 flex sm:-ml-6">
          {items.map((item, index) => (
            <div
              key={index}
              className="min-w-0 flex-[0_0_86%] pl-5 sm:flex-[0_0_50%] sm:pl-6 lg:flex-[0_0_33.333%]"
            >
              <Card />
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</section>
```

### Quando aplicar

Use esse padrão quando:

- o slider precisa parecer mais imersivo
- você quer mostrar parte do próximo slide
- o layout contido está apertando visualmente o carousel
- o texto deve seguir o grid, mas os slides podem escapar dele

Evite quando:

- a seção inteira precisa manter margens constantes
- o conteúdo do slider depende de alinhamento rígido com outros blocos
- o design exige rigor absoluto de container em todos os componentes

### Wrappers utilitários

Wrappers prontos, como alguns carousels do shadcn/ui, já podem aplicar:

- margem negativa no track
- padding lateral no item

Antes de adicionar mais classes:

- verifique o track
- verifique o slide
- ajuste `basis-*`, `pl-*` e wrappers externos antes de introduzir `gap-*`

## Referências

- [Embla Carousel Docs](https://www.embla-carousel.com/)
- [Loop Option](https://www.embla-carousel.com/api/options/#loop)
