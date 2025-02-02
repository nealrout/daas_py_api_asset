# This is a custom test runner that does not use a database.  We are doing this 
# because we opted for stored procedure/function calls for CRUD operations.
from django.test.runner import DiscoverRunner

class NoDbTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
