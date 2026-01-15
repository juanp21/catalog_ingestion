"""
models.py - Define cómo se ve la base de datos
VERSIÓN 2: Con sistema de usuarios
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Crear el objeto de base de datos
db = SQLAlchemy()

# ==================================================
# NUEVO: MODELO User (Tabla de usuarios)
# ==================================================
class User(UserMixin, db.Model):
    """
    Esta clase representa UN USUARIO en la base de datos.
    UserMixin agrega funcionalidades para Flask-Login (is_authenticated, etc.)
    """
    
    # Columna ID (identificador único)
    id = db.Column(db.Integer, primary_key=True)
    
    # Nombre de usuario (único)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # unique=True significa que no puede haber 2 usuarios "acrylic"
    
    # Email (único)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Password encriptado (NUNCA guardes passwords en texto plano)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # ============================================
    # NUEVO: Rol de usuario
    # ============================================
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    # is_admin = True → Puede ver todos los usuarios y sus catálogos
    # is_admin = False → Solo ve su propio catálogo
    
    # Fecha de registro
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ============================================
    # RELACIÓN: Un usuario tiene muchos tracks
    # ============================================
    tracks = db.relationship('Track', backref='owner', lazy=True, cascade='all, delete-orphan')
    # tracks = lista de todos los tracks de este usuario
    # backref='owner' = desde un Track puedes hacer track.owner para ver quién lo subió
    # cascade='all, delete-orphan' = si borras el usuario, se borran sus tracks
    
    def __repr__(self):
        return f'<User {self.username}>'


# ==================================================
# MODELO: Track (Tabla de canciones) - ACTUALIZADO
# ==================================================
class Track(db.Model):
    """
    Esta clase representa UNA CANCIÓN en la base de datos.
    AHORA: Cada track pertenece a un usuario
    """
    
    # Columna ID
    id = db.Column(db.Integer, primary_key=True)
    
    # ============================================
    # NUEVO: Relación con usuario
    # ============================================
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # ForeignKey significa "este número apunta al id de un User"
    # nullable=False = obligatorio, todo track debe tener dueño
    
    # Información básica del track
    track_name = db.Column(db.String(200), nullable=False)
    artists = db.Column(db.String(500))
    album = db.Column(db.String(200))
    
    # Códigos
    isrc = db.Column(db.String(50), index=True)
    # Ya no es unique=True porque dos usuarios pueden tener el mismo ISRC
    upc = db.Column(db.String(50))
    
    # Enlaces
    spotify_url = db.Column(db.String(300))
    spotify_id = db.Column(db.String(100))
    
    # ============================================
    # NUEVO: Audio Features (Spotify)
    # ============================================
    tempo = db.Column(db.Float)  # BPM
    energy = db.Column(db.Float)  # 0.0 - 1.0
    danceability = db.Column(db.Float)  # 0.0 - 1.0
    valence = db.Column(db.Float)  # 0.0 - 1.0 (positividad)
    acousticness = db.Column(db.Float)  # 0.0 - 1.0
    instrumentalness = db.Column(db.Float)  # 0.0 - 1.0
    key = db.Column(db.Integer)  # 0-11 (C, C#, D, etc.)
    mode = db.Column(db.Integer)  # 0 = minor, 1 = major
    time_signature = db.Column(db.Integer)  # 3, 4, 5, etc.
    
    # ============================================
    # NUEVO: Artist Stats (Spotify)
    # ============================================
    artist_id = db.Column(db.String(100))  # ID del primer artista
    artist_followers = db.Column(db.Integer)  # Seguidores en Spotify
    artist_popularity = db.Column(db.Integer)  # 0-100
    artist_genres = db.Column(db.String(500))  # "reggaeton, latin trap, urbano latino"
    artist_image_url = db.Column(db.String(500))  # NUEVO: URL de imagen del artista
    
    # ============================================
    # NUEVO: Album Info
    # ============================================
    album_image_url = db.Column(db.String(500))  # NUEVO: URL de portada del álbum
    
    # ============================================
    # NUEVO: Location (MusicBrainz)
    # ============================================
    artist_country = db.Column(db.String(200))  # "Puerto Rico", "Colombia", etc.
    artist_city = db.Column(db.String(200))  # "San Juan", "Medellín", etc.
    
    # ============================================
    # NUEVO: Social Media Stats (Instagram, TikTok)
    # ============================================
    instagram_username = db.Column(db.String(100))  # Username de Instagram
    instagram_followers = db.Column(db.Integer)  # Seguidores en Instagram
    tiktok_username = db.Column(db.String(100))  # Username de TikTok
    tiktok_followers = db.Column(db.Integer)  # Seguidores en TikTok
    
    # ============================================
    # NUEVO: Clearance System
    # ============================================
    clearance_type = db.Column(db.String(50))  # "EasyClear", "PreClear", "FreeClear"
    clearance_price = db.Column(db.Float)  # Precio establecido por usuario (null para FreeClear)
    
    # ============================================
    # NUEVO: Last.fm Data
    # ============================================
    lastfm_tags = db.Column(db.String(500))  # "rock, alternative, indie"
    lastfm_playcount = db.Column(db.Integer)
    lastfm_listeners = db.Column(db.Integer)
    
    # Fecha
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el track a diccionario"""
        return {
            'id': self.id,
            'track_name': self.track_name,
            'artists': self.artists,
            'album': self.album,
            'isrc': self.isrc,
            'upc': self.upc,
            'spotify_url': self.spotify_url,
            'spotify_id': self.spotify_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            # Audio features
            'tempo': self.tempo,
            'energy': self.energy,
            'danceability': self.danceability,
            'valence': self.valence,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'key': self.key,
            'mode': self.mode,
            'time_signature': self.time_signature,
            # Artist stats
            'artist_id': self.artist_id,
            'artist_followers': self.artist_followers,
            'artist_popularity': self.artist_popularity,
            'artist_genres': self.artist_genres,
            'artist_image_url': self.artist_image_url,
            'album_image_url': self.album_image_url,
            # Location
            'artist_country': self.artist_country,
            'artist_city': self.artist_city,
            # Social Media
            'instagram_username': self.instagram_username,
            'instagram_followers': self.instagram_followers,
            'tiktok_username': self.tiktok_username,
            'tiktok_followers': self.tiktok_followers,
            # Clearance
            'clearance_type': self.clearance_type,
            'clearance_price': self.clearance_price,
            # Last.fm data
            'lastfm_tags': self.lastfm_tags,
            'lastfm_playcount': self.lastfm_playcount,
            'lastfm_listeners': self.lastfm_listeners
        }
    
    def __repr__(self):
        return f'<Track {self.track_name} by {self.artists}>'


