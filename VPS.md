# 🧼 VPS Docker + EasyPanel — Guia de Limpeza, Otimização e Automação

Guia prático para diagnóstico, limpeza e automação em VPS com Docker e EasyPanel. Foco em liberar espaço, padronizar manutenção e evitar recorrência de problemas.

Atualizado em: 2025-08-06 • Versão: 1.0

Sumário

- [Visão Geral](#-visão-geral)
- [Diagnóstico de Uso de Disco](#-diagnóstico-de-uso-de-disco)
- [Limpeza de Logs do Sistema](#-limpeza-de-logs-do-sistema)
- [Docker: Verificação e Limpeza](#-docker-verificação-e-limpeza)
- [Crontab: Automatizando as Limpezas](#-crontab-automatizando-as-limpezas)
- [Dicas Extras](#-dicas-extras)
- [Melhorias Futuras](#-melhorias-futuras)

## 🧠 Visão Geral

Este guia documenta o processo de diagnóstico, limpeza e automação realizado em uma VPS com Docker e EasyPanel para resolver problemas de espaço em disco e melhorar a manutenção.

---

## 🔍 Diagnóstico de Uso de Disco

### Ver uso das pastas no root:

```bash
du -d 1 | sort -n -r
```

### Ver uso dentro de `/var/log`:

```bash
sudo du -h /var/log --max-depth=1 | sort -hr
sudo du -h /var/log/* | sort -hr | head -20
```

---

## 🧹 Limpeza de Logs do Sistema

### Liberar espaço do `journal` (logs do systemd):

```bash
sudo journalctl --vacuum-time=2d
```

---

## 🐳 Docker: Verificação e Limpeza

### Verificar uso de disco pelo Docker:

```bash
docker system df
```

### Limpar containers parados, imagens não usadas e cache:

```bash
docker system prune -a
```

---

## 🔁 Crontab: Automatizando as Limpezas

### Acessar o crontab do root:

```bash
sudo crontab -e
```

### Comandos adicionados no crontab:

```bash
# Limpa imagens Docker antigas nas seg, qua e sex às 3h da manhã
0 3 * * 1,3,5 /usr/bin/docker image prune -a -f >> /var/log/docker-prune.log 2>&1

# Limpa arquivos com +7 dias no /tmp diariamente às 2h
0 2 * * * find /tmp -type f -mtime +7 -delete

# Atualiza pacotes diariamente às 4h30
30 4 * * * apt update && apt upgrade -y >> /var/log/apt-upgrade.log 2>&1

# Remove logs compactados e antigos (+14 dias) de /var/log às 1h15
15 1 * * * find /var/log -name "*.gz" -o -name "*.1" -type f -mtime +14 -delete
```

---

## 💡 Dicas Extras

### Verificar espaço em disco:

```bash
df -h
```

### Verificar diretórios mais pesados:

```bash
du -h /var | sort -hr | head -20
```

### Criar pastas úteis:

```bash
mkdir -p /root/backups
mkdir -p /var/log/cron-jobs
```

### Verificar logs do cron:

```bash
cat /var/log/syslog | grep CRON
```

---

## 🚀 Melhorias Futuras

- Instalar `fail2ban` para segurança
- Automatizar backups de containers e bancos
- Monitorar com `Netdata`, `htop` ou `glances`
- Configurar alertas por e-mail
- Usar `logrotate` para gerenciar logs

---

**Salve esse arquivo para consultar sempre que necessário.**
