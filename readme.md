# Scraper + FastAPI project + mongodb

## To run this project you need to follow the next steps.

1) Clone this repo.
    `git clone https://github.com/NazikM/dataOX_test_task`
2) Add your proxy to a list. In scraper/proxy/list.txt

    Format for proxy list: http://username:pass@ip:port
    
    The AUTOTHROTTLE options in settings.py are set for 100 proxies.  If you'd like to use less or more you should change these params.
    
>    Note: You can get 10 free proxy with good speed on webshare.io or buy 100 proxies for 1$
    
2) Run your Docker Desktop.
3) Run git compose file. This will everything you need inside your docker.
    `docker-compose up`
