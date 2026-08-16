# Database Schema

## urls
- id
- original_url
- short_code (UNIQUE)
- created_at
- updated_at
- click_count
- last_clicked_at

## click_events
- id
- url_id (FK urls.id)
- clicked_at
- user_agent
- referrer
