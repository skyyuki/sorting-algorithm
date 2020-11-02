import importlib


def pytest_generate_tests(metafunc):
    if 'sorter' in metafunc.fixturenames:
        from test.test_visual_sorting import sub_sorters
        for module_name in sub_sorters:
            module = importlib.import_module('visual_sorting.' + module_name)
            metafunc.parametrize('sorter', (getattr(module, func_name) for func_name in sub_sorters[module_name]))
