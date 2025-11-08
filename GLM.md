# GLM

## Table of Contents

- [Overview](#overview)
- [Initial Analysis](#initial-analysis)
- [Server Files Removal](#server-files-removal)
- [Prisma Files Removal](#prisma-files-removal)
- [Package.json Update](#packagejson-update)
- [References Cleanup](#references-cleanup)
- [Directory Cleanup](#directory-cleanup)
- [Hot Reload Fix](#hot-reload-fix)
- [Testing and Validation](#testing-and-validation)
- [Expected Result](#expected-result)
- [Essential Commands](#essential-commands)

## Overview

**Objective:** Convert a Next.js project using a custom server and Prisma to a standard Next.js project without server or database dependencies.

## Initial Analysis

- Identify all custom server-related files (e.g., `server.ts`, `socket.ts`)
- Locate all Prisma files and directories (`prisma/`, `db.ts`, `.db` files)
- Check `package.json` dependencies related to server and database

## Server Files Removal

- Remove main server file (usually `server.ts` in root)
- Remove Socket.IO configuration files (`socket.ts`, `socketio.ts`)
- Remove examples or pages that depend on WebSocket/Socket.IO

## Prisma Files Removal

- Delete the complete `prisma/` directory
- Remove database configuration files (`db.ts`, `database.ts`)
- Delete local database files (`.db`, `.sqlite`)

## Package.json Update

**Scripts to remove/replace:**

- `"dev": "nodemon server.ts"` → `"dev": "next dev"`
- `"start": "tsx server.ts"` → `"start": "next start"`
- Remove all `db:*` scripts (push, migrate, studio, etc.)

**Dependencies to remove:**

- `@prisma/client`
- `prisma`
- `socket.io`
- `socket.io-client`
- `tsx` (if used only for server)
- `nodemon` (if used only for server)

## References Cleanup

- Search and remove imports from deleted files
- Remove Socket.IO client references
- Delete pages/components that depend on WebSocket
- Remove database-related environment variables (`DATABASE_URL`)

## Directory Cleanup

- Remove empty directories (`db/`, `prisma/`, `examples/websocket/`)
- Use commands like `Remove-Item -Path "db", "prisma", "examples" -Recurse -Force`

## Hot Reload Fix

**Problem:** After removing the custom server, hot reload may not work

**Cause:** Settings in `next.config.ts` that disable hot reload for nodemon integration

**Solution:**

- Remove `webpack` configurations that ignore file changes:
  ```typescript
  webpack: (config) => {
    config.watchOptions = {
      ignored: ["**/*"], // ← REMOVE THIS LINE
    };
    return config;
  };
  ```
- Change `reactStrictMode: false` to `reactStrictMode: true`
- Remove comments about disabling hot reload

**Test:** Make a change to any file and verify it recompiles automatically

## Testing and Validation

- Clean `node_modules` and reinstall dependencies: `pnpm install`
- Test the build: `pnpm build`
- Test the development server: `pnpm dev`
- Verify the application loads correctly in the browser
- **Test hot reload:** Make a code change and confirm it recompiles automatically

## Expected Result

- Standard Next.js project running without custom server
- No database or Prisma dependencies
- Standard Next.js scripts in package.json
- Application working correctly in development and production mode
- **Hot reload working correctly** (code changes reflected automatically)

## Essential Commands

```bash
# Cleanup
Remove-Item -Path "node_modules", "package-lock.json" -Recurse -Force
Remove-Item -Path "db", "prisma", "examples" -Recurse -Force

# Reinstall and test
pnpm install
pnpm build
pnpm dev
```
