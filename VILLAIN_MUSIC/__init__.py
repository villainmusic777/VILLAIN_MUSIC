from .logging import LOGGER
from .core.dir import dirr
from .core.git import git
from .core.bot import VILLAIN
from .misc import dbb

dirr()
git()
dbb()

app = VILLAIN()
