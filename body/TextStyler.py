import copy

from intepreter.language.Semantic import Semantic
from intepreter.modules.ModuleManager import ModuleManager


class TextStyler:
    comments = []

    __just_replace = {
        '\n' : '<br/>',
        ' '  : '&nbsp;'
    }

    __word_type = {'command'   : sorted(ModuleManager.get_all_commands_names(),
                                         key = lambda x: len(x),
                                         reverse=True),
                   'operator'  : Semantic.get_operators() }

    __type_color = {'command'   : 'blue',
                    'operator'  : 'red',
                    'comment'   : 'grey',
                    'regular_word' : 'black'}

    @classmethod
    def plain_2_rich(cls, text):
        result = copy.deepcopy(text)

        result = cls.__cut_out_comments(result)

        for old in cls.__just_replace.keys():
            new = cls.__just_replace[old]
            result = result.replace(old, new)

        for type in cls.__word_type:
            for word in cls.__word_type[type]:
                result = result.replace(word, cls.__get_colored_word(word))

        return cls.__insert_comments(result)


    @classmethod
    def rich_2_plain(cls, text):
        result = copy.deepcopy(text)

        result = result.replace('<br />', '<br/>')
        for new in cls.__just_replace.keys():
            old = cls.__just_replace[new]
            result = result.replace(old, new)

        x = cls.__clear_code(result)
        y = x[36:] + '\n'
        return y

    @classmethod
    def __cut_out_comments(cls, text):
        lines = text.split('\n')
        for idx, line in enumerate(lines):
            try:
                comment = line[line.index(Semantic.get_symbol('comment')):]
                lines[idx] = line[:line.index(Semantic.get_symbol('comment'))]
                if comment:
                    cls.comments.append((idx, comment))
            except ValueError as ignored:
                pass

        return '\n'.join(lines)

    @classmethod
    def __insert_comments(cls, text):
        lines = text.split('<br/>')
        for idx, comment in cls.comments:
            lines[idx] += (cls.__get_colored_word(comment, cls.__type_color['comment']))

        cls.comments = []
        return '<br/>'.join(lines)

    @classmethod
    def __get_colored_word(cls, word, color=None):
        if color:
            return f'<font color=\"{color}\">{word}</font>'

        word_type = "regular_word"
        for x in cls.__word_type.keys():
            if word in cls.__word_type[x]:
                word_type = x

        color = cls.__type_color[word_type]
        return f'<font color=\"{color}\">{word}</font>'

    @classmethod
    def __clear_code(cls, rich):
        text = copy.deepcopy(rich)
        while True:
            try:
                text = text[:text.index('<')] + text[text.index('>') + 1:]
            except:
                break
        return text
