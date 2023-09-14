class PrimaryDataBaseRouter:
    def db_for_read(self, model, **hints):
        return 'slave'

    def db_for_write(self, model, **hints):
        return 'master'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {
            'master',
        }

        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True

        return None


class TestDataBaseRouter:
    def db_for_read(self, model, **hints):
        return 'master'

    def db_for_write(self, model, **hints):
        return 'master'
