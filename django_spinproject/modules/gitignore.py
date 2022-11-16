from ._base import BaseModule
from .gitignore_data import _V1_ENV, _V2_ENV


class GitignoreModule(BaseModule):
	name = 'gitignore'
	help_text = "Creates .gitignore file"
	environments = (_V1_ENV, _V2_ENV, )