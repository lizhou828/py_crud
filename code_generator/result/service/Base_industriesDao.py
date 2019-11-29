import datetime

from code_generator.result.DB.BaseDao import BaseDao
from code_generator.result.model.Base_industries import Base_industries

class Base_industriesDao(BaseDao):

    def __init__(self):
        super().__init__(Base_industries)
        pass

if __name__ == "__main__":
    dao = Base_industriesDao()
    data_list = dao.selectAll()
    for data1 in data_list:
        id = data1.get_id()
        all = data1.get_first_industries() +  data1.get_second_industries() + data1.get_three_industries()
        if all <= 0:
            continue


        update = Base_industries()
        update.set_id(id)
        first_proportion =  '%.4f' % ( data1.get_first_industries()  / all )
        first_proportion = float(first_proportion) * 100

        update.set_first_proportion(first_proportion)
        second_proportion = '%.4f' % ( data1.get_second_industries() /all )
        second_proportion = float(second_proportion)* 100
        update.set_second_proportion(second_proportion)
        three_proportion = '%.4f' % ( data1.get_three_industries()  / all )
        three_proportion = float(three_proportion)* 100
        update.set_three_proportion(three_proportion)
        update.set_create_time(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        dao.updateByPK(update)
        print(update)
