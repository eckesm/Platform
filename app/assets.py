# https://hackersandslackers.com/flask-blueprints


from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = False
    common_less_bundle = Bundle(
        'src/less/*.less',
        filters='less,cssmin',
        output='dist/css/style.css',
        extra={'rel': 'stylesheet/less'}
    )
    auth_less_bundle = Bundle(
        'auth_bp/less/auth.less',
        filters='less,cssmin',
        output='dist/css/auth.css',
        extra={'rel': 'stylesheet/less'}
    )
    groups_less_bundle = Bundle(
        'groups_bp/less/groups.less',
        filters='less,cssmin',
        output='dist/css/groups.css',
        extra={'rel': 'stylesheet/less'}
    )
    home_less_bundle = Bundle(
        'home_bp/less/home.less',
        filters='less,cssmin',
        output='dist/css/home.css',
        extra={'rel': 'stylesheet/less'}
    )
    posts_less_bundle = Bundle(
        'posts_bp/less/posts.less',
        filters='less,cssmin',
        output='dist/css/posts.css',
        extra={'rel': 'stylesheet/less'}
    )
    users_less_bundle = Bundle(
        'users_bp/less/users.less',
        filters='less,cssmin',
        output='dist/css/users.css',
        extra={'rel': 'stylesheet/less'}
    )
    assets.register('common_less_bundle', common_less_bundle)
    assets.register('auth_less_bundle', auth_less_bundle)
    assets.register('groups_less_bundle', groups_less_bundle)
    assets.register('home_less_bundle', home_less_bundle)
    assets.register('posts_less_bundle', posts_less_bundle)
    assets.register('users_less_bundle', users_less_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_less_bundle.build()
        auth_less_bundle.build()
        groups_less_bundle.build()
        home_less_bundle.build()
        posts_less_bundle.build()
        users_less_bundle.build()
    return assets
