import requests
from bs4 import BeautifulSoup

from intepreter.modules.DataProvider import DataProvider
from intepreter.modules._interfaces.CommonLogic import CommonLogic


class WebLogic:
    @staticmethod
    def load_page(url):
        session = requests.Session()
        response = session.get(url)
        content = response.text

        DataProvider.return_value(content)

    @staticmethod
    def get_element_from_html(filename, traverse_tags, cmd, cmd_value):
        with open(filename, 'r') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'lxml')

            tags = traverse_tags.split('@')
            if tags[0] == "":
                tags = tags[1:]

            current = soup
            for tag in tags:
                tag_name, *tag_cnts = tag.split('!')
                tag_cnts.append(1)
                tag_cnt = int(tag_cnts[0])

                next_child = None
                children = [e for e in current.children if e.name is not None]
                for child in children:
                    if child.name == tag_name:
                        tag_cnt -= 1
                        if tag_cnt == 0:
                            next_child = child
                            break

                if not next_child:
                    raise CommonLogic.RunTimeError()

                current = next_child

            if cmd == 'attr':
                try:
                    # DataProvider.return_value("http:" + current[cmd_value])
                    DataProvider.return_value('https:' + current[cmd_value])
                except:
                    raise CommonLogic.RunTimeError(
                        f'Wrong attribute value `{cmd_value}`'
                    )
            elif cmd == 'field':
                parts = current.text.split()
                parts = [part.strip() for part in parts]
                DataProvider.return_value(" ".join(parts))
            else:
                raise CommonLogic.RunTimeError(
                    f'Wrong attribute name `{cmd}`'
                )

class Web:
    __info = [
        ['load_page', WebLogic.load_page, [str], None, None],
        ['get_element_from_html', WebLogic.get_element_from_html, [str, str, str, str], None, None],
    ]

    @staticmethod
    def get_info():
        return Web.__info
