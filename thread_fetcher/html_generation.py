
from jinja2 import Environment, FileSystemLoader

class HTML:
    def __init__(self, title_text, file_name) -> None:
        env = Environment(loader=FileSystemLoader('template'))
        self.template = env.get_template('template.html')
        self.file_content = None
        self.title_text = title_text
        self.file_name = file_name
        self.body = ""
        self.url = ""
        

    def add_tweet_card(self, tweet_text, tweet_media_type=None, tweet_media_urls=None) -> None:
        self.body += """<div class="tweet_card">"""
        self.body += f"""<div class="tweet_text">{tweet_text}</div>"""
        if tweet_media_type == "photo":
            for image_url in tweet_media_urls:
                self.body += f"""
                <img class="tweet_image" src="{image_url}">
                """
        elif tweet_media_type == "animated_gif":
            self.body += f"""
            <video class="tweet_gif" controls autoplay src="{tweet_media_urls[0]}">
            """
        elif tweet_media_type == "video":
            self.body += f"""
            <video class="tweet_video" controls src="{tweet_media_urls[0]}"/>
            """
        self.body += "</div>"

    def save(self) -> None:
        file_content = self.template.render(
            title=self.title_text, body=self.body)
        with open(self.file_name + ".html", "w") as f:
            f.write(file_content)











