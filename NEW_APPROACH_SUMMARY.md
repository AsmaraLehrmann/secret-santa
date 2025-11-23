# 🎅 NEW APPROACH: Wishlist-Gated Secret Santa

Based on your updated requirements, I've created a completely new version!

## What's Different?

### Your New Requirements ✅

✅ Participants must send wishlist to get assignment  
✅ Initial email asks for wishlist  
✅ Once everyone responds, reveal assignments  
✅ Assignments include the recipient's wishlist  
✅ You can check who hasn't responded WITHOUT seeing assignments  
✅ Mentions "Santa's Helper, Asmara" in final emails  

## Files You Need

### Core Scripts
1. **[santa_wishlist_gated.py](computer:///mnt/user-data/outputs/santa_wishlist_gated.py)** - Main script (use this!)
2. **[status.py](computer:///mnt/user-data/outputs/status.py)** - Safe status checker (run anytime!)
3. **[interactive_workflow.py](computer:///mnt/user-data/outputs/interactive_workflow.py)** - Guided walkthrough

### Documentation
1. **[QUICK_TEST.md](computer:///mnt/user-data/outputs/QUICK_TEST.md)** - 5-minute test with 3 emails
2. **[README_WISHLIST_GATED.md](computer:///mnt/user-data/outputs/README_WISHLIST_GATED.md)** - Complete documentation
3. **[OVERVIEW_WISHLIST_GATED.md](computer:///mnt/user-data/outputs/OVERVIEW_WISHLIST_GATED.md)** - Feature overview

## Quick Start

### 1. Setup (One Time)
```python
python santa_wishlist_gated.py
```
This sends everyone:
> Ho ho ho from the North Pole! 🎅
> 
> In order to get your Secret Santa assignment, you need to send a letter to Santa with a list of your interests or a wishlist of items under $10!

### 2. Check Status (Anytime - Safe!)
```bash
python status.py
```
Shows who responded WITHOUT revealing assignments!

### 3. Collect Wishlists (Daily)
```python
from santa_wishlist_gated import check_wishlists
check_wishlists(dry_run=False)
```

### 4. Send Assignments (When Ready)
```python
from santa_wishlist_gated import send_assignments
send_assignments(dry_run=False)
```
Everyone gets:
> Ho ho ho! 🎅
> 
> You are the Secret Santa for Bob! Don't tell anyone!
>
> They have sent the following message to the North Pole:
> 
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> I'd love coffee, books, or chocolate!
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>
> If you have any questions, please reach out to Santa's Helper, Asmara.

## The Magic Feature: Safe Status Checking! ✨

This is the key feature you asked for:

```bash
python status.py
```

Output:
```
============================================================
SECRET SANTA STATUS
============================================================

✅ WISHLISTS RECEIVED (2/5)
   • Alice (alice@example.com)
   • Bob (bob@example.com)

⏳ WAITING FOR WISHLISTS (3)
   • Chris (chris@example.com)
   • Dina (dina@example.com)
   • Evan (evan@example.com)
============================================================
```

**You can run this as many times as you want without spoiling assignments!**

## Testing with Your 3 Emails

Perfect for testing! See [QUICK_TEST.md](computer:///mnt/user-data/outputs/QUICK_TEST.md):

1. Create bot Gmail
2. Configure 3 test emails in script
3. Run setup
4. Reply to wishlist requests
5. Check status
6. Collect wishlists  
7. Send assignments
8. Done!

**Takes 5 minutes total.**

## Computer Requirements

**Does my computer need to be on?** NO!

- 30 seconds for initial setup (once)
- 5 seconds/day to check wishlists (for ~1 week)
- 30 seconds to send assignments (once)

**Total: 5 minutes over a week**

## Configuration

Edit `santa_wishlist_gated.py`, find `setup_secret_santa()`:

```python
participants = {
    'alice': {'email': 'alice@example.com'},
    'bob': {'email': 'bob@example.com'},
    'chris': {'email': 'chris@example.com'},
}

# Optional: prevent couples from being matched
undesired_matches = (
    {'alice', 'bob'},
)
```

## What Gets Saved?

The script creates `santa_game_state.json`:
```json
{
  "assignments": {
    "alice": "bob",
    "bob": "chris",
    "chris": "alice"
  },
  "participants": {
    "alice": {
      "email": "alice@example.com",
      "wishlist_received": true,
      "wishlist_content": "I'd love coffee...",
      "assignment_sent": false
    },
    ...
  }
}
```

**Keep this file private!** It has all the assignments.

## Command Cheat Sheet

```bash
# Setup (once)
python santa_wishlist_gated.py

# Check status (anytime - safe!)
python status.py

# Or use Python:
from santa_wishlist_gated import *

# Check status
check_status()

# Collect wishlists  
check_wishlists(dry_run=True)   # test
check_wishlists(dry_run=False)  # collect

# Send assignments
send_assignments(dry_run=True)   # test
send_assignments(dry_run=False)  # send

# Or use interactive mode
python interactive_workflow.py
```

## Workflow Example

```
Day 1: Setup
  → python santa_wishlist_gated.py
  → Everyone gets wishlist request

Day 2-7: Daily monitoring
  → python status.py (check who responded)
  → check_wishlists(dry_run=False) (collect new ones)
  → Send reminders to slow people!

Day 8: Everyone responded!
  → python status.py (confirm 5/5 received)
  → send_assignments(dry_run=False)
  → Everyone gets their assignment!

Done! 🎄
```

## Key Features

✅ Wishlist required to get assignment  
✅ Safe status checking (no spoilers!)  
✅ Assignment + wishlist in single email  
✅ Mentions "Santa's Helper, Asmara"  
✅ Can send partial assignments as people respond  
✅ Dry-run mode for everything  
✅ Complete anonymity maintained  

## Which File to Start With?

- **Testing?** → [QUICK_TEST.md](computer:///mnt/user-data/outputs/QUICK_TEST.md)
- **Learning?** → [OVERVIEW_WISHLIST_GATED.md](computer:///mnt/user-data/outputs/OVERVIEW_WISHLIST_GATED.md)
- **Reference?** → [README_WISHLIST_GATED.md](computer:///mnt/user-data/outputs/README_WISHLIST_GATED.md)
- **Just do it?** → `python interactive_workflow.py`

## Comparison: Old vs New Approach

| Feature | Original Request | New Approach |
|---------|------------------|--------------|
| Get assignment | Immediate | After sending wishlist ✅ |
| Wishlists | Forwarded separately | Embedded in assignment ✅ |
| Status check | Would reveal assignments | Safe checker! ✅ |
| Email flow | 2 emails per person | 2 emails per person |
| Participation | Optional | Required ✅ |
| Mentions Asmara | No | Yes! ✅ |

## Ready to Go!

Start with [QUICK_TEST.md](computer:///mnt/user-data/outputs/QUICK_TEST.md) to test with your 3 emails, then use it for real!

The key feature is `status.py` - run it anytime to check progress without spoiling the surprise! 🎅
