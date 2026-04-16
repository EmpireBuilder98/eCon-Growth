# Command HVAC · Sales Portal Setup Guide

Live URL: https://econgrowth.com/internal/
Auth: Supabase (project: egofvdwrletgiwzzqalo)
Table: public.portal_access

---

## ONE-TIME SETUP

### 1. Get your Supabase anon key
- Supabase dashboard → project egofvdwrletgiwzzqalo → Settings → API
- Copy the anon/public key (starts with eyJ...)

### 2. Paste it in BOTH files
In index.html AND playbook.html, replace:
  const SUPABASE_ANON = 'YOUR_SUPABASE_ANON_KEY';

### 3. Set redirect URL in Supabase
- Supabase → Authentication → URL Configuration
- Site URL: https://econgrowth.com
- Redirect URLs: add https://econgrowth.com/internal/index.html

### 4. Push to GitHub
Upload the /internal/ folder to your repo root.

### 5. Add to root robots.txt
  Disallow: /internal/

---

## MANAGING USERS

Add a user (run in Supabase SQL Editor):

  INSERT INTO public.portal_access (email, full_name, role, company, invited_by)
  VALUES ('their@email.com', 'Their Name', 'team', 'Company Name', 'Kristopher');

Then invite them: Supabase → Authentication → Users → Invite User
They get an email to set their password.

Roles: admin (Kris + Watson), team (staff), affiliate (partners)

Remove access instantly:
  UPDATE public.portal_access SET active = false WHERE email = 'their@email.com';

See who has logged in:
  SELECT email, full_name, role, last_login, login_count, active
  FROM public.portal_access ORDER BY last_login DESC NULLS LAST;

---

## HOW IT WORKS

User hits /internal/ -> Command HVAC login screen
Two options: password OR magic link (one-click email)
Supabase checks portal_access table
active=true -> playbook.html with their name in nav
active=false or not in table -> locked out, told to contact Kris
Sign Out button ends the session

Same auth system as Command HVAC. Real JWT tokens. Legit.

---

Support: Kristopher Cravens (615) 664-9178
