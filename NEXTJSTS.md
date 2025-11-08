# Next.js + TypeScript - Configurações Iniciais Padrão

Este documento contém as configurações iniciais recomendadas para projetos Next.js com TypeScript, incluindo otimizações, dicas e melhores práticas.

## Sumário

1. [Estrutura de Arquivos](#1-estrutura-de-arquivos-recomendada)
2. [Configurações de Arquivos](#2-configurações-de-arquivos)
   - [next.config.js](#nextconfigjs)
   - [tsconfig.json](#tsconfigjson)
   - [package.json](#packagejson)
   - [.eslintrc.json](#eslintrcjson)
   - [.gitignore](#gitignore)
   - [.prettierrc](#prettierrc)
3. [Melhores Práticas](#3-melhores-práticas)
   - [Otimizações de Desempenho](#otimizações-de-desempenho)
   - [Tipagem TypeScript](#tipagem-typescript)
   - [Estrutura de Componentes](#estrutura-de-componentes)
   - [Segurança](#segurança)
   - [Padrões de Código](#padrões-de-código)
4. [Scripts e Comandos Úteis](#4-scripts-e-comandos-úteis)
5. [Configurações Adicionais](#5-configurações-adicionais)
   - [Husky e lint-staged](#husky-e-lint-staged)
   - [Testes com Jest](#testes-com-jest)

## 1. Estrutura de Arquivos Recomendada

```
project/
├── public/
├── app/                 # App Router (ou pages/ para Pages Router)
├── components/
├── lib/
├── styles/
├── types/
├── hooks/
├── services/
├── .env.example
├── .gitignore
├── next.config.js
├── tsconfig.json
├── package.json
├── postcss.config.js   # Se usando Tailwind CSS
└── README.md
```

## 2. Configurações de Arquivos

### next.config.js

Configurações recomendadas para otimização e segurança:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Otimizações de produção
  compiler: {
    removeConsole: true, // Remove console.log em produção
  },

  // Segurança
  reactStrictMode: true,
  swcMinify: true,

  // Imagens
  images: {
    unoptimized: true, // Aceita imagens de qualquer domínio
    formats: [
      "image/webp",
      "image/avif",
      "image/jpeg",
      "image/png",
      "image/gif",
      "image/svg+xml",
    ],
    // Permite carregar imagens de qualquer domínio externo
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**', // Wildcard para todos os hostnames
        port: '',
        pathname: '**', // Wildcard para todos os paths
      },
      {
        protocol: 'http',
        hostname: '**',
        port: '',
        pathname: '**',
      },
    ],
  },

  // Headers de segurança
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
        ],
      },
    ];
  },

  // Redirecionamentos (opcional)
  async redirects() {
    return [
      // Exemplo: redirecionar de /old para /new
      // {
      //   source: '/old-path',
      //   destination: '/new-path',
      //   permanent: true,
      // },
    ];
  },
};

module.exports = nextConfig;
```

### tsconfig.json

Configurações TypeScript recomendadas com verificações estritas:

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["*"]
    },
    "removeComments": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "alwaysStrict": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### package.json

Scripts e dependências recomendadas:

```json
{
  "name": "seu-projeto-nextjs",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "format": "prettier --write .",
    "check-format": "prettier --check .",
    "prepare": "husky install"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "14.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "prettier": "^3.0.0"
  }
}
```

### .eslintrc.json

Configurações ESLint recomendadas:

```json
{
  "extends": [
    "next/core-web-vitals",
    "@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "@next/next/no-img-element": "off"
  }
}
```

### .gitignore

Configurações recomendadas para .gitignore:

```
# Dependencies
node_modules/

# Environment variables
.env.local
.env.production
.env.test

# Next.js
.next/
out/

# TypeScript
*.tsbuildinfo
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

## 3. Melhores Práticas

### Otimizações de Desempenho

1. **Remover console.log em produção**: A configuração `removeConsole: true` remove todos os `console.log` em builds de produção, reduzindo o tamanho do bundle.

2. **Otimizar imagens**: Use o componente `next/image` para otimização automática de imagens.
   - **Imagens de domínios externos**: A configuração `remotePatterns` com wildcards (`**`) permite carregar imagens de qualquer domínio externo. Em produção, considere restringir a domínios específicos por segurança:
     ```javascript
     remotePatterns: [
       {
         protocol: 'https',
         hostname: 'exemplo.com',
         port: '',
         pathname: '/images/**',
       },
     ]
     ```

3. **Code splitting**: Next.js faz code splitting automaticamente, mas você pode otimizar ainda mais com `next/dynamic` para importação condicional.

### Tipagem TypeScript

1. **Tipos personalizados**: Crie um diretório `types/` para armazenar interfaces e tipos personalizados.

2. **Validação de props**: Sempre tipar as props dos componentes para evitar erros em tempo de execução.

3. **Tipos de API**: Use tipos para estruturar as respostas de API e garantir consistência.

### Estrutura de Componentes

1. **Componentes reutilizáveis**: Organize componentes em subpastas dentro de `components/` (ex: `components/ui/`, `components/forms/`).

2. **Hooks personalizados**: Crie hooks em `hooks/` para lógica reutilizável.

3. **Serviços**: Coloque lógica de API em `services/` para manter componentes limpos.

### Segurança

1. **Headers de segurança**: Use o método `headers()` no `next.config.js` para adicionar headers de segurança.

2. **Validação de entrada**: Sempre valide dados de entrada, especialmente em API routes.

3. **Environment variables**: Use `.env` para armazenar credenciais e variáveis sensíveis.

### Padrões de Código

1. **Nomenclatura**: Use camelCase para variáveis e funções, PascalCase para componentes.

2. **Componentes pequenos**: Prefira componentes pequenos e focados em uma única responsabilidade.

3. **Documentação**: Comente código complexo e documente componentes importantes.

## 4. Scripts e Comandos Úteis

- `pnpm dev`: Inicia o servidor de desenvolvimento
- `pnpm build`: Cria uma build de produção
- `pnpm start`: Inicia o servidor de produção
- `pnpm lint`: Executa o linter
- `pnpm type-check`: Verifica tipagem TypeScript
- `pnpm format`: Formata o código com Prettier
- `pnpm check-format`: Verifica formatação sem modificar arquivos

## 5. Configurações Adicionais

### .prettierrc

Crie `.prettierrc`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

### Husky e lint-staged

Para garantir que o código esteja formatado e verificado antes de cada commit:

```bash
pnpm add -D husky lint-staged
```

Adicione ao `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]
  },
  "scripts": {
    "prepare": "husky install"
  }
}
```

### Testes com Jest

Adicione Jest e React Testing Library:

```bash
pnpm add -D jest @testing-library/react @testing-library/jest-dom jsdom
```

---

## Conclusão

Essas configurações iniciais fornecem uma base sólida para projetos Next.js com TypeScript, com foco em performance, segurança e manutenibilidade. Personalize conforme as necessidades específicas do seu projeto.
