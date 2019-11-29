import datetime

from code_generator.result.DB.BaseDao import BaseDao
from code_generator.result.model.Base_production import Base_production

class Base_productionDao(BaseDao):

    def __init__(self):
        super().__init__(Base_production)
        pass

if __name__ == "__main__":
    dao = Base_productionDao()
    data_list = dao.selectAll()
    for data1 in data_list:

        per_capita_production = 0
        for data2 in data_list:
            if data1.get_city_id() == data2.get_city_id() and  data1.get_county_id() == data2.get_county_id() and data1.get_year()-1 == data2.get_year():
                # 找到下一年的数据
                per_capita_production = data2.get_per_capita_production()

        update = Base_production()
        if per_capita_production <= 0:
            update.set_per_capita_growth_rate(0)
        else:
            per_capita_growth_rate = '%.4f' % ((data1.get_per_capita_production() - per_capita_production) / per_capita_production)
            first_proportion = float(per_capita_growth_rate) * 100
            update.set_per_capita_growth_rate(per_capita_growth_rate)
        update.set_id(data1.get_id())
        update.set_create_time(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        dao.updateByPK(update)
