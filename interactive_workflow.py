#!/usr/bin/env python3
"""
Interactive Secret Santa workflow script.
Guides you through the entire process step-by-step.
"""

from santa_wishlist_gated import (
    setup_secret_santa, 
    check_status, 
    check_wishlists, 
    send_assignments
)
import os
import sys

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def wait_for_enter(msg="Press Enter to continue..."):
    input(f"\n{msg}")

def main():
    clear_screen()
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Secret Santa - Interactive Workflow  🎅            ║
║                  (Wishlist-Gated Version)                    ║
╚══════════════════════════════════════════════════════════════╝

This script will guide you through the entire Secret Santa process:

1. Send initial wishlist requests
2. Check who has responded
3. Collect wishlists
4. Send assignments when ready

Make sure you've already:
✓ Created email_auth.json with bot credentials
✓ Edited santa_wishlist_gated.py with your participants
""")
    
    wait_for_enter()
    
    # Check if game state exists
    if os.path.exists('santa_game_state.json'):
        print_header("⚠️  Existing Game Detected")
        print("Found santa_game_state.json from a previous game.")
        response = input("\nContinue with existing game? (yes/no): ")
        if response.lower() != 'yes':
            print("\nPlease delete santa_game_state.json to start fresh.")
            print("Or run the functions manually to continue existing game.")
            return
    else:
        # Step 1: Setup
        print_header("STEP 1: Initial Setup")
        print("This will:")
        print("  • Create random Secret Santa assignments")
        print("  • Save them to santa_game_state.json")
        print("  • Send wishlist request emails to everyone")
        print()
        
        response = input("Run setup? (yes/no): ")
        if response.lower() != 'yes':
            print("Setup cancelled.")
            return
        
        print("\nTesting first (dry run)...")
        setup_secret_santa(dry_run=True)
        
        print("\n" + "-"*60)
        response = input("\nLooks good? Send for real? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled. You can run setup_secret_santa() manually later.")
            return
        
        print("\n🎅 Sending wishlist requests...")
        setup_secret_santa(dry_run=False)
        
        print("\n✅ Setup complete!")
        print("\nNow wait for people to reply with their wishlists.")
        wait_for_enter()
    
    # Main loop: Check status and collect wishlists
    while True:
        clear_screen()
        print_header("STEP 2: Monitor Responses")
        
        print("What would you like to do?\n")
        print("1. Check status (who has responded)")
        print("2. Collect new wishlists from Gmail")
        print("3. Send assignments (when everyone is ready)")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            print_header("Status Check")
            check_status()
            wait_for_enter()
            
        elif choice == '2':
            print_header("Collect Wishlists")
            print("Checking Gmail for wishlist replies...\n")
            
            # Test first
            game_state = check_wishlists(dry_run=True)
            
            if game_state:
                print("\n" + "-"*60)
                response = input("\nCollect these wishlists? (yes/no): ")
                if response.lower() == 'yes':
                    check_wishlists(dry_run=False)
                    print("\n✅ Wishlists collected!")
                else:
                    print("Skipped.")
            
            wait_for_enter()
            
        elif choice == '3':
            print_header("Send Assignments")
            
            # Check status first
            print("Current status:")
            check_status()
            
            print("\n" + "-"*60)
            response = input("\nReady to send assignments? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                wait_for_enter()
                continue
            
            # Test first
            print("\nTesting first (dry run)...\n")
            send_assignments(dry_run=True)
            
            print("\n" + "-"*60)
            response = input("\nSend these assignments for real? (yes/no): ")
            if response.lower() == 'yes':
                print("\n🎅 Sending assignments...")
                send_assignments(dry_run=False)
                print("\n✅ Assignments sent!")
                print("\n🎄 Secret Santa is complete! Happy holidays!")
                wait_for_enter()
                break
            else:
                print("Cancelled.")
                wait_for_enter()
                
        elif choice == '4':
            print("\nExiting. Happy holidays! 🎅")
            break
            
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")
            wait_for_enter()
    
    print("\n" + "="*60)
    print("  Thank you for using Secret Santa! 🎄")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExited by user. Goodbye! 🎅")
        sys.exit(0)
