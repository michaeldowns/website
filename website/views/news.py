from flask import Blueprint, render_template

from ..models import NewsPost

news = Blueprint('news', __name__)

@news.route('/news')
def page():
    news_posts = NewsPost.query.order_by(
        NewsPost.posted.desc(),
        NewsPost.id
    ).all()

    return render_template('news.html', news_posts=news_posts)
