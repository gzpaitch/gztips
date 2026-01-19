# Deploy de Aplicações Vite/React no Easypanel

Guia para configurar e fazer deploy de aplicações React com Vite em VPS usando Easypanel.

## Pré-requisitos

- Aplicação React + Vite funcionando localmente
- Repositório Git configurado
- Easypanel instalado na VPS

## Configuração do Projeto

### 1. vite.config.ts

Adicione `base: './'` para gerar paths relativos nos assets:

```ts
export default defineConfig({
  base: "./",
  // ... outras configurações
});
```

### 2. index.html

Use path relativo no script:

```html
<script type="module" src="./index.tsx"></script>
```

### 3. Dockerfile

Crie na raiz do projeto:

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 80
CMD ["serve", "dist", "-s", "-l", "80"]
```

> **Nota:** Ajuste o comando de instalação conforme seu package manager:
>
> - npm: `COPY package*.json ./` + `RUN npm install`
> - yarn: `COPY package.json yarn.lock ./` + `RUN yarn install`
> - pnpm: `COPY package*.json pnpm-lock.yaml ./` + `RUN npm install -g pnpm && pnpm install`

### 4. .dockerignore (opcional)

```
node_modules
dist
.git
*.md
```

## Deploy no Easypanel

1. Crie um novo serviço do tipo **App**
2. Conecte ao repositório Git
3. Em **Build**, selecione **Dockerfile**
4. Configure a porta como **80**
5. Faça o deploy

## Troubleshooting

### Erro de MIME type

Se aparecer erro `Failed to load module script... MIME type ""`:

- Verifique se está servindo a pasta `dist`, não a raiz
- Confirme que `base: './'` está no vite.config.ts
- Rebuild a aplicação após alterar o config

### Tela branca

- Verifique o console do navegador para erros
- Confirme que o build foi executado (`pnpm build`)
- Verifique se os arquivos estão em `/app/dist` no container

### Build falha no Easypanel

- Evite usar Nixpacks para apps Vite, prefira Dockerfile
- Verifique se o lockfile está commitado (pnpm-lock.yaml, package-lock.json)
