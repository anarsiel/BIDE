import copy

from intepreter.language.Semantic import Semantic
from intepreter.modules.DataProvider import DataProvider
from intepreter.modules.ModuleManager import ModuleManager


class TextStyler:
    __beginning = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">'
    __ending = '</p></body></html>'
    __just_replace = {
        '\n' : '<br/>',
        ' '  : '&nbsp;'
    }

    __word_type = {'commands'   : ModuleManager.get_all_commands_names(),
                   'operators'  : Semantic.get_operators() }

    __type_color = {'commands'   : 'blue',
                    'operators' : 'red' }

    @classmethod
    def plain_2_rich(cls, text):
        result = copy.deepcopy(text)

        for old in cls.__just_replace.keys():
            new = cls.__just_replace[old]
            result = result.replace(old, new)

        for type in cls.__word_type:
            for word in cls.__word_type[type]:
                result = result.replace(word, cls.get_colored_word(word))
        return result

    @classmethod
    def get_colored_word(cls, word):
        word_type = None
        for x in cls.__word_type.keys():
            if word in cls.__word_type[x]:
                word_type = x

        if not word_type:
            return word

        color = cls.__type_color[word_type]
        return f'<font color=\"{color}\">{word}</font>'

    @classmethod
    def rich_2_plain(cls, text):
        result = copy.deepcopy(text)

        result = result.replace('<br />', '<br/>')
        for new in cls.__just_replace.keys():
            old = cls.__just_replace[new]
            result = result.replace(old, new)

        x = cls.clear_code(result)
        y = x[36:] + '\n'
        return y

    @classmethod
    def clear_code(cls, rich):
        text = copy.deepcopy(rich)
        while True:
            try:
                text = text[:text.index('<')] + text[text.index('>') + 1:]
            except:
                break
        return text