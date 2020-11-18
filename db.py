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
        Work = self.tables.work
        Genre = self.tables.genre
        Illustrator = self.tables.illustrator
        Musician = self.tables.musician
        Option = self.tables.option
        Scenario = self.tables.scenario
        Voice = self.tables.voice
        Writer = self.tables.writer

        return self.session.query(Work).\
            filter(Work.work_id in idlist).\
            filter(Work.work_id == Genre.work_id).\
            filter(Work.work_id == Illustrator.work_id).\
            filter(Work.work_id == Musician.work_id).\
            filter(Work.work_id == Option.work_id).\
            filter(Work.work_id == Scenario.work_id).\
            filter(Work.work_id == Voice.work_id).\
            filter(Work.work_id == Writer.work_id).\
            all()

    def search(self, params):
        # 集合を取りidのリストを返す
        return res