# ==================================================
# FUNCIONES ÚTILES - ACTUALIZADAS
# ==================================================

def init_db(app):
    """Inicializa la base de datos con la app de Flask"""
    db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas si no existen
        db.create_all()
        print("✅ Base de datos inicializada (con tabla Users)")


def add_track(track_data, user_id):
    """
    Agrega una canción a la base de datos
    AHORA: Requiere user_id (dueño del track) y soporta campos extendidos
    
    Args:
        track_data (dict): Diccionario con info del track
        user_id (int): ID del usuario dueño
    
    Returns:
        Track: El track guardado, o None si ya existe
    """
    # Verificar si ya existe (mismo ISRC para el MISMO usuario)
    if track_data.get('isrc'):
        existing = Track.query.filter_by(
            isrc=track_data['isrc'],
            user_id=user_id  # NUEVO: buscar en tracks de este usuario
        ).first()
        if existing:
            print(f"⚠️  Track ya existe en tu catálogo: {track_data['track_name']}")
            return None
    
    # Crear nuevo track
    new_track = Track(
        user_id=user_id,
        track_name=track_data.get('track_name'),
        artists=track_data.get('artists'),
        album=track_data.get('album'),
        isrc=track_data.get('isrc'),
        upc=track_data.get('upc'),
        spotify_url=track_data.get('spotify_url'),
        spotify_id=track_data.get('track_id'),
        # NUEVO: Audio features
        tempo=track_data.get('tempo'),
        energy=track_data.get('energy'),
        danceability=track_data.get('danceability'),
        valence=track_data.get('valence'),
        acousticness=track_data.get('acousticness'),
        instrumentalness=track_data.get('instrumentalness'),
        key=track_data.get('key'),
        mode=track_data.get('mode'),
        time_signature=track_data.get('time_signature'),
        # NUEVO: Artist stats
        artist_id=track_data.get('artist_id'),
        artist_followers=track_data.get('artist_followers'),
        artist_popularity=track_data.get('artist_popularity'),
        artist_genres=track_data.get('artist_genres'),
        artist_image_url=track_data.get('artist_image_url'),
        album_image_url=track_data.get('album_image_url'),
        # NUEVO: Location
        artist_country=track_data.get('artist_country'),
        artist_city=track_data.get('artist_city'),
        # NUEVO: Social Media
        instagram_username=track_data.get('instagram_username'),
        instagram_followers=track_data.get('instagram_followers'),
        tiktok_username=track_data.get('tiktok_username'),
        tiktok_followers=track_data.get('tiktok_followers'),
        # NUEVO: Last.fm data
        lastfm_tags=track_data.get('lastfm_tags'),
        lastfm_playcount=track_data.get('lastfm_playcount'),
        lastfm_listeners=track_data.get('lastfm_listeners')
    )
    
    db.session.add(new_track)
    db.session.commit()
    
    print(f"✅ Track guardado: {track_data['track_name']}")
    return new_track


