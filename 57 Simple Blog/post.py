import requests as req


class Post:
    def __init__(self):
        self.posts_url = "https://api.npoint.io/c790b4d5cab58020d391"

    def get_all_posts(self):
        res = req.get(self.posts_url)
        return res.json()
