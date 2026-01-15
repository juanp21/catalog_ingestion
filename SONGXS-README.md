# SONGXS - Music Metadata Extractor MVP

Herramienta web simple para extraer metadata de Spotify y trabajar con ISRCs.

## 🎯 Funcionalidades

1. **UPC/ISRC Extractor:** Playlist de Spotify → Excel con metadata
2. **ISRC to Playlist:** Lista de ISRCs → Tracks encontrados → Excel

---

## 📦 INSTALACIÓN LOCAL

### 1. Instalar Python

Descarga Python 3.11+: https://www.python.org/downloads/

Verifica instalación:
```bash
python --version
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Spotify API

1. Ve a: https://developer.spotify.com/dashboard
2. Crea una app
3. Copia Client ID y Client Secret
4. Pégalos en `app.py` líneas 18-19

### 4. Ejecutar

```bash
python app.py
```

Abre: http://localhost:5000

---

## 🚀 DEPLOY GRATIS (Render.com)

### Paso 1: Subir a GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/songxs.git
git push -u origin main
```

### Paso 2: Deploy en Render

1. Crea cuenta: https://render.com
2. New → Web Service
3. Conecta tu repo de GitHub
4. Configuración:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Plan: Free
5. Variables de entorno:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
6. Create Web Service

Espera 10 minutos. Tu URL: `https://songxs.onrender.com`

---

## 📁 Estructura de Archivos

```
songxs/
├── app.py              (Backend Flask)
├── requirements.txt    (Dependencias)
└── templates/
    └── index.html      (Frontend)
```

---

## 🎨 Personalizar

### Cambiar nombre/colores:

Edita `templates/index.html`:
- Busca "SONGXS" y reemplaza
- Colores: `bg-black`, `bg-zinc-900`, etc.

---

## ✅ TODO funcionará en:

- ✅ Tu computadora (localhost)
- ✅ Internet gratis (Render.com)
- ✅ Descarga Excel funcional
- ✅ Diseño oscuro/moderno

---

**Tiempo estimado:** 30 minutos para tenerlo funcionando
**Costo:** $0
