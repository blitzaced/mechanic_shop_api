
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Chip2447@localhost/mechanic_shop_db'
    DEBUG = True
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    TESTING = True  # Add this
    WTF_CSRF_ENABLED = False  # Add this for form testing
    SECRET_KEY = 'test-secret-key'

class ProductionConfig:
    pass

development = DevelopmentConfig
testing = TestingConfig
production = ProductionConfig