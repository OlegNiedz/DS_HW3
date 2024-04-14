pip install scrapy
poetry add scrapy
scrapy start project scrapy_project
cd scrapy_project                                   створення проекту

scrapy genspider get_urls index.minfin.com.ua       створення заготовки павука
scrapy crawl get_urls                               запуск павука
scrapy crawl get_losses -O links.json                запис у файл               

scrapy genspider get_losses index.minfin.com.ua     створення заготовки павука
scrapy crawl get_losses                             запуск павука
scrapy crawl get_losses -O losses.json              запис у файл 