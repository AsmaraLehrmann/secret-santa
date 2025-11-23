import random
import copy
import smtplib
from email.message import EmailMessage
import json
import imaplib
import email
from datetime import datetime

with open("email_auth.json") as f:
    # Read in the auth for your mail account (tested with gmail app password only)
    email_auth = json.load(f)
    gmail_username = email_auth['gmail_username']
    gmail_app_password = email_auth['gmail_app_password']

def mailer(recipient, message, sender="Santa's Workshop", subject="Secret Santa", reply_to=None):
    """
    Utility script for sending emails.
    :param recipient: email recipient
    :param message: email message
    :param sender: sender name
    :param subject: email subject
    :param reply_to: optional reply-to address
    :return: None
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    if reply_to:
        msg['Reply-To'] = reply_to
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_username, gmail_app_password)
    server.send_message(msg)
    server.quit()
    

def make_matches(email_dict, blocked_matches=()):
    """
    Randomise a list of participants and match them into giver:receiver pairs, ensuring that no-one is assigned
    themselves and that (optionally) certain pairings are blocked
    :param email_dict: Dictionary of participants and their details. We only use the keys of this dict
    :param blocked_matches: optional list of sets of blocked pairs in format ({'alice', 'bob'}) where we don't want
    Alice or Bob to be assigned each other
    :return: list of tuples in format [(giver, receiver)]
    """
    candidates = list(email_dict.keys())
    receivers = copy.copy(candidates)
    random.shuffle(receivers)
    pairs = []
    for giver, receiver in zip(candidates, receivers):
        if giver == receiver:
            # we can't have someone send a gift to themselves!
            print(f"self santa detected! {giver} buys for {receiver}. Retrying")
            return False
        if {giver, receiver} in blocked_matches:
            # note that blocked_matches is empty by default. Santa only cheats if you tell him to!
            print(f"undesirable secret santa detected! {giver} buys for {receiver}. Retrying")
            return False
        pairs.append((giver, receiver))
    return pairs


def save_game_state(matches, participants, filename="santa_game_state.json"):
    """
    Save the game state including assignments and wishlist status
    :param matches: List of tuples (giver, receiver)
    :param participants: Dictionary with participant details
    :param filename: Name of file to save state
    :return: None
    """
    game_state = {
        'assignments': {},  # giver: receiver
        'participants': {},  # name: {email, wishlist_received, wishlist_content}
        'created_at': datetime.now().isoformat()
    }
    
    # Save assignments
    for giver, receiver in matches:
        game_state['assignments'][giver] = receiver
    
    # Save participant details
    for name, details in participants.items():
        game_state['participants'][name] = {
            'email': details['email'],
            'wishlist_received': False,
            'wishlist_content': None,
            'assignment_sent': False
        }
    
    with open(filename, 'w') as f:
        json.dump(game_state, f, indent=2)
    
    print(f"Game state saved to {filename}")
    return game_state


def load_game_state(filename="santa_game_state.json"):
    """
    Load the saved game state
    :param filename: Name of file to load
    :return: game_state dictionary or None if file doesn't exist
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run setup_secret_santa() first!")
        return None


def send_initial_requests(participants, dry_run=True):
    """
    Send the initial wishlist request emails to all participants.
    They must send their wishlist to receive their assignment!
    
    :param participants: Dictionary of participants with names and emails
    :param dry_run: if True, doesn't send real emails
    :return: None
    """
    msg_template = """Ho ho ho from the North Pole! 🎅

In order to get your Secret Santa assignment, you need to send a letter to Santa with a list of your interests or a wishlist of items under $10!

Simply REPLY to this email with your wishlist or interests, and Santa will reveal your Secret Santa assignment once everyone has responded!

Merry Christmas! 🎄

P.S. Don't forget to actually reply to this email with your wishlist!
"""
    
    print("=" * 60)
    print("SENDING WISHLIST REQUESTS")
    print("=" * 60)
    
    for name, details in participants.items():
        if dry_run:
            print(f"\nDRY RUN - Would send to {details['email']} ({name}):")
            print(msg_template)
        else:
            mailer(
                details['email'], 
                msg_template,
                subject="🎅 Secret Santa - Send Your Wishlist to Get Your Assignment!"
            )
            print(f"✉️  Sent wishlist request to {name} ({details['email']})")
    
    if not dry_run:
        print("\n✅ All wishlist requests sent!")
        print("Run check_wishlists() to see who has responded.")


