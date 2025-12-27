import json
import os
from typing import Optional
from datetime import datetime


class MetadataStore:
    """Simple JSON-based metadata storage for startup profiles and analysis results."""
    
    def __init__(self, storage_dir: str = "./metadata"):
        """Initialize the metadata store."""
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_startup_profile(self, profile_id: str, profile: dict) -> None:
        """Save a startup profile."""
        filepath = os.path.join(self.storage_dir, f"startup_{profile_id}.json")
        profile["updated_at"] = datetime.now().isoformat()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2)
    
    def get_startup_profile(self, profile_id: str) -> Optional[dict]:
        """Retrieve a startup profile."""
        filepath = os.path.join(self.storage_dir, f"startup_{profile_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def save_analysis_result(self, profile_id: str, analysis: dict) -> None:
        """Save analysis results for a startup."""
        filepath = os.path.join(self.storage_dir, f"analysis_{profile_id}.json")
        analysis["updated_at"] = datetime.now().isoformat()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
    
    def get_analysis_result(self, profile_id: str) -> Optional[dict]:
        """Retrieve analysis results for a startup."""
        filepath = os.path.join(self.storage_dir, f"analysis_{profile_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_startups(self) -> list[str]:
        """List all startup profile IDs."""
        profiles = []
        for filename in os.listdir(self.storage_dir):
            if filename.startswith("startup_") and filename.endswith(".json"):
                profile_id = filename[8:-5]  # Remove "startup_" and ".json"
                profiles.append(profile_id)
        return profiles
