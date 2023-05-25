class SecondaryDatabaseRouter:
    """
    A database router to route the Strategy model to the secondary database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'strategy':
            return 'secondary'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'strategy':
            return 'secondary'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'strategy' \
                or obj2._meta.app_label == 'strategy':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'strategy':
            return db == 'secondary'
        return None