def check_wishlists(dry_run=True, game_state_file="santa_game_state.json"):
    """
    Check for wishlist replies and update game state.
    Does NOT send assignments - use send_assignments() for that.
    
    :param dry_run: if True, doesn't mark emails as read or update state
    :param game_state_file: path to game state JSON
    :return: game_state with updated wishlist info
    """
    # Load game state
    game_state = load_game_state(game_state_file)
    if not game_state:
        return None
    
    # Connect to Gmail IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_username, gmail_app_password)
    mail.select("inbox")
    
    # Search for unread emails with "Secret Santa" in subject
    status, messages = mail.search(None, 'UNSEEN SUBJECT "Secret Santa"')
    
    if status != "OK":
        print("No messages found!")
        mail.close()
        mail.logout()
        return game_state
    
    email_ids = messages[0].split()
    
    if not email_ids:
        print("No new wishlist emails found.")
        mail.close()
        mail.logout()
        return game_state
    
    print(f"Found {len(email_ids)} unread Secret Santa emails\n")
    
    new_wishlists = 0
    
    for email_id in email_ids:
        # Fetch the email
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        if status != "OK":
            print(f"Error fetching email {email_id}")
            continue
        
        # Parse email
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Get sender
                from_header = msg.get("From")
                if "<" in from_header:
                    sender_email = from_header.split("<")[1].split(">")[0].strip()
                else:
                    sender_email = from_header.strip()
                
                # Get email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                
                # Find who this person is
                sender_name = None
                for name, details in game_state['participants'].items():
                    if details['email'].lower() == sender_email.lower():
                        sender_name = name
                        break
                
                if not sender_name:
                    print(f"⚠️  Email from {sender_email} not in participants list. Skipping.")
                    continue
                
                # Check if they already sent wishlist
                if game_state['participants'][sender_name]['wishlist_received']:
                    print(f"ℹ️  {sender_name} already sent their wishlist. Skipping.")
                    if not dry_run:
                        mail.store(email_id, '+FLAGS', '\\Seen')
                    continue
                
                # New wishlist!
                new_wishlists += 1
                print(f"🎁 NEW WISHLIST from {sender_name}:")
                print(f"   Email: {sender_email}")
                print(f"   Content preview: {body[:100]}...")
                print()
                
                if not dry_run:
                    # Update game state
                    game_state['participants'][sender_name]['wishlist_received'] = True
                    game_state['participants'][sender_name]['wishlist_content'] = body
                    
                    # Save updated state
                    with open(game_state_file, 'w') as f:
                        json.dump(game_state, f, indent=2)
                    
                    # Mark as read
                    mail.store(email_id, '+FLAGS', '\\Seen')
    
    mail.close()
    mail.logout()
    
    if dry_run and new_wishlists > 0:
        print(f"⚠️  DRY RUN - {new_wishlists} wishlists found but not saved.")
        print("   Run with dry_run=False to actually save them.\n")
    elif new_wishlists > 0:
        print(f"✅ Processed {new_wishlists} new wishlist(s)!\n")
    
    return game_state


def check_status(game_state_file="santa_game_state.json"):
    """
    Check who has and hasn't sent their wishlist.
    Does NOT reveal assignments!
    
    :param game_state_file: path to game state JSON
    :return: None
    """
    game_state = load_game_state(game_state_file)
    if not game_state:
        return
    
    received = []
    pending = []
    
    for name, details in game_state['participants'].items():
        if details['wishlist_received']:
            received.append(name)
        else:
            pending.append(name)
    
    print("=" * 60)
    print("SECRET SANTA STATUS")
    print("=" * 60)
    print(f"\n✅ WISHLISTS RECEIVED ({len(received)}/{len(game_state['participants'])})")
    for name in received:
        email = game_state['participants'][name]['email']
        print(f"   • {name.capitalize()} ({email})")
    
    if pending:
        print(f"\n⏳ WAITING FOR WISHLISTS ({len(pending)})")
        for name in pending:
            email = game_state['participants'][name]['email']
            print(f"   • {name.capitalize()} ({email})")
    else:
        print("\n🎉 ALL WISHLISTS RECEIVED!")
        print("   Ready to send assignments! Run: send_assignments()")
    
    print("\n" + "=" * 60)


