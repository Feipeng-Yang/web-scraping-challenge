from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    # get the data from mongo database

    mars_news = mongo.db.mars_news.find_one()
    featured_image = mongo.db.featured_image.find_one()
    html_table_facts = mongo.db.html_table_facts.find_one()
    hemisphere_image_urls = list(mongo.db.hemisphere_image_urls.find())


    return render_template("index.html", mars_news=mars_news, featured_image=featured_image, \
        html_table_facts=html_table_facts, hemisphere_image_urls=hemisphere_image_urls)


@app.route("/scrape")
def scraper():
    # call scrape_mars to get data and upsert into the database
    # create the collections
    mars_news = mongo.db.mars_news
    featured_image = mongo.db.featured_image
    html_table_facts = mongo.db.html_table_facts
    hemisphere_image_urls = mongo.db.hemisphere_image_urls

    # call scrape to get data
    [mars_news_data, featured_image_data, html_table_facts_data, hemisphere_image_urls_data] = scrape_mars.scrape()

    # update the mongo database
    mars_news.update({}, mars_news_data, upsert=True)
    featured_image.update({},featured_image_data, upsert=True)
    html_table_facts.update({},html_table_facts_data, upsert=True)
    hemisphere_image_urls.drop()
    hemisphere_image_urls.insert_many(hemisphere_image_urls_data)
    # update the hemisphere image urls
    # for hemisphere_data in hemisphere_image_urls_data:
    #     print('++++++')
    #     print(hemisphere_data)
    #     hemisphere_image_urls.update({},hemisphere_data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
