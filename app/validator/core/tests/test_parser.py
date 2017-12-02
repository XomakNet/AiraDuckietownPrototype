from unittest import TestCase
from antlr4 import ParseTreeWalker, CommonTokenStream, FileStream
from validator.core.grammar.PrismTemplateLexer import PrismTemplateLexer
from validator.core.grammar.PrismTemplateParser import PrismTemplateParser
from validator.core.grammar.listeners import PrismReplacementsGatherer
from validator.core.parser import MapParser, OrderParser, TagsParser


class TestTemplateParser(TestCase):

    _template_path = "test_template.prism"

    def test_create_tree(self):
        input_stream = FileStream(self._template_path)
        lexer = PrismTemplateLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PrismTemplateParser(stream)
        tree = parser.program()

        self.assertIsNotNone(tree)

    def test_replacements_parsing(self):
        input_stream = FileStream(self._template_path)
        lexer = PrismTemplateLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = PrismTemplateParser(stream)
        tree = parser.program()

        listener = PrismReplacementsGatherer()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        self.assertTrue("move" in listener.replacements)
        self.assertTrue("max_x" in listener.replacements)
        self.assertTrue("max_y" in listener.replacements)
        self.assertTrue("max_direction" in listener.replacements)


class TestMapParser(TestCase):
    map_path = "test_town"

    def test_parsing(self):
        map_parser = MapParser(self.map_path)

        self.assertTrue(map_parser.specification.max_x == 9)
        self.assertTrue(map_parser.specification.max_y == 9)
        self.assertTrue(len(map_parser.specification.graph.nodes()) == 100)
        self.assertTrue(len(map_parser.specification.graph.edges()) == 9)


class TestOrderParser(TestCase):
    order_path = "test_order"

    def test_parsing(self):
        order_parser = OrderParser(self.order_path)

        self.assertTrue(order_parser.specification.start == (0, 0))
        self.assertTrue(order_parser.specification.finish == (9, 0))


class TestTagsParser(TestCase):
    tags_path = "test_tags"

    def test_parsing(self):
        tags_parser = TagsParser(self.tags_path)
        self.assertTrue([i for i in range(1, 8)] == tags_parser.specification.tags)
