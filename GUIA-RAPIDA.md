# 🚀 GUÍA RÁPIDA - Para No Programadores

## ⏱️ Tiempo total: 30 minutos

---

## PARTE 1: PREPARAR TU COMPUTADORA (10 min)

### ✅ Paso 1: Descargar Python
📍 **Página:** https://www.python.org/downloads/

1. Click en el botón grande "Download Python 3.x"
2. Instala el archivo descargado
3. **IMPORTANTE:** Marca la casilla "Add Python to PATH"
4. Click "Install Now"

### ✅ Paso 2: Descargar Visual Studio Code
📍 **Página:** https://code.visualstudio.com/

1. Descarga VSCode
2. Instala normal (siguiente, siguiente, finalizar)

### ✅ Paso 3: Descargar archivos de SONGXS
Te los envié en un ZIP. Descomprime en tu Escritorio.

---

## PARTE 2: CONFIGURAR SPOTIFY (5 min)

### ✅ Paso 4: Crear App en Spotify

📍 **Página:** https://developer.spotify.com/dashboard

1. Log in con tu Spotify
2. Click "Create app"
3. Llena:
   - App name: `SONGXS`
   - App description: `Metadata extractor`
   - Redirect URI: `http://localhost:5000`
4. Marca las casillas que te piden
5. Click "Save"

### ✅ Paso 5: Copiar tus códigos

1. Verás "Client ID" - cópialo
2. Click "Show client secret" - cópialo también
3. Guárdalos en un notepad por ahora

---

## PARTE 3: INSTALAR (5 min)

### ✅ Paso 6: Abrir Terminal/CMD

**En Mac:**
- Busca "Terminal" en Spotlight

**En Windows:**
- Busca "CMD" o "Command Prompt"

### ✅ Paso 7: Navegar a tu carpeta

```bash
cd Desktop/songxs
```

### ✅ Paso 8: Instalar librerías

```bash
pip install -r requirements.txt
```

Espera 1-2 minutos. Verás muchas cosas instalándose.

---

## PARTE 4: CONFIGURAR CÓDIGOS (2 min)

### ✅ Paso 9: Abrir código

1. Abre VSCode
2. File → Open Folder → Selecciona la carpeta `songxs`
3. Abre el archivo `app.py`

### ✅ Paso 10: Pegar tus códigos de Spotify

Busca las líneas 18-19:

```python
SPOTIFY_CLIENT_ID = 'tu_client_id_aqui'
SPOTIFY_CLIENT_SECRET = 'tu_client_secret_aqui'
```

Reemplaza con lo que copiaste:

```python
SPOTIFY_CLIENT_ID = '1234abcd...'  # Lo que copiaste
SPOTIFY_CLIENT_SECRET = '5678efgh...'  # Lo que copiaste
```

**Guarda el archivo:** Ctrl+S (Windows) o Cmd+S (Mac)

---

## PARTE 5: EJECUTAR (1 min)

### ✅ Paso 11: Iniciar la app

En la terminal, escribe:

```bash
python app.py
```

Verás algo como:
```
 * Running on http://0.0.0.0:5000
```

### ✅ Paso 12: Abrir en navegador

Abre Chrome/Firefox y ve a:

```
http://localhost:5000
```

---

## 🎉 ¡LISTO! YA ESTÁ FUNCIONANDO

Deberías ver tu página SONGXS.

### Probar:

1. Copia esta playlist de prueba:
   ```
   https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
   ```

2. Pégala en el campo "UPC/ISRC Extractor"

3. Click "Extract Metadata"

4. Espera 10-20 segundos

5. Click "Download Excel"

¡Si descarga un archivo Excel, está funcionando! ✅

---

## 🌐 PARTE 6: PONERLO EN INTERNET (Opcional)

Si quieres que otros lo usen sin tu computadora:

### ✅ Opción más fácil: Render.com

📍 **Página:** https://render.com

1. Crea cuenta (gratis)
2. Click "New +" → "Web Service"
3. Conecta con GitHub (necesitarás crear cuenta en GitHub primero)
4. Sube tu carpeta `songxs` a GitHub
5. En Render, selecciona tu proyecto
6. Configuración automática
7. Agrega tus códigos de Spotify en "Environment"
8. Deploy

En 10 minutos tendrás una URL tipo:
```
https://songxs-abc123.onrender.com
```

---

## ❓ Si algo no funciona:

### "Command not found: python"
- Reinstala Python y marca "Add to PATH"

### "No module named flask"
- Corre otra vez: `pip install -r requirements.txt`

### "Invalid client"
- Verifica que copiaste bien los códigos de Spotify

### La página no carga
- ¿Python está corriendo en la terminal?
- ¿Dice "Running on http://..."?

---

## 📞 ¿Necesitas ayuda?

Mándame screenshot del error que te salga.

---

**¡Éxito!** 🚀
