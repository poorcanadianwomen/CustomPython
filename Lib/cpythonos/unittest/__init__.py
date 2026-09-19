"""unittest module for CustomPython OS.

Unit testing framework.
"""

import sys
import time
import traceback


class TestCase:
    """Base class for all test cases."""
    
    def __init__(self, methodName='runTest'):
        self._testMethodName = methodName
        self._outcome = None
        self._testMethodName = methodName
        self._cleanups = []
    
    def setUp(self):
        """Hook method for setting up the test fixture before each test."""
        pass
    
    def tearDown(self):
        """Hook method for tearing down the test fixture after each test."""
        pass
    
    def run(self, result=None):
        """Run the test."""
        if result is None:
            result = TestResult()
        
        result.startTest(self)
        try:
            self.setUp()
            try:
                testMethod = getattr(self, self._testMethodName)
                testMethod()
            except Exception as e:
                result.addError(self, e)
            else:
                result.addSuccess(self)
            try:
                self.tearDown()
            except Exception as e:
                result.addError(self, e)
        finally:
            result.stopTest(self)
        
        return result
    
    def assertEqual(self, first, second, msg=None):
        """Check that first == second."""
        if first != second:
            failureMessage = f'{first!r} != {second!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertNotEqual(self, first, second, msg=None):
        """Check that first != second."""
        if first == second:
            failureMessage = f'{first!r} == {second!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertTrue(self, expr, msg=None):
        """Check that expr is true."""
        if not expr:
            failureMessage = f'False is not true'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertFalse(self, expr, msg=None):
        """Check that expr is false."""
        if expr:
            failureMessage = f'True is not false'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIs(self, expr1, expr2, msg=None):
        """Check that expr1 is expr2."""
        if expr1 is not expr2:
            failureMessage = f'{expr1!r} is not {expr2!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIsNot(self, expr1, expr2, msg=None):
        """Check that expr1 is not expr2."""
        if expr1 is expr2:
            failureMessage = f'{expr1!r} is {expr2!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIsNone(self, expr, msg=None):
        """Check that expr is None."""
        if expr is not None:
            failureMessage = f'{expr!r} is not None'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIsNotNone(self, expr, msg=None):
        """Check that expr is not None."""
        if expr is None:
            failureMessage = f'None is not None'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIn(self, member, container, msg=None):
        """Check that member is in container."""
        if member not in container:
            failureMessage = f'{member!r} not found in {container!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertNotIn(self, member, container, msg=None):
        """Check that member is not in container."""
        if member in container:
            failureMessage = f'{member!r} found in {container!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIsInstance(self, obj, cls, msg=None):
        """Check that obj is an instance of cls."""
        if not isinstance(obj, cls):
            failureMessage = f'{obj!r} is not an instance of {cls!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertNotIsInstance(self, obj, cls, msg=None):
        """Check that obj is not an instance of cls."""
        if isinstance(obj, cls):
            failureMessage = f'{obj!r} is an instance of {cls!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertIsSubclass(self, cls, classinfo, msg=None):
        """Check that cls is a subclass of classinfo."""
        if not issubclass(cls, classinfo):
            failureMessage = f'{cls!r} is not a subclass of {classinfo!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertNotIsSubclass(self, cls, classinfo, msg=None):
        """Check that cls is not a subclass of classinfo."""
        if issubclass(cls, classinfo):
            failureMessage = f'{cls!r} is a subclass of {classinfo!r}'
            if msg:
                failureMessage = f'{msg}: {failureMessage}'
            raise self.failureException(failureMessage)
    
    def assertRaises(self, exception, callableObj=None, *args, **kwargs):
        """Check that an exception is raised."""
        context = _AssertRaisesContext(self, exception)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)
    
    def assertRaisesRegex(self, exception, regex, callableObj=None, *args, **kwargs):
        """Check that an exception is raised and matches regex."""
        context = _AssertRaisesContext(self, exception, regex=regex)
        if callableObj is None:
            return context
        with context:
            callableObj(*args, **kwargs)
    
    def assertWarns(self, warning, callableObj=None, *args, **kwargs):
        """Check that a warning is raised."""
        # Stub
        pass
    
    def assertLogs(self, logger=None, level=None):
        """Check that logs are emitted."""
        # Stub
        pass
    
    def fail(self, msg=None):
        """Fail immediately."""
        raise self.failureException(msg or 'Test failed')
    
    def addCleanup(self, function, /, *args, **kwargs):
        """Add a function to be called after tearDown."""
        self._cleanups.append((function, args, kwargs))
    
    def doCleanups(self):
        """Execute all cleanups."""
        while self._cleanups:
            function, args, kwargs = self._cleanups.pop()
            try:
                function(*args, **kwargs)
            except Exception:
                pass
    
    @property
    def failureException(self):
        """Return the exception class used for test failures."""
        return AssertionError


class _AssertRaisesContext:
    """Context manager for assertRaises."""
    
    def __init__(self, test_case, expected_exception, regex=None):
        self.test_case = test_case
        self.expected = expected_exception
        self.regex = regex
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            raise AssertionError(f'{self.expected.__name__} not raised')
        
        if not issubclass(exc_type, self.expected):
            return False
        
        if self.regex is not None:
            import re
            if not re.search(self.regex, str(exc_value)):
                raise AssertionError(
                    f'{self.expected.__name__} raised, but message does not match regex'
                )
        
        self.exception = exc_value
        return True


