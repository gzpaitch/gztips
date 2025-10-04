# GLM

## Prompt para Remoção de Servidor Customizado e Prisma de Projetos Next.js

**Objetivo:** Converter um projeto Next.js que usa servidor customizado e Prisma para um projeto Next.js padrão sem dependências de servidor ou banco de dados.

**Instruções:**

1. **Análise Inicial:**

   - Identifique todos os arquivos relacionados ao servidor customizado (ex: `server.ts`, `socket.ts`)
   - Localize todos os arquivos e diretórios do Prisma (`prisma/`, `db.ts`, arquivos `.db`)
   - Verifique dependências no `package.json` relacionadas a servidor e banco de dados

2. **Remoção de Arquivos do Servidor:**

   - Remova o arquivo principal do servidor (geralmente `server.ts` na raiz)
   - Remova arquivos de configuração de Socket.IO (`socket.ts`, `socketio.ts`)
   - Remova exemplos ou páginas que dependem do WebSocket/Socket.IO

3. **Remoção de Arquivos do Prisma:**

   - Delete o diretório `prisma/` completo
   - Remova arquivos de configuração do banco (`db.ts`, `database.ts`)
   - Delete arquivos de banco de dados locais (`.db`, `.sqlite`)

4. **Atualização do package.json:**

   - **Scripts a remover/substituir:**

     - `"dev": "nodemon server.ts"` → `"dev": "next dev"`
     - `"start": "tsx server.ts"` → `"start": "next start"`
     - Remover todos os scripts `db:*` (push, migrate, studio, etc.)

   - **Dependências a remover:**
     - `@prisma/client`
     - `prisma`
     - `socket.io`
     - `socket.io-client`
     - `tsx` (se usado apenas para servidor)
     - `nodemon` (se usado apenas para servidor)

5. **Limpeza de Referências:**

   - Busque e remova imports de arquivos deletados
   - Remova referências a Socket.IO client
   - Delete páginas/componentes que dependem de WebSocket
   - Remova variáveis de ambiente relacionadas ao banco (`DATABASE_URL`)

6. **Limpeza de Diretórios:**

   - Remova diretórios vazios (`db/`, `prisma/`, `examples/websocket/`)
   - Use comandos como `Remove-Item -Path "db", "prisma", "examples" -Recurse -Force`

7. **Correção do Hot Reload (next.config.ts):**

   - **Problema:** Após remover o servidor customizado, o hot reload pode não funcionar
   - **Causa:** Configurações no `next.config.ts` que desabilitam o hot reload para integração com nodemon
   - **Solução:**
     - Remova configurações `webpack` que ignoram mudanças de arquivo:
       ```typescript
       webpack: (config) => {
         config.watchOptions = {
           ignored: ["**/*"], // ← REMOVER ESTA LINHA
         };
         return config;
       };
       ```
     - Altere `reactStrictMode: false` para `reactStrictMode: true`
     - Remova comentários sobre desabilitar hot reload
   - **Teste:** Faça uma mudança em qualquer arquivo e verifique se recompila automaticamente

8. **Teste e Validação:**
   - Limpe `node_modules` e reinstale dependências: `pnpm install`
   - Teste o build: `pnpm build`
   - Teste o servidor de desenvolvimento: `pnpm dev`
   - Verifique se a aplicação carrega corretamente no navegador
   - **Teste o hot reload:** Faça uma mudança no código e confirme que recompila automaticamente

**Resultado Esperado:**

- Projeto Next.js padrão funcionando sem servidor customizado
- Sem dependências de banco de dados ou Prisma
- Scripts padrão do Next.js no package.json
- Aplicação funcionando corretamente em modo de desenvolvimento e produção
- **Hot reload funcionando corretamente** (mudanças no código refletidas automaticamente)

**Comandos Essenciais:**

```bash
# Limpeza
Remove-Item -Path "node_modules", "package-lock.json" -Recurse -Force
Remove-Item -Path "db", "prisma", "examples" -Recurse -Force

# Reinstalação e teste
pnpm install
pnpm build
pnpm dev
```

---