def search_tracks(query, user_id):
    """
    Busca tracks en la base de datos
    AHORA: Solo busca en los tracks del usuario
    
    Args:
        query (str): Texto a buscar
        user_id (int): ID del usuario
    
    Returns:
        list: Lista de tracks que coinciden
    """
    return Track.query.filter(
        Track.user_id == user_id,  # NUEVO: filtrar por usuario
        db.or_(
            Track.track_name.ilike(f'%{query}%'),
            Track.artists.ilike(f'%{query}%'),
            Track.isrc.ilike(f'%{query}%')
        )
    ).all()


def get_all_tracks(user_id, limit=100):
    """
    Obtiene todos los tracks del usuario
    AHORA: Solo devuelve tracks del usuario especificado
    
    Args:
        user_id (int): ID del usuario
        limit (int): Máximo número de tracks
    
    Returns:
        list: Lista de tracks
    """
    return Track.query.filter_by(user_id=user_id).order_by(
        Track.created_at.desc()
    ).limit(limit).all()


def get_catalog_stats(user_id):
    """
    Obtiene estadísticas del catálogo del usuario
    AHORA: Solo stats de este usuario
    
    Args:
        user_id (int): ID del usuario
    
    Returns:
        dict: Diccionario con stats
    """
    total_tracks = Track.query.filter_by(user_id=user_id).count()
    tracks_with_isrc = Track.query.filter(
        Track.user_id == user_id,
        Track.isrc != None,
        Track.isrc != ''
    ).count()
    tracks_with_upc = Track.query.filter(
        Track.user_id == user_id,
        Track.upc != None,
        Track.upc != ''
    ).count()
    
    return {
        'total_tracks': total_tracks,
        'tracks_with_isrc': tracks_with_isrc,
        'tracks_with_upc': tracks_with_upc
    }


# ==================================================
# NUEVAS FUNCIONES: Manejo de usuarios
# ==================================================

def create_user(username, email, password, is_admin=False):
    """
    Crea un nuevo usuario
    El PRIMER usuario creado será admin automáticamente
    
    Args:
        username (str): Nombre de usuario
        email (str): Email
        password (str): Password (será encriptado)
        is_admin (bool): Si es admin (opcional)
    
    Returns:
        User: Usuario creado, o None si ya existe
    """
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    
    # Verificar si ya existe
    if User.query.filter_by(username=username).first():
        return None, "Username ya existe"
    if User.query.filter_by(email=email).first():
        return None, "Email ya existe"
    
    # Verificar si es el primer usuario (hacer admin automáticamente)
    user_count = User.query.count()
    if user_count == 0:
        is_admin = True
        print("🔑 Primer usuario - asignado como ADMIN automáticamente")
    
    # Crear usuario con password encriptado
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        is_admin=is_admin
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    role = "ADMIN" if is_admin else "USER"
    print(f"✅ Usuario creado: {username} ({role})")
    return new_user, None


