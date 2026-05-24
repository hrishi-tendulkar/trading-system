# Owner Handoff: What You Need To Give Me

This is the short version for tomorrow.

## What I already did

- built the app and jobs scaffold
- added Railway and Supabase project config in the repo
- created the first database migration in `supabase/migrations/`
- applied the first database migration to the live Supabase project
- stored the real FMP key and live database connection privately for setup
- stored the shared site password as a secure hash in Railway
- stored the final SEC user-agent value in Railway
- used dummy placeholders only where secrets are still missing

## What I need from you

### 1. OpenAI API key

I need the real `OPENAI_API_KEY`.

## Fastest way to hand these to me

Send me a message tomorrow with:

1. the OpenAI API key

Then I can replace the dummy values and finish the real wiring.

## Optional if you want me to be even faster

Because the database password and FMP key were pasted into chat, it is a good idea to rotate them after final setup is complete.
