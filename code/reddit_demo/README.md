# Reddit Extraction Pipeline

## Purpose

Extracts state-subreddit posts and comments from PullPush API for use
as a modern public discourse corpus (2011–present) in the gender bias
state-year panel. Greenlit by Gineete as a corpus source.

## Source

- **PullPush API** (https://api.pullpush.io)
- Community successor to Pushshift
- Coverage: ~2011–present
- No API key required, no authentication

## Current extraction

| Period | States | Posts | Comments | Total |
|---|---|---|---|---|
| January 2020 | 50 | 4,423 | 4,563 | 8,986 |

## Key technical notes

- Submissions are mostly link posts — title text is thin, selftext sparse
- Comments provide the bulk of usable text (80–95% non-deleted per state)
- Deleted/removed content (`[deleted]`, `[removed]`) filtered at extraction
- Small states (WY, VT, ND) have lower volume but still usable
- Rate limit: 1.5s delay between requests sufficient, no throttling hit
- Full historical extraction estimated 3–6 weeks background processing

## Pipeline

1. Fetch submissions per state subreddit (title + selftext)
2. Fetch comments per state subreddit (body text)
3. Filter deleted/removed content
4. Save posts and comments to separate CSVs

## Key files

| File | Description |
|---|---|
| `code/reddit_demo/reddit_jan2020.ipynb` | Extraction notebook |
| `corpus/reddit/2020-01/posts.csv` | Submissions with text |
| `corpus/reddit/2020-01/comments.csv` | Comments with text |
| `corpus/reddit/2020-01/errors.log` | Fetch errors |