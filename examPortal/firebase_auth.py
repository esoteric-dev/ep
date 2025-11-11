"""
Firebase Authentication utilities for the Django application.
This module provides functions to integrate Firebase Authentication with Django.
"""
import os
from django.conf import settings

# Firebase Admin SDK initialization (optional, for server-side verification)
try:
    import firebase_admin
    from firebase_admin import credentials, auth as firebase_auth
    
    # Initialize Firebase Admin SDK if credentials are provided
    if settings.FIREBASE_ADMIN_CREDENTIAL_PATH and os.path.exists(settings.FIREBASE_ADMIN_CREDENTIAL_PATH):
        cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL_PATH)
        firebase_admin.initialize_app(cred)
        FIREBASE_ADMIN_INITIALIZED = True
    else:
        FIREBASE_ADMIN_INITIALIZED = False
except Exception as e:
    print(f"Firebase Admin SDK initialization skipped: {e}")
    FIREBASE_ADMIN_INITIALIZED = False


def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token.
    
    Args:
        id_token: The Firebase ID token to verify
        
    Returns:
        dict: The decoded token if valid, None otherwise
    """
    if not FIREBASE_ADMIN_INITIALIZED:
        return None
    
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        return None


def get_firebase_config():
    """
    Get Firebase configuration for client-side use.
    
    Returns:
        dict: Firebase configuration
    """
    return settings.FIREBASE_CONFIG