def get_user_by_email(email):
    """Busca usuario por email"""
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    """Busca usuario por username"""
    return User.query.filter_by(username=username).first()


def verify_password(user, password):
    """
    Verifica si el password es correcto
    
    Args:
        user (User): Usuario
        password (str): Password a verificar
    
    Returns:
        bool: True si es correcto
    """
    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()
    return bcrypt.check_password_hash(user.password_hash, password)


# ==================================================
# FUNCIONES DE ADMINISTRACIÓN
# ==================================================

def get_all_users():
    """
    Obtiene todos los usuarios (solo para admin)
    
    Returns:
        list: Lista de usuarios con sus stats
    """
    users = User.query.order_by(User.created_at.desc()).all()
    
    users_data = []
    for user in users:
        track_count = Track.query.filter_by(user_id=user.id).count()
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'track_count': track_count,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
    return users_data


def get_user_catalog_admin(user_id):
    """
    Obtiene el catálogo de un usuario específico (solo admin)
    
    Args:
        user_id (int): ID del usuario
    
    Returns:
        dict: Catálogo y stats del usuario
    """
    user = User.query.get(user_id)
    if not user:
        return None
    
    tracks = Track.query.filter_by(user_id=user_id).order_by(
        Track.created_at.desc()
    ).limit(100).all()
    
    stats = get_catalog_stats(user_id)
    
    return {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        },
        'tracks': [track.to_dict() for track in tracks],
        'stats': stats
    }


def get_global_stats():
    """
    Obtiene estadísticas globales de toda la plataforma (solo admin)
    
    Returns:
        dict: Stats globales
    """
    total_users = User.query.count()
    total_tracks = Track.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    
    # Tracks con metadata completa
    tracks_with_isrc = Track.query.filter(
        Track.isrc != None,
        Track.isrc != ''
    ).count()
    
    return {
        'total_users': total_users,
        'total_admins': total_admins,
        'total_tracks': total_tracks,
        'tracks_with_isrc': tracks_with_isrc
    }


