import json
from code_generator.result.model import DateEncoder

class Base_industries(object):

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
    
        # 第一产业产值(万元)
        self.first_industries = None
    
        # 第一产业占比(%)
        self.first_proportion = None
    
        # 第二产业产值(万元)
        self.second_industries = None
    
        # 第二产业占比(%)
        self.second_proportion = None
    
        # 第三产业产值(万元)
        self.three_industries = None
    
        # 第三产业占比(%)
        self.three_proportion = None
    
        # 
        self.create_time = None
    

    
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
    
    def get_first_industries(self):
        # 第一产业产值(万元)
        return self.first_industries
    
    def get_first_proportion(self):
        # 第一产业占比(%)
        return self.first_proportion
    
    def get_second_industries(self):
        # 第二产业产值(万元)
        return self.second_industries
    
    def get_second_proportion(self):
        # 第二产业占比(%)
        return self.second_proportion
    
    def get_three_industries(self):
        # 第三产业产值(万元)
        return self.three_industries
    
    def get_three_proportion(self):
        # 第三产业占比(%)
        return self.three_proportion
    
    def get_create_time(self):
        # 
        return self.create_time
    
    
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
    
    def set_first_industries(self, first_industries):
        # 第一产业产值(万元)
        self.first_industries = first_industries
    
    def set_first_proportion(self, first_proportion):
        # 第一产业占比(%)
        self.first_proportion = first_proportion
    
    def set_second_industries(self, second_industries):
        # 第二产业产值(万元)
        self.second_industries = second_industries
    
    def set_second_proportion(self, second_proportion):
        # 第二产业占比(%)
        self.second_proportion = second_proportion
    
    def set_three_industries(self, three_industries):
        # 第三产业产值(万元)
        self.three_industries = three_industries
    
    def set_three_proportion(self, three_proportion):
        # 第三产业占比(%)
        self.three_proportion = three_proportion
    
    def set_create_time(self, create_time):
        # 
        self.create_time = create_time
    

    def keys(self):
        '''
        当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
        但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法
        :param self:
        :return:
        '''
        return ('id', 'province_id', 'province_name', 'city_id', 'city_name', 'county_id', 'county_name', 'year', 'first_industries', 'first_proportion', 'second_industries', 'second_proportion', 'three_industries', 'three_proportion', 'create_time')

    def __getitem__(self, item):
        '''
        内置方法,当对实例化对象使用dict(obj)的时候, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值
        :param self:
        :param item:
        :return:
        '''
        return getattr(self, item)

    def __str__(self):
        Base_industriesDict = {'id': self.id,'province_id': self.province_id,'province_name': self.province_name,'city_id': self.city_id,'city_name': self.city_name,'county_id': self.county_id,'county_name': self.county_name,'year': self.year,'first_industries': self.first_industries,'first_proportion': self.first_proportion,'second_industries': self.second_industries,'second_proportion': self.second_proportion,'three_industries': self.three_industries,'three_proportion': self.three_proportion,'create_time': self.create_time}
        return json.dumps(Base_industriesDict,cls=DateEncoder)