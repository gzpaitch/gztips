# Gerenciar Processos e Portas no Windows

## Índice

1. [Identificar processos usando uma porta](#identificar-processos-usando-uma-porta)
2. [Entender o PID](#entender-o-pid)
3. [Encerrar processos](#encerrar-processos)
4. [Exemplos práticos](#exemplos-práticos)

---

## Identificar processos usando uma porta

### Comando básico

```bash
netstat -ano | findstr :PORTA
```

**Explicação dos parâmetros:**

- `netstat` - Comando que exibe conexões de rede ativas
- `-a` - Exibe todas as conexões e portas de escuta
- `-n` - Exibe endereços e portas em formato numérico
- `-o` - Exibe o PID (Process ID) associado a cada conexão
- `|` - Pipe (redireciona a saída para outro comando)
- `findstr` - Filtra linhas que contêm o texto especificado
- `:PORTA` - O número da porta que você quer verificar (ex: `:3000`)

### Exemplo de saída

```
TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       50060
TCP    [::]:3000              [::]:3000              LISTENING       50060
TCP    [::1]:3000             [::1]:52820            ESTABLISHED     50060
```

**Interpretação das colunas:**

1. **Protocolo** - TCP ou UDP
2. **Endereço Local** - IP:Porta local
3. **Endereço Remoto** - IP:Porta remota
4. **Estado** - Status da conexão (LISTENING, ESTABLISHED, CLOSE_WAIT, etc.)
5. **PID** - Process ID (última coluna) - **ESTE É O NÚMERO QUE VOCÊ PRECISA**

---

## Entender o PID

### O que é PID?

**PID (Process ID)** é um número único que identifica cada processo em execução no sistema operacional.

### Como identificar o PID na saída do netstat

Na saída do comando `netstat -ano`, o **PID está sempre na última coluna**:

```
TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       50060
                                                                      ^^^^^
                                                                      Este é o PID
```

### Estados de conexão comuns

- **LISTENING** - O processo está escutando/aguardando conexões naquela porta
- **ESTABLISHED** - Conexão ativa estabelecida
- **CLOSE_WAIT** - Conexão sendo fechada
- **TIME_WAIT** - Aguardando para garantir que a conexão foi fechada
- **FIN_WAIT** - Finalizando conexão

---

## Encerrar processos

### Comando para encerrar um processo

**IMPORTANTE: O número de barras depende do terminal que você está usando!**

#### CMD do Windows (Prompt de Comando)

```cmd
taskkill /F /PID NUMERO_DO_PID
```

#### Git Bash / Bash no Windows

```bash
taskkill //F //PID NUMERO_DO_PID
```

**Explicação dos parâmetros:**

- `taskkill` - Comando para encerrar processos
- `/F` ou `//F` - Force (força o encerramento do processo)
- `/PID` ou `//PID` - Especifica que você vai informar um Process ID
- `NUMERO_DO_PID` - O número do PID que você identificou

**Por que a diferença?**

- No **CMD** do Windows, use **uma barra** (`/F`, `/PID`)
- No **Git Bash** ou terminais Unix-like, use **duas barras** (`//F`, `//PID`) porque uma barra é interpretada como caminho de arquivo

### Verificar qual programa está usando o PID (opcional)

Antes de matar um processo, você pode verificar qual programa ele representa:

```bash
tasklist | findstr NUMERO_DO_PID
```

---

## Exemplos práticos

### Exemplo 1: Liberar a porta 3000

**Passo 1:** Identificar qual processo está usando a porta

```bash
netstat -ano | findstr :3000
```

**Saída:**

```
TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       50060
TCP    [::]:3000              [::]:3000              LISTENING       50060
```

**Passo 2:** Identificar o PID (última coluna): `50060`

**Passo 3:** (Opcional) Ver qual programa é

```bash
tasklist | findstr 50060
```

**Passo 4:** Encerrar o processo

No CMD:

```cmd
taskkill /F /PID 50060
```

No Git Bash:

```bash
taskkill //F //PID 50060
```

**Passo 5:** Verificar se a porta está livre

```bash
netstat -ano | findstr :3000
```

Se não houver saída, a porta está livre!

---

### Exemplo 2: Múltiplos processos na mesma porta

Se você encontrar vários PIDs diferentes:

```
TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       50060
TCP    [::1]:3000             [::1]:52820            ESTABLISHED     14144
```

Você precisa encerrar cada PID individualmente:

No CMD:

```cmd
taskkill /F /PID 50060
taskkill /F /PID 14144
```

No Git Bash:

```bash
taskkill //F //PID 50060
taskkill //F //PID 14144
```

---

### Exemplo 3: Portas comuns em desenvolvimento

| Porta | Uso comum                             |
| ----- | ------------------------------------- |
| 3000  | React, Node.js                        |
| 4200  | Angular                               |
| 5000  | Flask, .NET                           |
| 8000  | Django, Python HTTP Server            |
| 8080  | Tomcat, servidores de desenvolvimento |
| 9000  | PHP, diversos frameworks              |

---

## Resumo dos comandos

### No CMD do Windows

```cmd
# 1. Descobrir quem está usando a porta
netstat -ano | findstr :PORTA

# 2. Identificar qual programa (opcional)
tasklist | findstr PID

# 3. Encerrar o processo
taskkill /F /PID NUMERO_DO_PID

# 4. Confirmar que a porta está livre
netstat -ano | findstr :PORTA
```

### No Git Bash

```bash
# 1. Descobrir quem está usando a porta
netstat -ano | findstr :PORTA

# 2. Identificar qual programa (opcional)
tasklist | findstr PID

# 3. Encerrar o processo
taskkill //F //PID NUMERO_DO_PID

# 4. Confirmar que a porta está livre
netstat -ano | findstr :PORTA
```

---

## Dicas importantes

1. **Sempre identifique o processo antes de matar** - Use `tasklist` para ter certeza do que está encerrando
2. **Cuidado com processos do sistema** - Alguns PIDs são críticos para o Windows
3. **Use //F com cuidado** - A flag force encerra sem salvar dados
4. **Várias instâncias** - Se você iniciou o mesmo servidor várias vezes, pode haver múltiplos PIDs
5. **Reinicie se necessário** - Se um processo não morrer, pode ser necessário reiniciar o computador

---

## Alternativas

### PowerShell (alternativa mais moderna)

```powershell
# Encontrar processo na porta 3000
Get-NetTCPConnection -LocalPort 3000 | Select-Object -Property LocalPort, OwningProcess

# Encerrar processo
Stop-Process -Id PID -Force
```

### GUI (Interface Gráfica)

1. Abra o **Gerenciador de Tarefas** (Ctrl + Shift + Esc)
2. Vá na aba **Detalhes**
3. Procure pelo PID
4. Clique com botão direito > **Finalizar tarefa**
