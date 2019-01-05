# Fix monkey patching ssl
import gevent
from gevent import monkey
monkey.patch_all()

# https://stackoverflow.com/a/51704613
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


DEFAULT_LOGGER = 'rlbot'

# https://stackoverflow.com/a/24773951
def install_and_import(package):
    import importlib

    try:
        importlib.import_module(package)
    except ImportError:
        pipmain(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

if __name__ == '__main__':
    install_and_import('rlbot')
    from rlbot.utils import public_utils, logging_utils
    logger = logging_utils.get_logger(DEFAULT_LOGGER)
    if not public_utils.have_internet():
        logger.log(logging_utils.logging_level, 'Skipping upgrade check for now since it looks like you have no internet')
    elif public_utils.is_safe_to_upgrade():
        pipmain(['install', '-r', 'requirements.txt', '--upgrade', '--upgrade-strategy=eager'])

    import gui  # This runs the gui