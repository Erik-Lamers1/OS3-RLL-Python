from pkg_resources import require

from os3_rrl.conf import settings


def show_version():
    print("""
OS3 Rocket League Ladder version {}
""".format(require(settings.PYTHON_PACKAGE_NAME)[0].version))
