from fastapi import FastAPI, HTTPException
from scrapfly import ScrapflyClient, ScrapeConfig
from dotenv import load_dotenv
import os

load_dotenv() 
app = FastAPI()

SCRAPFLY_KEY = os.getenv("SCRAPFLY_KEY")
PROFILE_URL:str = os.getenv("PROFILE_URL")
print("SCRAPFLY_KEY:", SCRAPFLY_KEY)
print("PROFILE_URL:", PROFILE_URL)

client = ScrapflyClient(key=SCRAPFLY_KEY)

@app.get("/scrapeProfile")
async def scrape_profile():
	try:
		result = client.scrape(ScrapeConfig(
			url=PROFILE_URL,
			asp=True,
			country="US", 
			proxy_pool="public_residential_pool", 
			# render_js=True
		))

		html_content = result.content

		start = html_content.find('<title>')
		end = html_content.find('</title>', start)
		title = html_content[start + 7:end].strip()

		return {"profile_url": PROFILE_URL, "title": title}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	

@app.get("/health")
async def health_check():
    return {"status": "ok"}