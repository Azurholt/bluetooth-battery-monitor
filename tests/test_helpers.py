import ast
import pathlib
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_FILE = REPO_ROOT / 'bluetooth_battery_monitor.py'


def _load_helper_functions():
    source = SOURCE_FILE.read_text()
    tree = ast.parse(source, filename=str(SOURCE_FILE))

    wanted = {'Appearance', 'BTClassName'}
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]

    module = ast.Module(body=selected, type_ignores=[])
    ast.fix_missing_locations(module)

    namespace = {}
    exec(compile(module, filename=str(SOURCE_FILE), mode='exec'), namespace)
    return namespace['Appearance'], namespace['BTClassName']


Appearance, BTClassName = _load_helper_functions()


class TestAppearance(unittest.TestCase):
    def test_known_appearance_values(self):
        self.assertEqual(Appearance(64), 'Phone')
        self.assertEqual(Appearance(961), 'Keyboard')
        self.assertEqual(Appearance(964), 'Gamepad')

    def test_unknown_appearance_value(self):
        self.assertEqual(Appearance(9999), 'Unknown')


class TestBTClassName(unittest.TestCase):
    def _cod(self, major, minor):
        return (major << 8) | (minor << 2)

    def test_known_class_values(self):
        self.assertEqual(BTClassName(self._cod(2, 3)), 'Smartphone')
        self.assertEqual(BTClassName(self._cod(4, 1)), 'Headset')
        self.assertEqual(BTClassName(self._cod(5, 2 * 16)), 'Mouse')

    def test_unknown_class_values(self):
        self.assertEqual(BTClassName(self._cod(7, 0)), 'Unknown')


if __name__ == '__main__':
    unittest.main()
