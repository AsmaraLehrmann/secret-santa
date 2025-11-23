#!/usr/bin/env python3
"""
Safely collect wishlists without showing assignments.
"""
from santa_wishlist_gated import check_wishlists, load_game_state

print("Collecting wishlists from Gmail...\n")

# Collect wishlists
game_state = check_wishlists(dry_run=False)

if game_state:
    # Count without showing names
    received = sum(1 for p in game_state['participants'].values() if p['wishlist_received'])
    total = len(game_state['participants'])
    
    print(f"\n✅ Collection complete!")
    print(f"   Wishlists received: {received}/{total}")
    print(f"\n   Run 'python status.py' to see details")
else:
    print("Error loading game state")
