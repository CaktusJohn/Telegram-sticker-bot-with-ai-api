CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    username TEXT,
    ref_code TEXT UNIQUE,
    invited_by TEXT,
    stars_balance INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_TEMP_FILES_TABLE = """
CREATE TABLE IF NOT EXISTS temp_files (
    user_id INTEGER,  
    file_path TEXT,
    file_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_FACE_DETECTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS face_detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    user_id INTEGER,                        
    file_path TEXT,
    faces_count INTEGER,
    faces_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
);
"""