# ==================================================
# MODELO: ArtistCache (Caché de datos de artista)
# ==================================================
class ArtistCache(db.Model):
    """
    Caché de datos de artista para evitar llamadas repetidas a APIs
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Identificador del artista
    artist_id = db.Column(db.String(100), unique=True, index=True)  # Spotify Artist ID
    artist_name = db.Column(db.String(200), index=True)
    
    # Spotify stats
    spotify_followers = db.Column(db.Integer)
    spotify_popularity = db.Column(db.Integer)
    spotify_genres = db.Column(db.String(500))
    artist_image_url = db.Column(db.String(500))
    
    # Location (MusicBrainz)
    artist_country = db.Column(db.String(200))
    artist_city = db.Column(db.String(200))
    
    # Social media
    instagram_username = db.Column(db.String(100))
    instagram_followers = db.Column(db.Integer)
    tiktok_username = db.Column(db.String(100))
    tiktok_followers = db.Column(db.Integer)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ArtistCache {self.artist_name}>'
    
    def to_dict(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist_name,
            'spotify_followers': self.spotify_followers,
            'spotify_popularity': self.spotify_popularity,
            'spotify_genres': self.spotify_genres,
            'artist_image_url': self.artist_image_url,
            'artist_country': self.artist_country,
            'artist_city': self.artist_city,
            'instagram_username': self.instagram_username,
            'instagram_followers': self.instagram_followers,
            'tiktok_username': self.tiktok_username,
            'tiktok_followers': self.tiktok_followers
        }


def get_or_create_artist_cache(artist_id, artist_name, sp_client, fetch_complete=False, 
                                get_location_func=None, get_instagram_func=None, get_tiktok_func=None):
    """
    Obtiene datos de artista del caché o los crea si no existen
    
    Args:
        artist_id (str): Spotify Artist ID
        artist_name (str): Nombre del artista
        sp_client: Spotify client instance
        fetch_complete (bool): Si True, obtiene todos los datos (lento). Si False, solo Spotify (rápido)
        get_location_func: Function to get artist location
        get_instagram_func: Function to get Instagram stats
        get_tiktok_func: Function to get TikTok stats
    
    Returns:
        dict: Datos del artista
    """
    # Buscar en caché
    cached = ArtistCache.query.filter_by(artist_id=artist_id).first()
    
    if cached:
        # Ya existe en caché, retornar
        return cached.to_dict()
    
    # No existe, crear nuevo
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    
    cache = ArtistCache(
        artist_id=artist_id,
        artist_name=artist_name
    )
    
    # Siempre obtener datos de Spotify (rápido)
    try:
        artist_info = sp_client.artist(artist_id)
        cache.spotify_followers = artist_info['followers']['total']
        cache.spotify_popularity = artist_info['popularity']
        cache.spotify_genres = ', '.join(artist_info['genres'][:5])
        if artist_info['images']:
            cache.artist_image_url = artist_info['images'][0]['url']
    except Exception as e:
        print(f"⚠️  Error obteniendo Spotify stats para {artist_name}: {e}")
    
    # Si fetch_complete, obtener datos opcionales (lento)
    if fetch_complete and (get_location_func or get_instagram_func or get_tiktok_func):
        def fetch_location():
            try:
                if get_location_func:
                    location = get_location_func(artist_name)
                    if location:
                        cache.artist_country = location['country']
                        cache.artist_city = location['city']
            except Exception as e:
                print(f"⚠️  Error obteniendo location para {artist_name}: {e}")
        
        def fetch_instagram():
            try:
                if get_instagram_func:
                    instagram = get_instagram_func(artist_name)
                    if instagram:
                        cache.instagram_username = instagram['username']
                        cache.instagram_followers = instagram['followers']
            except Exception as e:
                print(f"⚠️  Error obteniendo Instagram para {artist_name}: {e}")
        
        def fetch_tiktok():
            try:
                if get_tiktok_func:
                    tiktok = get_tiktok_func(artist_name)
                    if tiktok:
                        cache.tiktok_username = tiktok['username']
                        cache.tiktok_followers = tiktok['followers']
            except Exception as e:
                print(f"⚠️  Error obteniendo TikTok para {artist_name}: {e}")
        
        # Ejecutar en paralelo
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(fetch_location),
                executor.submit(fetch_instagram),
                executor.submit(fetch_tiktok)
            ]
            # Esperar a que terminen
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"⚠️  Error en thread: {e}")
    
    # Guardar en DB
    db.session.add(cache)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    return cache.to_dict()


# ==================================================
# MODELO: SplitSheet (Hoja de división de regalías)
# ==================================================
class SplitSheet(db.Model):
    """
    Documento que detalla cómo se dividen las regalías de una canción
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con track
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'), nullable=False)
    track = db.relationship('Track', backref=db.backref('split_sheets', lazy=True))
    
    # Relación con usuario creador
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', backref=db.backref('created_split_sheets', lazy=True))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Estado
    status = db.Column(db.String(50), default='draft')
    # Posibles valores: 'draft', 'pending_signatures', 'completed'
    
    # PDF final
    pdf_url = db.Column(db.String(500))
    
    # Notas adicionales
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<SplitSheet {self.id} for Track {self.track_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'track_id': self.track_id,
            'created_by_user_id': self.created_by_user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status,
            'pdf_url': self.pdf_url,
            'notes': self.notes,
            'collaborators': [c.to_dict() for c in self.collaborators]
        }
    
    def total_percentage(self):
        """Calcula el porcentaje total asignado"""
        return sum(c.percentage for c in self.collaborators)
    
    def is_valid(self):
        """Verifica si el split sheet es válido (suma 100%)"""
        return abs(self.total_percentage() - 100.0) < 0.01  # Tolerancia de 0.01%
    
    def all_signed(self):
        """Verifica si todos los colaboradores han firmado"""
        return all(c.signed for c in self.collaborators)


