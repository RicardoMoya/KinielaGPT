## ⚡ Antes de Empezar

Antes de usar `KinielaGPT` necesitaras tener instalado **UV** (recomendado) o **Python 3.10+**.

A continuación se muestran como instalar las dos opciones, aunque debes elegir una de las dos:


### Opción 1: UV (Recomendado) 

[UV](https://docs.astral.sh/uv/) es un gestor de paquetes y proyectos Python ultrarrápido que simplifica la instalación y ejecución de herramientas Python. **No requiere tener Python pre-instalado**.

<details>
<summary><b>🪟 Instalar UV en Windows</b></summary>

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar:
```powershell
uv --version
```
</details>

<details>
<summary><b>🍎🐧 Instalar UV en macOS/Linux</b></summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verificar:
```bash
uv --version
```

```{warning}
Reinicia tu terminal después de la instalación.
```
</details>

<br>

### Opción 2: Python 3.10+ y pip

Si ya tienes Python instalado y prefieres el método tradicional, puedes usar pip (el gestor de paquetes de Python). Requiere tener Python 3.10 o superior ya instalado en tu sistema.

<details>
<summary><b>🪟 Instalar Python en Windows</b></summary>

1. Descarga Python 3.10+ desde [python.org/downloads](https://www.python.org/downloads/)
2. **Marca "Add Python to PATH"** durante la instalación
3. Verifica:
```powershell
python --version
pip --version
```
</details>

<details>
<summary><b>🍎 Instalar Python en macOS</b></summary>

**macOS:**
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python 3.10+ para macOS
3. Ejecuta el instalador . pkg

Verifica:
```bash
python3 --version
pip3 --version
```
</details>

<details>
<summary><b>🐧 Instalar Python Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install python3.10 python3-pip python3.10-venv
```

Verifica:
```bash
python3 --version
pip3 --version
```
</details>