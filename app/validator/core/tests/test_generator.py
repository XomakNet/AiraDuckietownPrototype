from unittest import TestCase

from antlr4 import CommonTokenStream, InputStream
from io import StringIO

from validator.core.generator import TaxiGenerator, TagsGenerator
from validator.core.grammar.PrismTemplateLexer import PrismTemplateLexer
from validator.core.grammar.PrismTemplateParser import PrismTemplateParser
from validator.core.grammar.listeners import PrismErrorListener
from validator.core.parser import MapParser, OrderParser, TagsParser


class TestTaxiGenerator(TestCase):
    map_path = "test_town"
    order_path = "test_order"

    def test_order_calculations(self):
        map_parser = MapParser(self.map_path)
        order_parser = OrderParser(self.order_path)
        generator = TaxiGenerator(map_parser.specification, order_parser.specification)

        self.assertTrue(generator.can_satisfy_order)
        self.assertIsNotNone(generator._path)

    def test_move(self):
        map_parser = MapParser(self.map_path)
        order_parser = OrderParser(self.order_path)
        generator = TaxiGenerator(map_parser.specification, order_parser.specification)

        input_stream = InputStream(generator.move())
        output_stream = StringIO()
        lexer = PrismTemplateLexer(input_stream, output=output_stream)
        stream = CommonTokenStream(lexer)
        parser = PrismTemplateParser(stream)

        error_listener = PrismErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        parser.guard_declarations()
        self.assertTrue(len(error_listener.msg_list) == 0)


class TestTagsGenerator(TestCase):
    tags_path = "test_tags"
    tags_template_path = "test_tags_template.prism"

    def test_move(self):
        tags_parser = TagsParser(self.tags_path)
        generator = TagsGenerator(tags_parser.specification)

        input_stream = InputStream(generator.move())
        output_stream = StringIO()
        lexer = PrismTemplateLexer(input_stream, output=output_stream)
        stream = CommonTokenStream(lexer)
        parser = PrismTemplateParser(stream)

        error_listener = PrismErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        parser.guard_declarations()
        self.assertTrue(len(error_listener.msg_list) == 0)
