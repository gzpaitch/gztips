# generate-icons.js

This script generates SVG icons for Progressive Web App (PWA) requirements. It creates a set of icons in various sizes needed for different platforms and devices, with a consistent design featuring "CNEWS" and "ADMIN" text.

## What it does

- Creates SVG icons in multiple sizes required for PWA manifest
- Generates icons with a dark gradient background and news-themed design
- Places icons in the `public/icons` directory
- Creates a favicon.ico file

## Icon sizes generated

- 16x16 - favicon-16x16.svg
- 32x32 - favicon-32x32.svg
- 72x72 - icon-72x72.svg
- 96x96 - icon-96x96.svg
- 128x128 - icon-128x128.svg
- 144x144 - icon-144x144.svg
- 152x152 - icon-152x152.svg
- 180x180 - apple-touch-icon.svg
- 192x192 - icon-192x192.svg
- 384x384 - icon-384x384.svg
- 512x512 - icon-512x512.svg

## How to use

1. Place this script in your project's scripts directory
2. Run the script with Node.js: `node generate-icons.js`
3. The script will create all necessary SVG icons in the `public/icons` directory

## Important notes

- This script generates SVG icons, but for production you may need to convert them to PNG format
- The icons feature a dark gradient background with white news-themed elements and "CNEWS" and "ADMIN" text
- The design scales appropriately for different icon sizes
- The script automatically creates the output directory if it doesn't exist

## Dependencies

- Node.js with `fs` and `path` modules (standard with Node.js)

```js
const fs = require("fs");
const path = require("path");

// Icon sizes needed for PWA
const iconSizes = [
  { size: 16, name: "favicon-16x16.png" },
  { size: 32, name: "favicon-32x32.png" },
  { size: 72, name: "icon-72x72.png" },
  { size: 96, name: "icon-96x96.png" },
  { size: 128, name: "icon-128x128.png" },
  { size: 144, name: "icon-144x144.png" },
  { size: 152, name: "icon-152x152.png" },
  { size: 180, name: "apple-touch-icon.png" },
  { size: 192, name: "icon-192x192.png" },
  { size: 384, name: "icon-384x384.png" },
  { size: 512, name: "icon-512x512.png" },
];

// Create a simple SVG icon for each size
function generateSVGIcon(size) {
  const fontSize = Math.max(size * 0.08, 8);
  const adminFontSize = Math.max(size * 0.04, 6);
  const strokeWidth = Math.max(size * 0.006, 1);

  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1f2937;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#374151;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="${size}" height="${size}" rx="${
    size * 0.125
  }" fill="url(#bgGradient)"/>

  <!-- News icon -->
  <rect x="${size * 0.25}" y="${size * 0.25}" width="${size * 0.5}" height="${
    size * 0.35
  }" rx="${size * 0.02}" fill="#ffffff"/>
  <rect x="${size * 0.3}" y="${size * 0.32}" width="${size * 0.4}" height="${
    size * 0.02
  }" rx="${size * 0.01}" fill="#1f2937"/>
  <rect x="${size * 0.3}" y="${size * 0.38}" width="${size * 0.3}" height="${
    size * 0.02
  }" rx="${size * 0.01}" fill="#1f2937"/>
  <rect x="${size * 0.3}" y="${size * 0.44}" width="${size * 0.35}" height="${
    size * 0.02
  }" rx="${size * 0.01}" fill="#1f2937"/>
  <rect x="${size * 0.3}" y="${size * 0.5}" width="${size * 0.25}" height="${
    size * 0.02
  }" rx="${size * 0.01}" fill="#1f2937"/>

  <!-- CNEWS Text -->
  <text x="${size * 0.5}" y="${
    size * 0.75
  }" font-family="Arial, sans-serif" font-size="${fontSize}" font-weight="bold" text-anchor="middle" fill="#60a5fa">CNEWS</text>
  <text x="${size * 0.5}" y="${
    size * 0.85
  }" font-family="Arial, sans-serif" font-size="${adminFontSize}" text-anchor="middle" fill="#9ca3af">ADMIN</text>
</svg>`;
}

// Ensure directories exist
const iconsDir = path.join(__dirname, "..", "public", "icons");
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

// Generate SVG icons for each size
iconSizes.forEach(({ size, name }) => {
  const svgContent = generateSVGIcon(size);
  const svgPath = path.join(iconsDir, name.replace(".png", ".svg"));

  fs.writeFileSync(svgPath, svgContent);
  console.log(`Generated ${svgPath}`);
});

// Create a simple favicon.ico placeholder
const faviconContent = generateSVGIcon(32);
fs.writeFileSync(
  path.join(__dirname, "..", "public", "favicon.ico"),
  faviconContent
);

console.log("Icon generation completed!");
console.log(
  "Note: For production, convert SVG icons to PNG format using a proper image conversion tool."
);
```
