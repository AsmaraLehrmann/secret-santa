# Secret Santa - Wishlist-Gated Version 🎅

## Overview

This version requires participants to send their wishlist BEFORE they receive their Secret Santa assignment. This ensures everyone participates!

## How It Works

### The Process

```
1. You run setup → Everyone gets: "Send wishlist to get assignment!"
                    ↓
2. People reply with wishlists
                    ↓
3. You check status (without seeing assignments!)
                    ↓
4. You collect wishlists
                    ↓
5. Once everyone responds → Send assignments with embedded wishlists!
```

### Example Email Flow

**Initial Email (to everyone):**
> Ho ho ho from the North Pole! 🎅
> 
> In order to get your Secret Santa assignment, you need to send a letter to Santa with a list of your interests or a wishlist of items under $10!
> 
> Simply REPLY to this email with your wishlist...

**Person replies:**
> I'd love coffee, books about space, or dark chocolate!

**Assignment Email (after everyone responds):**
> Ho ho ho! 🎅
>
> You are the Secret Santa for Bob! Don't tell anyone!
>
> They have sent the following message to the North Pole:
> 
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> I'd love coffee, books about space, or dark chocolate!
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>
> If you have any questions, reach out to Santa's Helper, Asmara.

## Key Features

✅ **Participation Required**: No assignment without wishlist  
✅ **Status Checker**: See who responded without spoiling assignments  
✅ **Single Clean Email**: Assignment + wishlist in one message  
✅ **Flexible Timing**: Send assignments all at once or as people respond  
✅ **Same Security**: Bot handles all email monitoring  

## Files Included

### Core Files
- **santa_wishlist_gated.py** - Main script with all functionality
- **status.py** - Quick status checker (safe to run anytime!)

### Documentation
- **README_WISHLIST_GATED.md** - Complete documentation
- **QUICK_TEST.md** - 5-minute testing guide with 3 emails

## Quick Commands

```bash
# Setup (run once)
python santa_wishlist_gated.py

# Check status (anytime - safe!)
python status.py

# Daily: collect wishlists
python -c "from santa_wishlist_gated import check_wishlists; check_wishlists(dry_run=False)"

# When ready: send assignments
python -c "from santa_wishlist_gated import send_assignments; send_assignments(dry_run=False)"
```

## Status Checker - Your Safe Tool!

The `status.py` script lets you check progress WITHOUT revealing assignments:

```
============================================================
SECRET SANTA STATUS
============================================================

✅ WISHLISTS RECEIVED (3/5)
   • Alice (alice@example.com)
   • Bob (bob@example.com)
   • Chris (chris@example.com)

⏳ WAITING FOR WISHLISTS (2)
   • Dina (dina@example.com)
   • Evan (evan@example.com)
============================================================
```

**You can run this as many times as you want!** It never shows assignments.

## Testing with 3 Emails

See **QUICK_TEST.md** for a complete 5-minute walkthrough.

Summary:
1. Create bot Gmail
2. Configure 3 test emails
3. Run setup
4. Reply with wishlists
5. Check status
6. Collect wishlists
7. Send assignments
8. Check results!

## Typical Timeline

**Day 1**: Run `setup_secret_santa()` - wishlist requests sent  
**Day 2-7**: Daily check with `status.py` and `check_wishlists()`  
**Day 8**: All wishlists in! Run `send_assignments()`  
**Done!**: Everyone has assignments with wishlists  

## Computer Requirements

**Does my computer need to be on?** NO!

- 30 seconds to send initial requests (once)
- 5 seconds/day to check wishlists (for ~1 week)
- 30 seconds to send assignments (once)

**Total: 5 minutes over a week**

## Configuration

Edit `santa_wishlist_gated.py`:

```python
participants = {
    'alice': {'email': 'alice@example.com'},
    'bob': {'email': 'bob@example.com'},
    'chris': {'email': 'chris@example.com'},
}

# Optional: prevent certain pairings
undesired_matches = (
    {'alice', 'bob'},  # couples, roommates, etc
)
```

## Advantages Over Original Approach

| Feature | Original | Wishlist-Gated |
|---------|----------|----------------|
| Wishlists | Optional, manual | Required, automatic |
| Participation | Hope everyone joins | Guaranteed by design |
| Status Check | Can't check safely | `status.py` anytime! |
| Email Count | 2 per person | 2 per person |
| Wishlist Format | Separate email | Embedded in assignment |
| Anonymity | ✅ Yes | ✅ Yes |

## When to Use This Version

✅ You want guaranteed participation  
✅ You want to track who's responded  
✅ You prefer assignments with embedded wishlists  
✅ You want to send reminders to slow responders  

## Getting Started

1. **Read**: Start with **README_WISHLIST_GATED.md**
2. **Test**: Follow **QUICK_TEST.md** with 3 emails
3. **Use**: Configure real participants and run!

## Need Help?

- **Testing?** → QUICK_TEST.md
- **Full docs?** → README_WISHLIST_GATED.md  
- **Status check?** → Just run `python status.py`
- **Confused?** → Read the "How It Works" section above

Ready to ensure everyone participates? Start with **QUICK_TEST.md**! 🎅🎄
