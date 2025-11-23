# Quick Testing Guide - Wishlist-Gated Secret Santa

## Test with Your 3 Emails (5 minutes)

### What You Need
- Your 3 personal email addresses
- 1 new Gmail account as the "bot"

### Step-by-Step

#### 1. Create Bot Gmail (2 minutes)
```
1. Go to gmail.com
2. Create account: yoursanta2024@gmail.com
3. Settings → Security → 2-Step Verification → Enable
4. Create app password (save it!)
```

#### 2. Create email_auth.json (30 seconds)
```json
{
  "gmail_username": "yoursanta2024@gmail.com",
  "gmail_app_password": "your 16 char password"
}
```

#### 3. Edit Script (30 seconds)
In `santa_wishlist_gated.py`, change participants:

```python
participants = {
    'alice': {'email': 'your_email1@gmail.com'},
    'bob': {'email': 'your_email2@gmail.com'},
    'chris': {'email': 'your_email3@gmail.com'},
}
```

At the bottom, change:
```python
setup_secret_santa(dry_run=False)  # Change True to False
```

#### 4. Send Wishlist Requests (30 seconds)
```bash
python santa_wishlist_gated.py
```

#### 5. Reply with Wishlists (1 minute)
Check all 3 of your email inboxes. Each has an email:
"Secret Santa - Send Your Wishlist to Get Your Assignment!"

Reply to each with something like:
- Email 1: "I'd love coffee, books, or chocolate!"
- Email 2: "Board games or art supplies please!"
- Email 3: "Snacks, tea, or fun socks!"

**Important**: REPLY to the email, don't create new ones!

#### 6. Check Status (5 seconds)
```bash
python status.py
```

You'll see:
```
✅ WISHLISTS RECEIVED (0/3)

⏳ WAITING FOR WISHLISTS (3)
   • Alice
   • Bob  
   • Chris
```

#### 7. Collect Wishlists (5 seconds)
```python
# Collect wishlists (daily)
python collect_safe.py
```

Output:
```
🎁 NEW WISHLIST from alice
🎁 NEW WISHLIST from bob
🎁 NEW WISHLIST from chris
✅ Processed 3 new wishlist(s)!
```

#### 8. Check Status Again (5 seconds)
```bash
python status.py
```

Now see:
```
✅ WISHLISTS RECEIVED (3/3)
   • Alice
   • Bob
   • Chris

🎉 ALL WISHLISTS RECEIVED!
   Ready to send assignments!
```

#### 9. Send Assignments (Test First) (5 seconds)
```python
from santa_wishlist_gated import send_assignments
send_assignments(dry_run=True)
```

This shows you what WOULD be sent. Review it!

#### 10. Send Assignments for Real (5 seconds)
```python
send_assignments(dry_run=False)
```

#### 11. Check Your Inboxes! (1 minute)
Each of your 3 emails should now have an assignment like:

> Ho ho ho! 🎅
> 
> You are the Secret Santa for Bob! Don't tell anyone!
>
> They have sent the following message to the North Pole:
> 
> Board games or art supplies please!

## ✅ Test Complete!

You've successfully tested the entire flow!

## What Each Function Does

### `setup_secret_santa(dry_run=False)`
- Creates random assignments
- Saves to santa_game_state.json
- Sends wishlist request emails

### `check_status()`
- Shows who responded
- Does NOT reveal assignments!
- Safe to run anytime

### `check_wishlists(dry_run=False)`
- Checks Gmail for replies
- Saves wishlist contents
- Marks emails as read

### `send_assignments(dry_run=False)`
- Sends assignment + wishlist to each person
- Only sends if both people submitted wishlists
- Marks assignments as sent

## Quick Command Cheat Sheet

```bash
# Check status (safe!)
python status.py

# Or in Python:
from santa_wishlist_gated import *

# 1. Initial setup
setup_secret_santa(dry_run=True)   # test
setup_secret_santa(dry_run=False)  # send

# 2. Check status (anytime)
check_status()

# 3. Collect wishlists (daily)
check_wishlists(dry_run=True)   # test
check_wishlists(dry_run=False)  # collect

# 4. Send assignments (when ready)
send_assignments(dry_run=True)   # test
send_assignments(dry_run=False)  # send
```

## Real Use After Testing

1. Edit `participants` with real names/emails
2. Run `setup_secret_santa(dry_run=False)`
3. Daily: `check_status()` and `check_wishlists(dry_run=False)`
4. When ready: `send_assignments(dry_run=False)`

## Troubleshooting Test

### Emails not arriving?
- Check spam folders
- Verify email_auth.json is correct
- Make sure 2FA and app password are set up

### Wishlists not collected?
- Did you REPLY? (not new email)
- Subject must have "Secret Santa"
- Run `check_wishlists(dry_run=True)` first to debug

### Status shows 0/3?
- You need to run `check_wishlists(dry_run=False)` first!
- `status.py` just reads santa_game_state.json

That's it! Now you're ready to use it for real! 🎅
