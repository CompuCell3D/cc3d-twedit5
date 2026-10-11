import re
import yaml

from collections import namedtuple

SnippetTuple = namedtuple('SnippetTuple', 'snippet_text suggested_indent description')


class SnippetMenuParser(object):

    def __init__(self):

        self.snippetMenu = {}

        self.currentMenu = None

        self.currentSubmenu = None

        self.currentSnippet = None

        self.currentSuggestedIndent = None

        self.menuRegex = re.compile(r'^[=]*[\s]*#[\s]*@Menu@([\s\S]*)$')

        self.submenuRegex = re.compile(r'^[-]*([i\d]*)[\s]*#[\s]*@Submenu@([\s\S]*)$')

    def initialize(self):

        self.snippetMenu = {}

        self.currentMenu = None

        self.currentSubmenu = None

        self.currentSnippet = None

        self.currentSuggestedIndent = None

    def getSnippetMenuDict(self):

        return self.snippetMenu

    def findToken(self, _line, _regex, group_idx=0):

        line = _line.rstrip()

        for m in _regex.finditer(line):
            tokenGroup = m.groups()

            return tokenGroup[group_idx]

        return None

    def writeSnippet(self):

        if self.currentSnippet and self.currentMenu and self.currentSubmenu:

            self.currentMenu[self.currentSubmenu] = SnippetTuple(
                self.currentSnippet,
                self.currentSuggestedIndent if self.currentSuggestedIndent is not None else -1,
                ''
            )

    def _read_yaml_snippet_menu(self, file_name):

        with open(file_name) as file_handle:
            data = yaml.safe_load(file_handle) or {}

        self.initialize()

        menus = data.get('menus', [])
        for menu_data in menus:
            menu_name = str(menu_data.get('name', '')).strip()
            if not menu_name:
                continue

            submenu_dict = {}
            for snippet_data in menu_data.get('snippets', []):
                snippet_name = str(snippet_data.get('name', '')).strip()
                if not snippet_name:
                    continue

                snippet_text = snippet_data.get('code', '')
                if snippet_text is None:
                    snippet_text = ''

                submenu_dict[snippet_name] = SnippetTuple(
                    str(snippet_text),
                    int(snippet_data.get('suggested_indent', -1)),
                    str(snippet_data.get('description', '') or '')
                )

            self.snippetMenu[menu_name] = submenu_dict

    def _read_legacy_snippet_menu(self, file_name):

        with open(file_name) as file_handle:
            readyToAddSnippet = False

            for line in file_handle:

                menuName = self.findToken(line, self.menuRegex)

                if menuName:
                    self.writeSnippet()

                    readyToAddSnippet = False

                    self.snippetMenu[menuName] = {}

                    self.currentMenu = self.snippetMenu[menuName]

                    continue

                submenuName = self.findToken(line, self.submenuRegex, group_idx=1)

                suggested_indent = self.findToken(line, self.submenuRegex, group_idx=0)

                if submenuName is not None:

                    submenuName = submenuName.strip()

                    if suggested_indent:
                        self.currentSuggestedIndent = int(suggested_indent[1:])

                if submenuName:

                    self.writeSnippet()

                    self.currentSubmenu = submenuName

                    self.currentMenu[submenuName] = ''

                    self.currentSnippet = ''

                    readyToAddSnippet = True

                    if suggested_indent:

                        self.currentSuggestedIndent = int(suggested_indent[1:])

                    else:

                        self.currentSuggestedIndent = -1

                    continue

                if readyToAddSnippet:
                    self.currentSnippet += line

        self.writeSnippet()

    def readSnippetMenu(self, _fileName):

        with open(_fileName) as file_handle:
            first_nonempty_line = ''
            for line in file_handle:
                if line.strip():
                    first_nonempty_line = line.strip()
                    break

        if first_nonempty_line.startswith('version:') or first_nonempty_line.startswith('menus:'):
            self._read_yaml_snippet_menu(_fileName)
            return

        self.initialize()
        self._read_legacy_snippet_menu(_fileName)
