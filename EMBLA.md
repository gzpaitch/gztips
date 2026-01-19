# EMBLA

# Embla Carousel - Correção de Loop

## Problema

Quando usando `loop: true` no Embla Carousel com slides que não ocupam 100% da largura (ex: 85%, 90%), o último slide aparece junto com o primeiro slide, criando um efeito visual indesejado.

## Causa

O Embla Carousel cria clones dos slides para fazer o loop funcionar. Quando você usa:

- `align: 'start'`
- Slides com largura menor que 100% (ex: `flex-[0_0_90%]`)
- `gap` entre os slides no container flex

O carousel mostra múltiplos slides ao mesmo tempo, e os clones ficam visíveis causando o problema.

## Solução

### ❌ Configuração Incorreta

```tsx
const [emblaRef, emblaApi] = useEmblaCarousel({
  align: "start",
  loop: true,
  containScroll: "trimSnaps", // Não resolve o problema
});

// Container com gap
<div className="flex gap-4">
  {items.map((item, index) => (
    <div key={index} className="flex-[0_0_90%] min-w-0">
      {/* Conteúdo */}
    </div>
  ))}
</div>;
```

### ✅ Configuração Correta

```tsx
const [emblaRef, emblaApi] = useEmblaCarousel({
  loop: true,
  slidesToScroll: 1, // Garante scroll de um slide por vez
  // Não use: align, containScroll, dragFree
});

// Container sem gap, padding nos slides individuais
<div className="flex">
  {items.map((item, index) => (
    <div key={index} className="flex-[0_0_100%] min-w-0 px-2">
      {/* Conteúdo */}
    </div>
  ))}
</div>;
```

## Checklist de Implementação

1. **Configuração do Embla:**

   - ✅ `loop: true`
   - ✅ `slidesToScroll: 1`
   - ❌ Remover `align: 'start'`
   - ❌ Remover `containScroll`
   - ❌ Remover `dragFree`

2. **Container dos Slides:**

   - ✅ `className="flex"` (sem gap)
   - ❌ Remover `gap-4`, `gap-6`, etc.

3. **Slides Individuais:**
   - ✅ `className="flex-[0_0_100%] min-w-0 px-2"`
   - ✅ Largura de 100% (`flex-[0_0_100%]`)
   - ✅ Padding horizontal para espaçamento (`px-2`, `px-3`, `px-4`)
   - ❌ Não usar `flex-[0_0_90%]` ou outras porcentagens

## Exemplo Completo

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
      {/* Carousel Container */}
      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {items.map((item, index) => (
            <div key={index} className="flex-[0_0_100%] min-w-0 px-2">
              {/* Seu conteúdo aqui */}
              <div className="bg-card border rounded-2xl p-6">
                {item.content}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dots de Navegação */}
      <div className="flex justify-center gap-2 mt-6">
        {items.map((_, index) => (
          <button
            key={index}
            onClick={() => scrollTo(index)}
            className={
              index === selectedIndex
                ? "w-6 h-2 rounded-full bg-primary"
                : "w-2 h-2 rounded-full bg-muted-foreground/30"
            }
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
```

## Ajustes de Espaçamento

Se precisar ajustar o espaçamento entre os slides:

- **Menos espaço:** `px-1` ou `px-0.5`
- **Espaço padrão:** `px-2`
- **Mais espaço:** `px-3` ou `px-4`

## Quando Usar Loop

- ✅ Use `loop: true` quando tiver 3+ slides
- ❌ Evite loop com apenas 2 slides (pode causar comportamento estranho)
- ✅ Combine com dots de navegação para melhor UX

## Referências

- [Embla Carousel Docs](https://www.embla-carousel.com/)
- [Loop Option](https://www.embla-carousel.com/api/options/#loop)
- Implementação: `app/components/landing/why-ppty/why-ppty-section.tsx`
