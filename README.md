# Keel

**Your local dev stack** — a clean, isolated local web development environment that runs natively on your machine.

Keel is a desktop app for installing and running PHP, Node.js, Apache/Nginx/Caddy, MariaDB/MySQL, Redis, and dozens of other dev tools — **no Docker required**, no system pollution. Everything lives in Keel’s own directories; uninstall the app and you’re back to a clean system.

Available on **macOS**, **Windows**, and **Linux**.

---

## Why Keel?

- **Fast setup** — pick a stack in the wizard (Full-stack PHP, Modern JS/API, or Custom) and install in one go
- **Native & lightweight** — Tauri 2 + Rust, direct binary downloads, no containers
- **Isolated** — packages, config, and data stay separate from Homebrew and your system PATH
- **Visual management** — sites, SSL, hosts, services, tunnels, and dev mail in one app
- **Integrated CLI** — use `php`, `node`, `mysql`, and more in your terminal via Keel’s PATH
- **Auto-updates** — signed in-app updater via GitHub Releases

---

## Features

| | |
|---|---|
| **Web servers** | Apache, Nginx, Caddy |
| **Runtimes** | PHP (multiple versions), Node.js, Bun, Python |
| **Databases** | MariaDB, MySQL, PostgreSQL, MongoDB, Redis |
| **Dev tools** | Composer, phpMyAdmin, Adminer, Mailpit, Git |
| **Websites** | Virtual hosts, SSL (Keel CA), `/etc/hosts` |
| **Tunnels** | Cloudflare, bore, chisel, rathole… |
| **i18n** | Vietnamese, English, and 18+ locales |

---

## Download

Official releases:

**[Releases →](https://github.com/sanhpotter/Keel/releases)**

| Platform | Format |
|----------|--------|
| macOS | `.dmg` (Apple Silicon & Intel) |
| Windows | `.msi` / `.exe` installer |
| Linux | `.AppImage`, `.deb` |

The app checks for updates in **Settings → Application**.

---

## Quick start

1. Install Keel and open the app
2. Choose a dev role (Full-stack / Modern JS / Custom) in the **Setup wizard**
3. Keel downloads and configures your stack — on macOS you may be prompted for Keel Helper (hosts & services)
4. Go to **Websites**, create a site, and open your local URL (e.g. `http://demo.test:8080`)

Data is stored at:

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Keel/` |
| Windows | `%APPDATA%\com.keel.app\` |
| Linux | `~/.local/share/com.keel.app/` |

---

## Links

- **Issues & releases:** [github.com/sanhpotter/Keel](https://github.com/sanhpotter/Keel)

---

<p align="center">
  <sub>Keel — local dev, zero host pollution.</sub>
</p>
