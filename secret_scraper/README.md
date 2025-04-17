# Secret Scraper
A scrappy little tool that sniffs out links on a webpage, because who doesn’t love a good snoop?

## What’s This Thing Do?
This bad boy takes a URL you throw at it, sucks down the webpage with `requests`, chews it up with `BeautifulSoup`, and spits out every `<a>` tag’s `href` it can find. It’s raw, it’s basic, and it works—think of it as a digital link vacuum. No hidden treasures yet, just the obvious stuff on the surface.

## How to Run This Bad Boy
1. Clone the repo: `git clone https://github.com/your-username/secret_scraper.git` (swap in your actual URL, genius).
2. Install the goods: `pip install requests beautifulsoup4`.
3. Fire it up: `python secrets.py`, type a URL (like `https://www.google.com`), and watch the links roll in.  
Enter a URL, hit enter, and pray the internet doesn’t hate you today.

## Where It’s At
Version 1.0—barebones but breathing. It’s got a `try-except` net to catch some hiccups (I'll probably get more specific here later) like dead sites or typos, and it’ll print every `<a>` link it finds, one per line. No frills, no fuss. It’ll choke on JavaScript-heavy sites, but that’s a problem for future me.

## Goodies I Might Add Later
- Turn those lazy relative links (`/about`) into full, clickable URLs.  
- Hunt down “hidden” links lurking in `<script>` tags or comments—sounds sneaky, right?  
- Maybe make the output less ugly  
Future me might get ambitious/creative until I melt stackoverflow

## Under the Hood
- Python (duh).  
- `requests` for grabbing pages.  
- `BeautifulSoup` for tearing into HTML.  
Nothing fancy here folks

## Final Words
Built with some trial, error, and google searches 
