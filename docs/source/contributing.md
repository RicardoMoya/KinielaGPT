# 🤝 Guía Rápida de Contribución

¡Gracias por tu interés en mejorar KinielaGPT! Sigue estos pasos sencillos:

## 🚀 ¿Cómo contribuir?

1. **Haz fork** y clona tu repositorio:
	```bash
	git clone https://github.com/tu-usuario/KinielaGPT.git
	cd KinielaGPT
	```
2. **Instala dependencias y prueba:**
	```bash
	uv sync  # o pip install -e .
	pytest
	```
3. **Crea una rama:**
	```bash
	git checkout -b feature-mi-mejora
	```
4. **Haz tus cambios y tests:**
	```bash
	pytest
	git commit -am "feature: tu mejora"
	git push origin feature-mi-mejora
	```
5. **Abre un Pull Request** en GitHub.

---

## 📋 Qué puedes aportar

- **Bugs:** Abre un issue con pasos claros para reproducir.
- **Funcionalidades:** Propón/discute en Discussions antes de programar grandes cambios.
- **Documentación:** Mejora o traduce los archivos en `docs/source/`.
- **Tests:** Añade tests en `tests/` usando `pytest`.

---

## 🛠️ Buenas prácticas

- Código limpio: sigue PEP8, usa type hints y docstrings.
- Commits claros: `feature:`, `fix:`, `docs:`, `test:`.
- Tests pasan antes de enviar PR.
- Actualiza docs si cambias la API.

---

## 📝 Recursos útiles

- **Tests:**
  ```bash
  pytest
  pytest --cov=kinielagpt
  ```
- **Formateo:**
  ```bash
  black kinielagpt/ tests/
  flake8 kinielagpt/ tests/
  ```
- **Docs:**
  ```bash
  cd docs
  make html
  ```

---

## 👥 Comunidad y soporte

Para preguntas, sugerencias o reportar issues:
- 📝 [GitHub Issues](https://github.com/RicardoMoya/KinielaGPT/issues)
- 💬 [GitHub Discussions](https://github.com/RicardoMoya/KinielaGPT/discussions)

---

Al contribuir, aceptas la licencia AGPL-3.0.

¡Gracias por hacer KinielaGPT mejor! 🎉
