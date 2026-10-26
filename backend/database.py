import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")


def get_supabase() -> Client:
    """
    Creates a Supabase client for ReLoop's FastAPI backend.
    """

    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL is missing from .env"
        )

    if not SUPABASE_SECRET_KEY:
        raise RuntimeError(
            "SUPABASE_SECRET_KEY is missing from .env"
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_SECRET_KEY
    )