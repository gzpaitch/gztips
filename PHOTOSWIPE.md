# PHOTOSWIPE

## PhotoSwipe Setup Guide

## Overview

This guide covers the installation and configuration of PhotoSwipe (v5) in a Next.js project using `react-photoswipe-gallery` for proper React integration.

## Installation

```bash
pnpm install photoswipe react-photoswipe-gallery
```

## Why react-photoswipe-gallery?

- **React-friendly API**: Provides components and hooks instead of imperative API
- **Next.js optimized**: Supports dynamic imports (loads JS only when needed)
- **PhotoSwipe v5 compatible**: Full access to latest features and plugins
- **Better DX**: Cleaner code with render props pattern

## Basic Implementation

### 1. Import Dependencies

```tsx
import { Gallery, Item } from "react-photoswipe-gallery";
import "photoswipe/dist/photoswipe.css";
```

### 2. Wrap Content with Gallery

```tsx
<Gallery>{/* Your image items here */}</Gallery>
```

### 3. Create Image Items

```tsx
<Item
  original={imageUrl}
  thumbnail={thumbnailUrl}
  width={1920}
  height={1080}
  alt="Image description"
>
  {({ ref, open }) => (
    <button ref={ref} onClick={open}>
      <img src={thumbnailUrl} alt="Image description" />
    </button>
  )}
</Item>
```

## Critical Issue: Image Aspect Ratio

### The Problem

PhotoSwipe requires explicit `width` and `height` props to calculate correct aspect ratios. Without real dimensions, images will be stretched or deformed in the lightbox.

### The Solution

Load actual image dimensions before passing them to PhotoSwipe:

#### Step 1: Create Image Dimensions Interface

```tsx
interface ImageDimensions {
  width: number;
  height: number;
}
```

#### Step 2: Add State to Store Dimensions

```tsx
const [imageDimensions, setImageDimensions] = useState<
  Record<string, ImageDimensions>
>({});
```

#### Step 3: Create Dimension Loader Function

```tsx
const loadImageDimensions = useCallback(
  (url: string): Promise<ImageDimensions> => {
    return new Promise((resolve, reject) => {
      const img = new window.Image();
      img.onload = () => {
        resolve({ width: img.naturalWidth, height: img.naturalHeight });
      };
      img.onerror = reject;
      img.src = url;
    });
  },
  [],
);
```

#### Step 4: Load Dimensions on File List Change

```tsx
useEffect(() => {
  const loadAllDimensions = async () => {
    const dimensions: Record<string, ImageDimensions> = {};

    for (const file of files) {
      if (isImage(file.name)) {
        try {
          const dims = await loadImageDimensions(file.url);
          dimensions[file.path] = dims;
        } catch (error) {
          console.error(`Failed to load dimensions for ${file.name}:`, error);
        }
      }
    }

    setImageDimensions(dimensions);
  };

  if (files.length > 0) {
    loadAllDimensions();
  }
}, [files, loadImageDimensions]);
```

#### Step 5: Use Real Dimensions in Item Component

```tsx
{
  files.map((file) => {
    const dimensions = imageDimensions[file.path];
    return (
      <Item
        key={file.path}
        original={file.url}
        thumbnail={file.url}
        width={dimensions?.width}
        height={dimensions?.height}
        alt={file.name}
      >
        {({ ref, open }) => (
          <button ref={ref} onClick={open}>
            <img src={file.url} alt={file.name} />
          </button>
        )}
      </Item>
    );
  });
}
```

## Key Points

1. **Never use fixed dimensions** (e.g., `width="1920"` for all images) - this causes distortion
2. **Always load actual dimensions** using `naturalWidth` and `naturalHeight`
3. **Handle loading state** - dimensions may not be available immediately
4. **Use optional chaining** (`dimensions?.width`) to prevent errors during loading

## Performance Considerations

- Images are loaded in the background to extract dimensions
- This happens asynchronously and doesn't block rendering
- Dimensions are cached in state to avoid re-loading
- PhotoSwipe only loads when user clicks (lazy loading)

## Complete Example

```tsx
"use client";

import { useState, useEffect, useCallback } from "react";
import { Gallery, Item } from "react-photoswipe-gallery";
import "photoswipe/dist/photoswipe.css";

interface ImageDimensions {
  width: number;
  height: number;
}

interface ImageFile {
  id: string;
  url: string;
  name: string;
}

export function ImageGallery({ images }: { images: ImageFile[] }) {
  const [imageDimensions, setImageDimensions] = useState<
    Record<string, ImageDimensions>
  >({});

  const loadImageDimensions = useCallback(
    (url: string): Promise<ImageDimensions> => {
      return new Promise((resolve, reject) => {
        const img = new window.Image();
        img.onload = () => {
          resolve({ width: img.naturalWidth, height: img.naturalHeight });
        };
        img.onerror = reject;
        img.src = url;
      });
    },
    [],
  );

  useEffect(() => {
    const loadAllDimensions = async () => {
      const dimensions: Record<string, ImageDimensions> = {};

      for (const image of images) {
        try {
          const dims = await loadImageDimensions(image.url);
          dimensions[image.id] = dims;
        } catch (error) {
          console.error(`Failed to load dimensions for ${image.name}:`, error);
        }
      }

      setImageDimensions(dimensions);
    };

    if (images.length > 0) {
      loadAllDimensions();
    }
  }, [images, loadImageDimensions]);

  return (
    <Gallery>
      <div className="grid grid-cols-3 gap-4">
        {images.map((image) => {
          const dimensions = imageDimensions[image.id];
          return (
            <Item
              key={image.id}
              original={image.url}
              thumbnail={image.url}
              width={dimensions?.width}
              height={dimensions?.height}
              alt={image.name}
            >
              {({ ref, open }) => (
                <button ref={ref} onClick={open} className="cursor-pointer">
                  <img
                    src={image.url}
                    alt={image.name}
                    className="w-full h-full object-cover"
                  />
                </button>
              )}
            </Item>
          );
        })}
      </div>
    </Gallery>
  );
}
```

## References

- [PhotoSwipe Official Docs](https://photoswipe.com/)
- [react-photoswipe-gallery NPM](https://www.npmjs.com/package/react-photoswipe-gallery)
- [GitHub Repository](https://github.com/dromru/react-photoswipe-gallery)
