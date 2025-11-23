# Secret Santa - Wishlist-Gated Assignments 🎅

A Secret Santa system where participants MUST send their wishlist before receiving their assignment. This ensures everyone participates and provides gift ideas!

## How It Works

### The Flow

1. **Setup**: You create assignments and send wishlist requests to everyone
2. **Participants Reply**: Each person replies with their wishlist
3. **You Check**: Use `status.py` to see who has responded (without seeing assignments!)
4. **Send Assignments**: Once everyone responds, reveal assignments with embedded wishlists

### Why This Approach?

✅ Ensures everyone provides a wishlist  
✅ No forgotten wishlists  
✅ No one gets their assignment without participating  
✅ You can check who's slacking without spoiling assignments  
✅ Clean, single email with assignment + wishlist together  

## Quick Start

### Requirements

- Python 3.6+
- Gmail account with app password
- List of participant names and emails

### Setup Gmail

1. Create a Gmail account (e.g., `santabot2024@gmail.com`)
2. Enable 2-step verification
3. Create app password: https://myaccount.google.com/apppasswords
4. Create `email_auth.json`:

```json
{
  "gmail_username": "santabot2024@gmail.com",
  "gmail_app_password": "abcd efgh ijkl mnop"
}
```

### Configure Participants

Edit `santa_wishlist_gated.py`, find the `setup_secret_santa()` function:

```python
participants = {
    'alice': {'email': 'alice@example.com'},
    'bob': {'email': 'bob@example.com'},
    'chris': {'email': 'chris@example.com'},
}
```

### Run Setup

```bash
# Test first
python santa_wishlist_gated.py

# Looks good? Send for real
# (Edit the file: change dry_run=False in the if __name__ block)
python santa_wishlist_gated.py
```

This sends everyone an email like:

> Ho ho ho from the North Pole! 🎅
> 
> In order to get your Secret Santa assignment, you need to send a letter to Santa with a list of your interests or a wishlist of items under $10!
> 
> Simply REPLY to this email with your wishlist...

## Daily Workflow

### Step 1: Check Who Has Responded

```bash
python status.py
```

Output:
```
============================================================
SECRET SANTA STATUS
============================================================

✅ WISHLISTS RECEIVED (2/4)
   • Alice (alice@example.com)
   • Bob (bob@example.com)

⏳ WAITING FOR WISHLISTS (2)
   • Chris (chris@example.com)
   • Dina (dina@example.com)
============================================================
```

**Note**: This does NOT show you the assignments! Just who has responded.

### Step 2: Collect New Wishlists

```python
from santa_wishlist_gated import check_wishlists

# Test first
check_wishlists(dry_run=True)

# Actually collect
check_wishlists(dry_run=False)
```

This checks your Gmail inbox for replies and saves them.

### Step 3: Send Assignments When Ready

