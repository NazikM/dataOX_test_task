#Scraper + FastAPI project + mongodb

## To run this project you need to follow the next steps.

1) Run git compose file. This will create FastAPI and mongodb apps. **Each scrapper you need to run separately**.
    >docker compose up
2) If scrappers are not working, run every separately:
    > docker build .

    > docker run --rm <image_id>