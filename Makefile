.PHONY: help
help:
	@echo '*****************************************************************************'
	@echo '*                                                                           *'
	@echo '* There are some commands for this project.                                 *'
	@echo '* Use TAB to complete the commands.                                         *'
	@echo '* SUPPORT LINUX/UNIX ONLY.                                                  *'
	@echo '*                                                                           *'
	@echo '* Usage:                                                                    *'
	@echo '*     make [option]                                                         *'
	@echo '*                                                                           *'
	@echo '* Example:                                                                  *'
	@echo '*     make help                                                             *'
	@echo '*                                                                           *'
	@echo '* Options:                                                                  *'
	@echo '*     help              --List all the commands and usages.                 *'
	@echo '*     clean             --Remove tempfiles (cache, test, etc).              *'
	@echo '*                                                                           *'
	@echo '*****************************************************************************'

.PHONY: clean
clean:
	@echo 'Cleaning, wait a minute please.'
	@find . -name '.tox' -print -exec rm -rf {} +
	@find . -name 'dist' -print -exec rm -rf {} +
	@find . -name 'htmlcov' -print -exec rm -rf {} +
	@find . -name '*.pyc' -print -exec rm -f {} +
	@find . -name '*.pyo' -print -exec rm -f {} +
	@find . -name '*.log*' -print -exec rm -f {} +
	@find . -name '.pytest_cache' -print -exec rm -rf {} +
	@find . -name '__pycache__' -print -exec rm -rf {} +
	@find . -path ./.coveragerc -prune -o -name '*coverage*' -print -exec rm -f {} +
	@echo 'Done [clean]'
