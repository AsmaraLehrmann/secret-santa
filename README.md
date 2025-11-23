# 🎅 Secret Santa Email Automation

Automate your Secret Santa gift exchange with randomized assignments and email delivery! Choose between two versions based on your needs.

Originally forked from [callumrollo/secret-santa](https://github.com/callumrollo/secret-santa) and enhanced with wishlist management features.

## 📋 Two Versions Available

### Version 1: Classic Assignment 
**Best for:** Traditional Secret Santa where you want immediate assignments.

- ✅ Random Secret Santa assignments sent immediately
- ✅ Participants get their assignment right away
- 📁 Files: /assignment_only

### Version 2: Wishlist-Gated Assignment 
**Best for:** Ensuring everyone participates and provides gift ideas.

- ✅ Participants must send wishlist to receive assignment
- ✅ Safe status checking (see who responded without spoiling assignments)
- ✅ Single email with assignment + wishlist included
- ✅ Guaranteed participation from everyone
- 📁 Files: /assignmentANDwishlist

---

## 🚀 Quick Start

### Requirements
- Python 3.6+
- Gmail account with app password
- List of participant names and emails

### Gmail Setup (Both Versions)

1. **Create a Gmail account** for the bot (e.g., `santabot2024@gmail.com`)
2. **Enable 2-step verification**
   - Go to Google Account → Security → 2-Step Verification
3. **Create app password**
   - Visit: https://myaccount.google.com/apppasswords
   - Generate password (save it!)
4. **Create `email_auth.json`**:
```json
{
  "gmail_username": "santabot2024@gmail.com",
  "gmail_app_password": "your 16 char password"
}
```

---

## Version 1: Classic Assignment

### How It Works
1. Creates random Secret Santa assignments
2. Sends everyone their assignment immediately

---

## Version 2: Wishlist-Gated 

### How It Works
1. Creates random Secret Santa assignments (kept secret)
2. Sends wishlist requests to everyone
3. Participants reply with their wishlists
4. Once everyone replies, assignments are sent with wishlists included
5. You can check status without spoiling assignments!

### Usage

#### Step 1: Setup
```python
# Edit participants in santa_wishlist_gated.py
participants = {
    'alice': {'email': 'alice@example.com'},
    'bob': {'email': 'bob@example.com'},
    'chris': {'email': 'chris@example.com'},
}

# Run setup (sends wishlist requests)
python santa_wishlist_gated.py
```

#### Step 2: Check Status (Safe!)
```bash
# See who has responded WITHOUT revealing assignments
python status.py
```

Output:
```
============================================================
SECRET SANTA STATUS
============================================================
✅ WISHLISTS RECEIVED (2/3)
   • Alice (alice@example.com)
   • Bob (bob@example.com)

⏳ WAITING FOR WISHLISTS (1)
   • Chris (chris@example.com)
============================================================
```

#### Step 3: Collect Wishlists
```python
# Run daily to collect new wishlist replies
python3 -c "from santa_wishlist_gated import check_wishlists; check_wishlists(dry_run=False)"
```

#### Step 4: Send Assignments
```python
# When everyone has responded, send assignments
python3 -c "from santa_wishlist_gated import send_assignments; send_assignments(dry_run=False)"
```

### Email Flow (Version 2)

**Initial Email (to everyone):**
```
Ho ho ho from the North Pole! 🎅

In order to get your Secret Santa assignment, you need to send a letter to Santa 
with a list of your interests or a wishlist of items under $10!

Simply REPLY to this email with your wishlist...
```

**Participant Replies:**
```
I'd love coffee, books about space, or dark chocolate!
```

**Assignment Email (sent after all wishlists received):**
```
Ho ho ho! 🎅

You are the Secret Santa for Bob! Don't tell anyone!

They have sent the following message to the North Pole:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I'd love coffee, books about space, or dark chocolate!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have any questions, please reach out to Santa's Helper, Asmara.
```

---

## 🧪 Testing with 3 Personal Emails

Both versions can be tested with your own email addresses! See `QUICK_TEST.md` for step-by-step instructions.

**Quick test setup:**
1. Create 1 bot Gmail account
2. Use 3 of your personal emails as participants
3. Run the script
4. Check your inboxes and reply
5. Verify the entire flow works!

---

## ⚙️ Configuration

### Participants
Edit the `participants` dictionary in either script:

```python
participants = {
    'alice': {'email': 'alice@example.com'},
    'bob': {'email': 'bob@example.com'},
    'chris': {'email': 'chris@example.com'},
}
```

### Block Certain Pairings
Prevent couples, roommates, etc. from being matched:

```python
undesired_matches = (
    {'alice', 'bob'},     # Alice and Bob won't be matched
    {'chris', 'dina'},    # Chris and Dina won't be matched
)
```

---

## 📊 Comparison Table

| Feature | Version 1 (Classic) | Version 2 (Wishlist-Gated) |
|---------|--------------------|-----------------------------|
| Immediate assignments | ✅ Yes | ❌ No - must send wishlist first |
| Wishlist management | ❌ Not available | Required, integrated |
| Status checking | ❌ Not available | ✅ Yes - safe to use! |
| Guaranteed participation | ❌ No | ✅ Yes |
| Assignment + wishlist | Separate emails | Single email |
| Best for | Traditional exchange | Ensuring participation |


---

## 💻 Computer Requirements

**Does my computer need to be on the whole time?** 

**NO!** Both versions require minimal computer time:

- **30 seconds** to send initial emails (once)
- **5 seconds/day** to check for replies (for ~1 week)
- **30 seconds** to send assignments (once)

**Total: ~5 minutes over the entire event**

Your computer can be off 99.9% of the time!

---

## 📁 Repository Structure

```
secret-santa/
├── Version 1 (Classic Assignment)
│   ├── santa_send_enhanced.py      # Main script
│   ├── check_wishlists.py          # Wishlist forwarding helper
│   └── README_ENHANCED.md          # Full documentation
│
├── Version 2 (Wishlist-Gated) - Recommended
│   ├── santa_wishlist_gated.py     # Main script
│   ├── status.py                   # Safe status checker
│   ├── interactive_workflow.py     # Guided walkthrough
│   ├── README_WISHLIST_GATED.md    # Full documentation
│   └── QUICK_TEST.md              # Testing guide
│
└── email_auth.json                # Your Gmail credentials (create this)
```

---

## 🎯 Which Version Should I Use?

### Choose Version 1 (Classic) if:
- ✅ You want traditional Secret Santa flow
- ✅ You trust everyone to participate
- ✅ You want immediate assignments

### Choose Version 2 (Wishlist-Gated) if:
- ✅ You want guaranteed participation
- ✅ You want to track who's responded
- ✅ You prefer assignments with wishlists included
- ✅ You want safe status checking without spoilers


---

## 🛠️ Troubleshooting

### Emails Not Arriving
- Check spam/junk folders
- Verify `email_auth.json` format is correct (use double quotes)
- Ensure 2FA and app password are set up
- **Outlook users**: Add bot email to safe senders list

### "JSONDecodeError"
Your `email_auth.json` has formatting issues. It should look exactly like:
```json
{
  "gmail_username": "email@gmail.com",
  "gmail_app_password": "password here"
}
```
Use double quotes, not single quotes!

### Wishlists Not Forwarding (Version 1)
- Make sure people REPLIED to the email (not new email)
- Subject must contain "Secret Santa"
- Run with `dry_run=True` first to debug

### Can't See Who Responded (Version 2)
- Run `python status.py` - this is safe!
- Make sure you ran `check_wishlists(dry_run=False)` first
- Check `santa_game_state.json` exists

---

## 🔒 Privacy & Security

- The bot email account sees all wishlists (necessary for the system)
- Keep `email_auth.json` private (contains credentials)
- Keep `santa_assignments.json` / `santa_game_state.json` private (contains assignments)
- Participants never see each other's assignments
- Complete anonymity is maintained throughout


## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share your Secret Santa stories!

---

## 📝 License

GNU General Public License v3.0

---

## 🙏 Credits

- Original script: [callumrollo/secret-santa](https://github.com/callumrollo/secret-santa)
- Enhanced and wishlist-gated versions: Asmara Lehrmann
- Built with ❤️ for holiday gift exchanges

---

---

**Happy Secret Santa! 🎅🎄**

Questions? Check the documentation files or open an issue!
