import pytest


def func(n):
    return n+1

# Test 1
def test_func1():
    assert func(1) == 3
# Test 2
def test_func2():
    assert func(2) == 3



def f():
	raise SystemExit(1)
# Test 3
def test_mytest():
	with pytest.raises(SystemExit):
		f()


# fixture helps to set up the data to be used in the test
@pytest.fixture
# This function cannot be called directly
def setup_list():
	return ["apple", "banana"]
# Test 4
def test_apple(setup_list):
	assert "mango" in setup_list