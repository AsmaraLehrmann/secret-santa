#!/usr/bin/env python3
"""
Force send Secret Santa assignments, even if some people haven't responded.
For people who didn't send wishlists, includes a note in the assignment email.
NO SPOILERS - Keeps assignments secret from you!
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

def force_send_assignments(dry_run=True):
    """
    Send assignments to EVERYONE, even if their recipient didn't submit wishlist.
    """
    # Load game state
    try:
        with open("santa_game_state.json", 'r') as f:
            game_state = json.load(f)
    except FileNotFoundError:
        print("Error: santa_game_state.json not found!")
        return
    
    # Count status
    total = len(game_state['participants'])
    received = sum(1 for p in game_state['participants'].values() if p['wishlist_received'])
    
    print("=" * 60)
    print("FORCE SEND ASSIGNMENTS")
    print("=" * 60)
    print(f"\nStatus: {received}/{total} wishlists received")
    print()
    
    if received < total:
        print("⚠️  WARNING: Not everyone has sent their wishlist!")
        print("   Assignments will include a note for missing wishlists.\n")
    
    if not dry_run:
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
    
    print()
    assignments_sent = 0
    skipped = 0
    
    for giver_name, receiver_name in game_state['assignments'].items():
        giver_details = game_state['participants'][giver_name]
        receiver_details = game_state['participants'][receiver_name]
        
        # Skip if already sent
        if giver_details.get('assignment_sent', False):
            skipped += 1
            continue
        
        # Compose email
        if receiver_details['wishlist_received']:
            # Receiver sent wishlist - normal email
            msg = f"""Ho ho ho! 🎅

You are the Secret Santa for {receiver_name.capitalize()}! Don't tell anyone!

They have sent the following message to the North Pole:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{receiver_details['wishlist_content']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Remember: Items should be under $10!

If you have any questions, please reach out to Santa's Helper, Asmara.

Merry Christmas! 🎄
"""
        else:
            # Receiver didn't send wishlist - modified email
            msg = f"""Ho ho ho! 🎅

You are the Secret Santa for {receiver_name.capitalize()}! Don't tell anyone!

Unfortunately, {receiver_name.capitalize()} did not send their wishlist in time. 
You may want to reach out to them directly or choose a gift based on what you know about them!

Remember: Items should be under $10!

If you have any questions, please reach out to Santa's Helper, Asmara.

Merry Christmas! 🎄
"""
        
        if dry_run:
            # Don't show who gets who - keep it secret!
            assignments_sent += 1
        else:
            mailer(
                giver_details['email'],
                msg,
                subject=f"🎅 Your Secret Santa Assignment: {receiver_name.capitalize()}!"
            )
            print(f"✉️  Sent assignment email")
            
            # Mark as sent
            game_state['participants'][giver_name]['assignment_sent'] = True
            assignments_sent += 1
    
    if not dry_run and assignments_sent > 0:
        # Save updated state
        with open("santa_game_state.json", 'w') as f:
            json.dump(game_state, f, indent=2)
        print(f"\n✅ Sent {assignments_sent} assignment(s)!")
        if skipped > 0:
            print(f"⏭️  Skipped {skipped} (already sent)")
    elif dry_run:
        print(f"\n⚠️  DRY RUN - Would send {assignments_sent} assignment(s)")
        if skipped > 0:
            print(f"⏭️  Would skip {skipped} (already sent)")
    else:
        print(f"\n⚠️  No new assignments sent")

if __name__ == '__main__':
    import sys
    
    # Check for --force flag
    if '--force' in sys.argv or '-f' in sys.argv:
        print("\n🚨 FORCE MODE - Sending assignments for real!\n")
        force_send_assignments(dry_run=False)
    else:
        print("\n📋 DRY RUN - Testing what would be sent\n")
        print("To actually send, run: python force_send.py --force\n")
        force_send_assignments(dry_run=True)
```

## Now it's safe! 🎅

**Dry run output:**
```
Status: 6/7 wishlists received
⚠️  DRY RUN - Would send 7 assignment(s)
