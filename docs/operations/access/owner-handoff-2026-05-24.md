# Owner Handoff: What You Need To Give Me

This is the short version for tomorrow.

## What I already did

- built the app and jobs scaffold
- added Railway and Supabase project config in the repo
- created the first database migration in `supabase/migrations/`
- used dummy placeholders anywhere secrets are still missing

## What I need from you

### 1. Shared site password

You choose one password that both you and your wife will use for the site.

I will turn it into a secure hash and store only the hash in Railway.

### 2. FMP API key

I need the real `FMP_API_KEY`.

### 3. OpenAI API key

I need the real `OPENAI_API_KEY`.

### 4. Supabase database password or connection string

I need one of these:

- the Supabase database password for project `Trading System`
- or the full `SUPABASE_DB_URL`

### 5. SEC user-agent identity

I need the text we will send to SEC EDGAR.

Use this format:

`Your Name your-email@example.com`

## Fastest way to hand these to me

Send me a message tomorrow with:

1. the shared site password
2. the FMP API key
3. the OpenAI API key
4. the Supabase DB URL or DB password
5. the SEC user-agent string

Then I can replace the dummy values and finish the real wiring.

## Optional if you want me to be even faster

If you already bought FMP and know the dashboard URL, send that too.

If you do not have FMP yet, I can still keep building local plumbing first and wire the real key after.
