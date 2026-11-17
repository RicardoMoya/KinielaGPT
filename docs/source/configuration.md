## 🔧 Configuración

<br>

### 🤖 Configurar para Claude.app

Edita el archivo de configuración `claude_desktop_config.json` que según tu sistema operativo se encuentra en:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Añade una de las siguientes configuraciones según tu método de instalación:

<details>
<summary><b>Usando uvx</b></summary>

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "uvx",
      "args": ["--with", "mcp<2", "kinielagpt"]
    }
  }
}
```
</details>


<details>
<summary><b>Usando pip</b></summary>

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "python",
      "args": ["-m", "kinielagpt"]
    }
  }
}
```

```{note}
En macOS/Linux, si `python` no funciona, usa `python3` en su lugar.
```

</details>

<br>

### 💻 Configurar para VS Code

Abre la Paleta de Comandos (`Ctrl + Shift + P`), ejecuta `MCP: Open User Configuration` y añade una de las siguientes configuraciones:

<details>
<summary><b>Usando uvx</b></summary>

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "uvx",
      "args": ["--with", "mcp<2", "kinielagpt"]
    }
  }
}
```
</details>


<details>
<summary><b>Usando pip</b></summary>

```json
{
  "mcpServers": {
    "kinielagpt": {
      "command": "python",
      "args": ["-m", "kinielagpt"]
    }
  }
}
```

```{note}
En macOS/Linux, si `python` no funciona, usa `python3` en su lugar.
```
</details>

<br>

```{tip}
Como alternativa puedes crear el archivo `.vscode/mcp.json` en tu workspace para compartir la configuración con otros. Más detalles en la [documentación oficial de VS Code MCP](https://code.visualstudio.com/docs/copilot/customization/mcp-servers).
```

