import mock
from bnoc import bnoc


def test_arg_routing_and_return_objects():
    with mock.patch('argparse._sys.argv', 'bnoc.py -cnf input/bipartite-1.json -o'.split(' ')):
        d = bnoc().build()
    assert all(i in d for i in ('info', 'matrices', 'overlap', 'cover', 'extra'))
