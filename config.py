
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Chip2447@localhost/mechanic_shop_db'
    DEBUG = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass