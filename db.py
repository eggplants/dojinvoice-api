from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class DojinvoiceDB(object):
    def __init__(self):
        Base = automap_base()
        self.engine = create_engine("sqlite:///dojinvoice.db")
        self.session = Session(self.engine)
        Base.prepare(self.engine, reflect=True)
        self.tables = Base.classes

    def get_exist_chobit_list(self) -> List[str]:
        Option = self.tables.option
        datalist = self.session.query(Option.work_id, Option.chobit_link).\
            filter(Option.chobit_link is not None).all()
        return datalist

    def get_category_list(self):
        Work = self.tables.work
        datalist = self.session.query(Work.category).all()
        return set(datalist)

    def idlist_to_data_list(self, idlist: List[str]):

        pass

    def search(self, params):
        # 集合を取りidのリストを返す
        return res