Once everyone has responded (or you're tired of waiting):

```python
from santa_wishlist_gated import send_assignments

# Test first
send_assignments(dry_run=True)

# Actually send
send_assignments(dry_run=False)
```

Each person gets an email like:

> Ho ho ho! 🎅
>
> You are the Secret Santa for Bob! Don't tell anyone!
>
> They have sent the following message to the North Pole:
>
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> I'd love a coffee mug, a book about space, or dark chocolate!
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>
> If you have any questions, please reach out to Santa's Helper, Asmara.

## Complete Example

```python
# Day 1: Setup
from santa_wishlist_gated import setup_secret_santa
setup_secret_santa(dry_run=False)  # Send wishlist requests

# Day 2-7: Check status daily
from santa_wishlist_gated import check_status, check_wishlists
check_status()                     # See who responded
check_wishlists(dry_run=False)     # Collect new wishlists

# Day 8: Everyone responded!
from santa_wishlist_gated import send_assignments
send_assignments(dry_run=False)    # Send assignments!
```

## Features

### Partial Assignments

Don't want to wait for everyone? You can send assignments to people who have already submitted wishlists:

```python
send_assignments(dry_run=False)
```

It will:
- ✅ Send assignments to people who submitted wishlists AND whose recipient submitted
- ⏭️ Skip people who haven't submitted
- ⏭️ Skip people whose recipient hasn't submitted

### Block Certain Pairs

Don't want couples matched together?

```python
undesired_matches = (
    {'alice', 'bob'},    # Alice won't get Bob and vice versa
    {'chris', 'dina'},
)
```

### Check Status Anytime

```bash
python status.py
```

This never reveals assignments - just shows who has responded!

## File Structure

After running, you'll have:

```
secret-santa/
├── email_auth.json              # Your Gmail credentials
├── santa_wishlist_gated.py      # Main script
├── status.py                    # Quick status checker
└── santa_game_state.json        # Generated: stores everything
```

### santa_game_state.json

This file contains:
- Assignments (who buys for whom)
- Wishlist status for each person
- Wishlist contents
- Whether assignments have been sent

**Keep this private!** It has all the assignments.

## Command Reference

### Initial Setup
```python
from santa_wishlist_gated import setup_secret_santa
setup_secret_santa(dry_run=True)   # Test
setup_secret_santa(dry_run=False)  # Send for real
```

### Check Status (Safe!)
```bash
python status.py
# OR
from santa_wishlist_gated import check_status
check_status()
```

### Collect Wishlists
```python
from santa_wishlist_gated import check_wishlists
check_wishlists(dry_run=True)   # Test
check_wishlists(dry_run=False)  # Actually collect
```

### Send Assignments
```python
from santa_wishlist_gated import send_assignments
send_assignments(dry_run=True)   # Test
send_assignments(dry_run=False)  # Send for real
```

## Testing with 3 Emails

Perfect for testing! Here's how:

1. **Create 4 Gmail accounts** (3 for participants, 1 for bot)
2. **Configure**:
```python
participants = {
    'alice': {'email': 'your.email1@gmail.com'},
    'bob': {'email': 'your.email2@gmail.com'},
    'chris': {'email': 'your.email3@gmail.com'},
}
```
3. **Run setup** (sends wishlist requests)
4. **Reply** to the wishlist emails from your 3 accounts
5. **Check status**: `python status.py`
6. **Collect wishlists**: `check_wishlists(dry_run=False)`
7. **Send assignments**: `send_assignments(dry_run=False)`
8. **Check your inboxes** - everyone should have their assignment!

## Timeline Example

```
Day 1 (Monday):
  • Run setup_secret_santa(dry_run=False)
  • Everyone gets wishlist request
  
Day 2 (Tuesday):
  • 2 people reply with wishlists
  • Run check_wishlists(dry_run=False)
  • Run check_status() - see 2/4 received
  
Day 3 (Wednesday):
  • 1 more person replies
  • Run check_wishlists(dry_run=False)
  • Run check_status() - see 3/4 received
  • Send reminder to last person!
  
Day 4 (Thursday):
  • Last person replies!
  • Run check_wishlists(dry_run=False)
  • Run check_status() - see 4/4 received! 🎉
  • Run send_assignments(dry_run=False)
  • Everyone gets their assignment!

Day 25 (Christmas):
  • Gift exchange! 🎁
```

## Troubleshooting

### "No messages found"
- Make sure people REPLIED to the wishlist email (not new email)
- Check subject line contains "Secret Santa"
- Verify Gmail IMAP is enabled

### "Can't find sender in participants"
- Email addresses must match exactly
- Check for typos in participant emails

### Someone never responds
- Send them a reminder manually
- Or run `send_assignments()` without them (they won't get assignment)

### Want to resend wishlist request to someone
- Just forward them the original email
- Or manually send them an email asking to reply

### Accidentally sent assignments too early
- No undo! But you can:
  - Send updated emails manually
  - Or wait for remaining wishlists and forward them

## Privacy & Security

- The bot email sees all wishlists (necessary for the system)
- `santa_game_state.json` contains full assignments - keep it private!
- Participants never see each other's assignments
- You can check status without spoiling assignments

## Computer On/Off?

**Short answer**: NO!

- **30 seconds** to send initial requests (one time)
- **5 seconds per day** to check for wishlists (for a week)
- **30 seconds** to send assignments (one time)

**Total: ~5 minutes over a week**

Your computer can be off 99% of the time!

## Tips

- Always test with `dry_run=True` first!
- Use `status.py` frequently to avoid spoilers
- Send reminders to slow responders
- Set a deadline for wishlists
- Consider $10 limit (or adjust as needed)

## Questions?

Run `python status.py` anytime to check progress without seeing assignments!

Happy Secret Santa! 🎅🎄
