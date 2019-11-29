import json
from code_generator.result.model import DateEncoder

class Base_production(object):

    def __init__(self):
    
        # 
        self.id = None
    
        # 
        self.province_id = None
    
        # 
        self.province_name = None
    
        # 
        self.city_id = None
    
        # 
        self.city_name = None
    
        # 
        self.county_id = None
    
        # 
        self.county_name = None
    
        # 年份
        self.year = None
    
        # 地区生产总值(万元)
        self.production_total = None
    
        # 地区生产总值增长速度(%)
        self.growth_rate = None
    
        # 
        self.create_time = None
    
        # 人均生产总值(万元)
        self.per_capita_production = None
    
        # 人均生产总值增速(%)
        self.per_capita_growth_rate = None
    

    
    def get_id(self):
        # 
        return self.id
    
    def get_province_id(self):
        # 
        return self.province_id
    
    def get_province_name(self):
        # 
        return self.province_name
    
    def get_city_id(self):
        # 
        return self.city_id
    
    def get_city_name(self):
        # 
        return self.city_name
    
    def get_county_id(self):
        # 
        return self.county_id
    
    def get_county_name(self):
        # 
        return self.county_name
    
    def get_year(self):
        # 年份
        return self.year
    
    def get_production_total(self):
        # 地区生产总值(万元)
        return self.production_total
    
    def get_growth_rate(self):
        # 地区生产总值增长速度(%)
        return self.growth_rate
    
    def get_create_time(self):
        # 
        return self.create_time
    
    def get_per_capita_production(self):
        # 人均生产总值(万元)
        return self.per_capita_production
    
    def get_per_capita_growth_rate(self):
        # 人均生产总值增速(%)
        return self.per_capita_growth_rate
    
    
    def set_id(self, id):
        # 
        self.id = id
    
    def set_province_id(self, province_id):
        # 
        self.province_id = province_id
    
    def set_province_name(self, province_name):
        # 
        self.province_name = province_name
    
    def set_city_id(self, city_id):
        # 
        self.city_id = city_id
    
    def set_city_name(self, city_name):
        # 
        self.city_name = city_name
    
    def set_county_id(self, county_id):
        # 
        self.county_id = county_id
    
    def set_county_name(self, county_name):
        # 
        self.county_name = county_name
    
    def set_year(self, year):
        # 年份
        self.year = year
    
    def set_production_total(self, production_total):
        # 地区生产总值(万元)
        self.production_total = production_total
    
    def set_growth_rate(self, growth_rate):
        # 地区生产总值增长速度(%)
        self.growth_rate = growth_rate
    
    def set_create_time(self, create_time):
        # 
        self.create_time = create_time
    
    def set_per_capita_production(self, per_capita_production):
        # 人均生产总值(万元)
        self.per_capita_production = per_capita_production
    
    def set_per_capita_growth_rate(self, per_capita_growth_rate):
        # 人均生产总值增速(%)
        self.per_capita_growth_rate = per_capita_growth_rate
    

    def keys(self):
        '''
        当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
        但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法
        :param self:
        :return:
        '''
        return ('id', 'province_id', 'province_name', 'city_id', 'city_name', 'county_id', 'county_name', 'year', 'production_total', 'growth_rate', 'create_time', 'per_capita_production', 'per_capita_growth_rate')

    def __getitem__(self, item):
        '''
        内置方法,当对实例化对象使用dict(obj)的时候, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值
        :param self:
        :param item:
        :return:
        '''
        return getattr(self, item)

    def __str__(self):
        Base_productionDict = {'id': self.id,'province_id': self.province_id,'province_name': self.province_name,'city_id': self.city_id,'city_name': self.city_name,'county_id': self.county_id,'county_name': self.county_name,'year': self.year,'production_total': self.production_total,'growth_rate': self.growth_rate,'create_time': self.create_time,'per_capita_production': self.per_capita_production,'per_capita_growth_rate': self.per_capita_growth_rate}
        return json.dumps(Base_productionDict,cls=DateEncoder)