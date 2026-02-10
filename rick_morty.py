import requests
import json
import time
import os
import random

url = "https://rickandmortyapi.com/api/character"
VAULT_FILE = "character_vault.json"

def load_vault():
    """Helper to load the saved characters list."""
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_to_vault(character, vault):
    """Adds a new character to the vault if they aren't already saved."""
    # Check if character ID is already in our list to avoid duplicates
    if not any(item['id'] == character['id'] for item in vault):
        vault.append(character)
        with open(VAULT_FILE, "w", encoding="utf-8") as f:
            json.dump(vault, f, indent=4, ensure_ascii=False)
        print(f"✨ {character['name']} has been added to your vault!")
    else:
        print(f"📋 {character['name']} was already in your vault.")

def get_character():
    vault = load_vault()
    
    try:
        # Try to get fresh data
        print("Searching the Multiverse...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        new_char = random.choice(data['results'])
        
        # Save this specific character to our local collection
        save_to_vault(new_char, vault)
        return new_char, "LIVE"

    except (requests.exceptions.RequestException):
        # Fallback to Vault
        print("📡 Signal lost! Accessing the Offline Vault...")
        
        if vault:
            return random.choice(vault), "OFFLINE VAULT"
        else:
            print("⚠️ The vault is empty and there's no internet!")
            return None, None

# Execute
char, source = get_character()

if char:
    print("-" * 30)
    print(f"Source: {source}")
    print(f"Character: {char['name']}")
    print(f"Species: {char['species']}")
    print("Wait for it...")
    time.sleep(1.5)
    print(f"Status: {char['status']}")
    print("-" * 30)