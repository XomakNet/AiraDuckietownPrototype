from unittest import TestCase
from validator.core.compile import TaxiCompiler
from validator.core.generator import TaxiGenerator
from validator.core.parser import MapParser, OrderParser
from antlr4 import CommonTokenStream, InputStream
from io import StringIO
from validator.core.grammar.PrismTemplateLexer import PrismTemplateLexer
from validator.core.grammar.PrismTemplateParser import PrismTemplateParser
from validator.core.grammar.listeners import PrismErrorListener


class TestCompiler(TestCase):
    map_path = "test_town"
    order_path = "test_order"
    template_path = "test_template.prism"

    def test_compiler(self):
        map_parser = MapParser(self.map_path)
        order_parser = OrderParser(self.order_path)
        generator = TaxiGenerator(map_parser.specification, order_parser.specification)

        compiler = TaxiCompiler(generator, self.template_path)

        input_stream = InputStream(str(compiler.compile()))
        output_stream = StringIO()
        lexer = PrismTemplateLexer(input_stream, output=output_stream)
        stream = CommonTokenStream(lexer)
        parser = PrismTemplateParser(stream)

        error_listener = PrismErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        parser.program()

        self.assertTrue(len(error_listener.msg_list) == 0)