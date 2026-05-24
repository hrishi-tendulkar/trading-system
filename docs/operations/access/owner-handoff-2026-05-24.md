# Owner Handoff: What You Need To Give Me

This is the short version for tomorrow.

## What I already did

- built the app and jobs scaffold
- added Railway and Supabase project config in the repo
- created the first database migration in `supabase/migrations/`
- applied the first database migration to the live Supabase project
- stored the real FMP key and live database connection privately for setup
- used dummy placeholders only where secrets are still missing

## What I need from you

### 1. Shared site password

You choose one password that both you and your wife will use for the site.

I will turn it into a secure hash and store only the hash in Railway.

### 2. OpenAI API key

I need the real `OPENAI_API_KEY`.

### 3. SEC user-agent identity

I need the text we will send to SEC EDGAR.

Use this format:

`Your Name your-email@example.com`

## Fastest way to hand these to me

Send me a message tomorrow with:

1. the shared site password
2. the OpenAI API key
3. the SEC user-agent string

Then I can replace the dummy values and finish the real wiring.

## Optional if you want me to be even faster

Because the database password and FMP key were pasted into chat, it is a good idea to rotate them after final setup is complete.
