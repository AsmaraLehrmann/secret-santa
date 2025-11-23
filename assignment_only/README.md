# Pure python santa randomizer for christmas cheer 🎅

### Requirements

- Python >= 3.6
- A throwaway gmail account
- List of participant email addresses

### Gmail setup

1. Create a new gmail account that will send the emails
2. Go to google account >> 2-step verification >> turn on 2-step verification
3. Setup whatever 2FA you prefer
4. Create an app password https://myaccount.google.com/u/7/apppasswords explained at https://support.google.com/accounts/answer/185833?hl=en
5. Copy the gmail address and 16 character app password into a file called `email_auth.json` in this directory, with the following structure

```json
{"gmail_username":  "you@gmail.com",
"gmail_app_password":  "16-char-app-password"}
```

### Run the script

1. Start by sending a test email to check that it is working with the `mailer` function e.g.

```python
mailer("your-regular-email@domain.org", "hi me, this is a test from the santabot")
```

2. Fill in the particpants dict in `secret_santa` with your participant **names**, **emails** and (optional) **wishlists**. Note from the examples that **wishlists** are not required. Bonus: check out the `undesired_matches` option if you wish to tip the scales a little.
3. Do a dry run, that is, run `secret_santa` with **dry_run** set to True to print out who will be sent emails and what those emails will say
4. Edit the email template in variable **msg** in `mail_invites` to say what you want to partipants
5. Once you are happy the matching is working as expected and the format of the message says what you want, run `secret_santa` with **dry_run=False** to send real emails to participants
6. (optional) to keep yourself honest, delete the outfolder of your gmail account to save the temptation to peak. Better hope you got the setup right though!