class TestResult:
    """Holds the result of a test run."""
    
    def __init__(self):
        self.errors = []
        self.failures = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
    
    def startTest(self, test):
        """Called when the test starts."""
        self.testsRun += 1
    
    def stopTest(self, test):
        """Called when the test ends."""
        pass
    
    def addError(self, test, err):
        """Called when an error occurs."""
        self.errors.append((test, self._exc_info_to_string(err, test)))
    
    def addFailure(self, test, err):
        """Called when a failure occurs."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
    
    def addSuccess(self, test):
        """Called when a test succeeds."""
        pass
    
    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        self.skipped.append((test, reason))
    
    def addExpectedFailure(self, test, err):
        """Called when an expected failure occurs."""
        self.expectedFailures.append((test, self._exc_info_to_string(err, test)))
    
    def addUnexpectedSuccess(self, test):
        """Called when an unexpected success occurs."""
        self.unexpectedSuccesses.append(test)
    
    def wasSuccessful(self):
        """Check if the test run was successful."""
        return not self.errors and not self.failures
    
    def _exc_info_to_string(self, err, test):
        """Convert exception info to string."""
        return ''.join(traceback.format_exception(*err))


class TestSuite:
    """A collection of tests."""
    
    def __init__(self, tests=()):
        self._tests = list(tests)
    
    def addTest(self, test):
        """Add a test."""
        self._tests.append(test)
    
    def addTests(self, tests):
        """Add multiple tests."""
        for test in tests:
            self.addTest(test)
    
    def run(self, result):
        """Run the test suite."""
        for test in self._tests:
            if result.shouldStop:
                break
            test.run(result)
        return result
    
    def __iter__(self):
        return iter(self._tests)
    
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
    
    def countTestCases(self):
        """Count test cases."""
        count = 0
        for test in self._tests:
            if isinstance(test, TestSuite):
                count += test.countTestCases()
            else:
                count += 1
        return count


class TestLoader:
    """Loads tests from test cases."""
    
    def loadTestsFromTestCase(self, testCaseClass):
        """Load tests from a test case class."""
        suite = TestSuite()
        for methodName in dir(testCaseClass):
            if methodName.startswith('test'):
                suite.addTest(testCaseClass(methodName))
        return suite
    
    def loadTestsFromModule(self, module):
        """Load tests from a module."""
        suite = TestSuite()
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, TestCase):
                suite.addTests(self.loadTestsFromTestCase(obj))
        return suite
    
    def loadTestsFromName(self, name):
        """Load tests from a name."""
        parts = name.split('.')
        module = __import__(parts[0])
        for part in parts[1:]:
            module = getattr(module, part)
        
        if isinstance(module, type) and issubclass(module, TestCase):
            return self.loadTestsFromTestCase(module)
        return self.loadTestsFromModule(module)
    
    def discover(self, start_dir, pattern='test*.py', top_level_dir=None):
        """Discover tests in a directory."""
        suite = TestSuite()
        import os
        import importlib
        
        for root, dirs, files in os.walk(start_dir):
            for filename in files:
                if filename.startswith('test') and filename.endswith('.py'):
                    filepath = os.path.join(root, filename)
                    module_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    suite.addTests(self.loadTestsFromModule(module))
        
        return suite


class TextTestRunner:
    """Test runner that outputs results to text."""
    
    def __init__(self, stream=None, verbosity=1):
        if stream is None:
            stream = sys.stderr
        self.stream = stream
        self.verbosity = verbosity
    
    def run(self, test):
        """Run a test suite."""
        result = TestResult()
        start_time = time.time()
        test(result)
        duration = time.time() - start_time
        
        self.stream.write('\n')
        
        # Print results
        if result.errors:
            self.stream.write('ERROR: %d\n' % len(result.errors))
            for test, err in result.errors:
                self.stream.write('  %s\n' % test)
                self.stream.write('    %s\n' % err)
        
        if result.failures:
            self.stream.write('FAIL: %d\n' % len(result.failures))
            for test, err in result.failures:
                self.stream.write('  %s\n' % test)
                self.stream.write('    %s\n' % err)
        
        if result.skipped:
            self.stream.write('SKIP: %d\n' % len(result.skipped))
        
        self.stream.write('\n')
        self.stream.write('Ran %d tests in %.3fs\n' % (result.testsRun, duration))
        self.stream.write('\n')
        
        if result.wasSuccessful():
            self.stream.write('OK\n')
        else:
            self.stream.write('FAILED (failures=%d, errors=%d)\n' % (
                len(result.failures), len(result.errors)))
        
        return result


def main(module='__main__', defaultTest=None, argv=None, testLoader=None,
         testRunner=None, exit=True, verbosity=1, failfast=False,
         catchbreak=False, buffer=False):
    """Discover and run tests."""
    if argv is None:
        argv = sys.argv
    
    if testLoader is None:
        testLoader = TestLoader()
    
    if testRunner is None:
        testRunner = TextTestRunner(verbosity=verbosity)
    
    # Import module
    if isinstance(module, str):
        import importlib
        module = importlib.import_module(module)
    
    # Load tests
    suite = testLoader.loadTestsFromModule(module)
    
    # Run tests
    result = testRunner.run(suite)
    
    if exit:
        sys.exit(not result.wasSuccessful())
    
    return result
