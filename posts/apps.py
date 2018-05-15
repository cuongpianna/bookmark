from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'
    verbose_name = 'Post bookmarks'

    def ready(self):
        import posts.signals
