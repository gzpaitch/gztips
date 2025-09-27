# Next.js + TypeScript - Configurações Iniciais Padrão

Este documento contém as configurações iniciais recomendadas para projetos Next.js com TypeScript, incluindo otimizações, dicas e melhores práticas.

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

## 2. next.config.js

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

## 3. tsconfig.json

Configurações TypeScript recomendadas:

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
    "removeComments": true, // Remove comentários no código compilado
    "noUnusedLocals": true, // Sinaliza variáveis locais não utilizadas
    "noUnusedParameters": true, // Sinaliza parâmetros não utilizados
    "strictNullChecks": true, // Verificações estritas de null/undefined
    "strictFunctionTypes": true, // Verificações estritas de tipos de função
    "strictBindCallApply": true, // Verificações estritas para bind/call/apply
    "noImplicitAny": true, // Não permite 'any' implícito
    "noImplicitReturns": true, // Verifica se todas as ramificações retornam valor
    "alwaysStrict": true, // Adiciona 'use strict' em todos os arquivos
    "exactOptionalPropertyTypes": true, // Tipos exatos para propriedades opcionais
    "noFallthroughCasesInSwitch": true, // Verifica switch/case incompletos
    "noUncheckedIndexedAccess": true, // Acesso a índices é verificado
    "noImplicitOverride": true, // Requer 'override' para métodos sobrescritos
    "verbatimModuleSyntax": true // Preserva import/export no JS emitido
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## 4. package.json

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
    "check-format": "prettier --check ."
  },
  "dependencies": {
    "next": "^14.0.0", // Atualize para a versão mais recente
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

## 5. .eslintrc.json

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

## 6. .gitignore

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

## 7. Dicas e Melhores Práticas

### Otimizações de Desempenho

1. **Remover console.log em produção**: A configuração `removeConsole: true` remove todos os `console.log` em builds de produção, reduzindo o tamanho do bundle.

2. **Otimizar imagens**: Use o componente `next/image` para otimização automática de imagens.

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

### Boas Práticas de Código

1. **Padrão de nomenclatura**: Use camelCase para variáveis e funções, PascalCase para componentes.

2. **Componentes pequenos**: Prefira componentes pequenos e focados em uma única responsabilidade.

3. **Documentação**: Comente código complexo e documente componentes importantes.

### Scripts úteis

- `npm run dev`: Inicia o servidor de desenvolvimento
- `npm run build`: Cria uma build de produção
- `npm run start`: Inicia o servidor de produção
- `npm run lint`: Executa o linter
- `npm run type-check`: Verifica tipagem TypeScript
- `npm run format`: Formata o código com Prettier

## 8. Configurações Adicionais Opcionais

### Prettier (formatação de código)

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

### Husky e lint-staged (pré-commit hooks)

Para garantir que o código esteja formatado e verificado antes de cada commit:

```bash
npm install --save-dev husky lint-staged
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

### Testes (opcional)

Adicione Jest e React Testing Library:

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom jsdom
```

## Conclusão

Essas configurações iniciais fornecem uma base sólida para projetos Next.js com TypeScript, com foco em performance, segurança e manutenibilidade. Personalize conforme as necessidades específicas do seu projeto.