# ==================================================
# MODELO: Collaborator (Colaborador en split sheet)
# ==================================================
class Collaborator(db.Model):
    """
    Una persona que participó en la creación de la canción
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con split sheet
    split_sheet_id = db.Column(db.Integer, db.ForeignKey('split_sheet.id'), nullable=False)
    split_sheet = db.relationship('SplitSheet', backref=db.backref('collaborators', lazy=True, cascade='all, delete-orphan'))
    
    # Información del colaborador
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    
    # Rol
    role = db.Column(db.String(100))
    # Valores comunes: 'Writer', 'Producer', 'Writer & Producer', 'Composer', etc.
    
    # Porcentaje de regalías
    percentage = db.Column(db.Float, nullable=False)
    # Debe sumar 100% entre todos los colaboradores
    
    # IPI/CAE (número de identificación en PRO)
    ipi_cae = db.Column(db.String(50))
    
    # PRO (Performance Rights Organization)
    pro = db.Column(db.String(100))
    # Ejemplos: ASCAP, BMI, SESAC, PRS, GEMA, etc.
    
    # Firma
    signed = db.Column(db.Boolean, default=False)
    signed_at = db.Column(db.DateTime)
    signature_data = db.Column(db.Text)  # Base64 de la firma (canvas)
    
    # Token único para firma
    signature_token = db.Column(db.String(100), unique=True)
    
    def __repr__(self):
        return f'<Collaborator {self.name} - {self.percentage}%>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'split_sheet_id': self.split_sheet_id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'percentage': self.percentage,
            'ipi_cae': self.ipi_cae,
            'pro': self.pro,
            'signed': self.signed,
            'signed_at': self.signed_at.isoformat() if self.signed_at else None
        }


# ==================================================
# FUNCIONES: Split Sheet Management
# ==================================================

def create_split_sheet(track_id, user_id, collaborators_data, notes=''):
    """
    Crea un nuevo split sheet
    
    Args:
        track_id (int): ID del track
        user_id (int): ID del usuario creador
        collaborators_data (list): Lista de dicts con info de colaboradores
        notes (str): Notas adicionales
    
    Returns:
        SplitSheet: El split sheet creado
    """
    import secrets
    
    # Crear split sheet
    split_sheet = SplitSheet(
        track_id=track_id,
        created_by_user_id=user_id,
        notes=notes
    )
    
    db.session.add(split_sheet)
    db.session.flush()  # Para obtener el ID
    
    # Crear colaboradores
    for collab_data in collaborators_data:
        collaborator = Collaborator(
            split_sheet_id=split_sheet.id,
            name=collab_data['name'],
            email=collab_data.get('email'),
            role=collab_data.get('role', 'Writer'),
            percentage=collab_data['percentage'],
            ipi_cae=collab_data.get('ipi_cae'),
            pro=collab_data.get('pro'),
            signature_token=secrets.token_urlsafe(32)
        )
        db.session.add(collaborator)
    
    db.session.commit()
    
    return split_sheet


def get_split_sheets_by_track(track_id):
    """Obtiene todos los split sheets de un track"""
    return SplitSheet.query.filter_by(track_id=track_id).all()


def get_split_sheet(split_sheet_id):
    """Obtiene un split sheet por ID"""
    return SplitSheet.query.get(split_sheet_id)


def sign_collaborator(signature_token, signature_data):
    """
    Firma un colaborador usando su token único
    
    Args:
        signature_token (str): Token único del colaborador
        signature_data (str): Datos de la firma en base64
    
    Returns:
        bool: True si se firmó correctamente
    """
    collaborator = Collaborator.query.filter_by(signature_token=signature_token).first()
    
    if not collaborator:
        return False
    
    collaborator.signed = True
    collaborator.signed_at = datetime.utcnow()
    collaborator.signature_data = signature_data
    
    # Actualizar estado del split sheet si todos firmaron
    split_sheet = collaborator.split_sheet
    if split_sheet.all_signed():
        split_sheet.status = 'completed'
    
    db.session.commit()
    
    return True

