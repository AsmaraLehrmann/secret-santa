#!/usr/bin/env python3
"""
Send ONE late wishlist to whoever is buying for the person who just submitted.
This is a one-time script - it will send to exactly ONE person.
NO SPOILERS - You won't see who gets it!
"""

import json
import smtplib
from email.message import EmailMessage

# Load credentials
with open("email_auth.json") as f:
    email_auth = json.load(f)
    gmail_username = email_auth['gmail_username']
    gmail_app_password = email_auth['gmail_app_password']

def mailer(recipient, message, sender="Santa's Workshop", subject="Secret Santa"):
    """Send an email"""
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_username, gmail_app_password)
    server.send_message(msg)
    server.quit()

def send_single_late_wishlist(person_name, dry_run=True):
    """
    Send late wishlist for ONE specific person.
    
    :param person_name: The name of the person who just submitted their wishlist
    :param dry_run: If True, don't actually send
    """
    # Load game state
    try:
        with open("santa_game_state.json", 'r') as f:
            game_state = json.load(f)
    except FileNotFoundError:
        print("Error: santa_game_state.json not found!")
        return
    
    # Find this person in the game (case-insensitive)
    person_name_key = None
    for name in game_state['participants'].keys():
        if name.lower() == person_name.lower():
            person_name_key = name
            break
    
    if not person_name_key:
        print(f"Error: {person_name} not found in participants!")
        print(f"Available names: {', '.join(game_state['participants'].keys())}")
        return
    
    receiver_details = game_state['participants'][person_name_key]
    
    # Check they have a wishlist
    if not receiver_details['wishlist_received']:
        print(f"Error: {person_name_key} hasn't submitted a wishlist yet!")
        return
    
    # Find who's buying for them (case-insensitive)
    giver_name = None
    for g_name, r_name in game_state['assignments'].items():
        if r_name.lower() == person_name_key.lower():
            giver_name = g_name
            break
    
    if not giver_name:
        print(f"Error: Couldn't find who's buying for {person_name_key}")
        return
    
    giver_details = game_state['participants'][giver_name]
    
    print("=" * 60)
    print("SEND LATE WISHLIST")
    print("=" * 60)
    print(f"\nSending late wishlist for: {person_name_key}")
    print("(Their Secret Santa will receive it - keeping secret who!)\n")
    
    # Compose email
    msg = f"""Ho ho ho! Looks like {person_name_key}'s letter got lost on the way to the North Pole! Here is their wishlist:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{receiver_details['wishlist_content']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remember: Items should be under $10!

If you have any questions, please reach out to Santa's Helper, Asmara.

Merry Christmas! 🎄
"""
    
    if dry_run:
        print("DRY RUN - Would send late wishlist (keeping secret who gets it!)")
        print("\nEmail preview:")
        print("-" * 60)
        print(msg)
        print("-" * 60)
    else:
        response = input(f"\nSend late wishlist to {person_name_key}'s Secret Santa? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
        
        try:
            mailer(
                giver_details['email'],
                msg,
                subject=f"🎅 Update: {person_name_key}'s Wishlist Arrived!"
            )
            print(f"\nSent late wishlist! (kept secret who received it)")
        except Exception as e:
            print(f"Error sending: {e}")

if __name__ == '__main__':
    import sys
    
    print("\nSEND SINGLE LATE WISHLIST")
    print("=" * 60)
    
    # Get the person's name from command line
    if len(sys.argv) < 2:
        print("\nUsage: python send_one_late_fixed.py <name> [--send]")
        print("\nExample:")
        print("  python send_one_late_fixed.py rachael        # dry run")
        print("  python send_one_late_fixed.py rachael --send # actually send")
        print()
        
        # Show available names
        try:
            with open("santa_game_state.json", 'r') as f:
                game_state = json.load(f)
            print("Available names:")
            for name in game_state['participants'].keys():
                print(f"  - {name}")
        except:
            pass
        
        sys.exit(1)
    
    person_name = sys.argv[1]
    dry_run = '--send' not in sys.argv and '-s' not in sys.argv
    
    if dry_run:
        print("DRY RUN MODE\n")
    else:
        print("SENDING FOR REAL\n")
    
    send_single_late_wishlist(person_name, dry_run=dry_run)