def send_assignments(dry_run=True, game_state_file="santa_game_state.json"):
    """
    Send Secret Santa assignments to everyone who has submitted a wishlist.
    Can send to everyone at once (if all wishlists received) or individually as they come in.
    
    :param dry_run: if True, doesn't send real emails
    :param game_state_file: path to game state JSON
    :return: None
    """
    game_state = load_game_state(game_state_file)
    if not game_state:
        return
    
    # Count how many have submitted wishlists
    total = len(game_state['participants'])
    received = sum(1 for p in game_state['participants'].values() if p['wishlist_received'])
    
    if received < total:
        print(f"⚠️  WARNING: Only {received}/{total} people have sent wishlists.")
        print("   Some people won't get assignments yet.")
        response = input("   Send assignments anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled. Run check_status() to see who's missing.")
            return
    
    print("\n" + "=" * 60)
    print("SENDING ASSIGNMENTS")
    print("=" * 60)
    
    assignments_sent = 0
    
    for giver_name, receiver_name in game_state['assignments'].items():
        giver_details = game_state['participants'][giver_name]
        receiver_details = game_state['participants'][receiver_name]
        
        # Only send if giver has submitted wishlist and hasn't received assignment yet
        if not giver_details['wishlist_received']:
            print(f"⏭️  Skipping {giver_name} - hasn't sent wishlist yet")
            continue
        
        if giver_details['assignment_sent']:
            print(f"⏭️  Skipping {giver_name} - already received assignment")
            continue
        
        # Only send if receiver has submitted wishlist
        if not receiver_details['wishlist_received']:
            print(f"⏭️  Skipping {giver_name} - their recipient ({receiver_name}) hasn't sent wishlist yet")
            continue
        
        # Compose assignment email
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
        
        if dry_run:
            print(f"\n{'='*60}")
            print(f"DRY RUN - Would send to {giver_name} ({giver_details['email']}):")
            print(msg)
            print(f"{'='*60}\n")
        else:
            mailer(
                giver_details['email'],
                msg,
                subject=f"🎅 Your Secret Santa Assignment: {receiver_name.capitalize()}!"
            )
            print(f"✉️  Sent assignment to {giver_name} ({giver_details['email']})")
            
            # Mark as sent
            game_state['participants'][giver_name]['assignment_sent'] = True
            assignments_sent += 1
    
    if not dry_run and assignments_sent > 0:
        # Save updated state
        with open(game_state_file, 'w') as f:
            json.dump(game_state, f, indent=2)
        print(f"\n✅ Sent {assignments_sent} assignment(s)!")
    elif dry_run:
        print(f"\n⚠️  DRY RUN - No emails actually sent.")
    elif assignments_sent == 0:
        print(f"\n⚠️  No new assignments to send.")


def setup_secret_santa(dry_run=True):
    """
    Initial setup: Create assignments and send wishlist request emails.
    
    :param dry_run: if True, doesn't send real emails
    :return: None
    """
    # Configure your participants here
    participants = {
        'alice': {'email': 'alice@example.com'},
        'bob': {'email': 'bob@example.com'},
        'chris': {'email': 'chris@example.com'},
        'dina': {'email': 'dina@example.com'},
    }

    # Optional: block certain pairings (e.g., couples)
    undesired_matches = (
        # {'alice', 'bob'},  # Uncomment to prevent Alice and Bob from being matched
    )

    print("=" * 60)
    print("SECRET SANTA SETUP")
    print("=" * 60)
    print(f"\nParticipants: {len(participants)}")
    for name in participants.keys():
        print(f"  • {name.capitalize()}")
    print()

    # Make assignments
    matches = False
    while not matches:
        matches = make_matches(participants, blocked_matches=undesired_matches)
    
    if matches:
        print("✅ Assignments created!")
        if dry_run:
            print("\nAssignments (DRY RUN - for your eyes only):")
            for giver, receiver in matches:
                print(f"   {giver.capitalize()} → {receiver.capitalize()}")
        print()
        
        # Save game state
        save_game_state(matches, participants)
        
        # Send initial wishlist requests
        send_initial_requests(participants, dry_run=dry_run)
        
        if not dry_run:
            print("\n" + "=" * 60)
            print("NEXT STEPS")
            print("=" * 60)
            print("1. Wait for participants to reply with wishlists")
            print("2. Run: check_status() to see who has responded")
            print("3. Run: check_wishlists(dry_run=False) to collect wishlists")
            print("4. Run: send_assignments(dry_run=False) when ready!")
    else:
        print("❌ Could not make matches from list!")


if __name__ == '__main__':
    # STEP 1: Initial setup (run once)
    # This creates assignments and sends wishlist requests
    setup_secret_santa(dry_run=True)
    
    # After testing, run with dry_run=False:
    # setup_secret_santa(dry_run=False)
    
    # STEP 2: Check who has responded (run anytime)
    # check_status()
    
    # STEP 3: Collect wishlists (run daily)
    # check_wishlists(dry_run=True)   # test first
    # check_wishlists(dry_run=False)  # actually collect
    
    # STEP 4: Send assignments when ready
    # send_assignments(dry_run=True)   # test first
    # send_assignments(dry_run=False)  # actually send
