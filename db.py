from typing import Any, List, Optional, TypedDict, cast

# from api import Params
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class PagenatedListDict(TypedDict):
    offset: int
    index: int
    data: List[Any]


def pagenate(lis: List[Any], offset: int, idx: int) -> PagenatedListDict:
    _ = cast(PagenatedListDict, {})
    start = idx*offset
    _['offset'], _['index'], _['data'] = offset, idx, lis[start:start + offset]
    return _


class DojinvoiceDB(object):
    def __init__(self):
        Base = automap_base()
        self.engine = create_engine("sqlite:///dojinvoice.db")
        self.session = Session(self.engine)
        Base.prepare(self.engine, reflect=True)
        self.tables = Base.classes

    def get_exist_chobit_list(
            self, offset: int, idx: int) -> PagenatedListDict:
        datalist = [{"id": _['work_id'], "chobit_link":_['chobit_link']}
                    for _ in self.engine.execute(
                        '''select work_id, chobit_link from option
                        where chobit_link is not null''')]
        return pagenate(datalist, offset, idx)

    def get_category_list(self, offset: int, idx: int):
        Work = self.tables.work
        datalist = self.session.query(Work.category).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_genre_list(self, offset: int, idx: int):
        Genre = self.tables.genre
        datalist = self.session.query(Genre.genre).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_rate_filtered_list(self, min_rate: float, max_rate: float,
                               idlist: Optional[List[str]] = None):
        _ = [_['work_id'] for _ in self.engine.execute(
            '''select work_id from option
            where rating is not null and :min <= rating and :max >= rating ''',
            min=min_rate, max=max_rate)]
        return (set(idlist) | set(_) if idlist is not None else _)

    def get_illustrator_list(self, offset: int, idx: int):
        Illustrator = self.tables.illustrator
        datalist = self.session.query(Illustrator.illustrator).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_musician_list(self, offset: int, idx: int):
        Musician = self.tables.musician
        datalist = self.session.query(Musician.musician).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_scenario_list(self, offset: int, idx: int):
        Scenario = self.tables.scenario
        datalist = self.session.query(Scenario.scenario).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_voice_list(self, offset: int, idx: int):
        Voice = self.tables.voice
        datalist = self.session.query(Voice.voice).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

    def get_writer_list(self, offset: int, idx: int):
        Writer = self.tables.writer
        datalist = self.session.query(Writer.writer).all()
        datalist = [_[0] for _ in list(set(datalist))]
        return pagenate(datalist, offset, idx)

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
            join(Genre, Work.work_id == Genre.work_id).\
            join(Genre, Work.work_id == Illustrator.work_id).\
            join(Musician, Work.work_id == Musician.work_id).\
            join(Option, Work.work_id == Option.work_id).\
            join(Scenario, Work.work_id == Scenario.work_id).\
            join(Voice, Work.work_id == Voice.work_id).\
            join(Writer, Work.work_id == Writer.work_id).\
            all()

    # def search(self, params: Params):
    #     # keyword: str
    #     # category: str
    #     # max_rate: float
    #     # min_rate: float
    #     # genre: str
    #     # illustrator: str
    #     # musician: str
    #     # scenario: str
    #     # voice: str
    #     # writer: str
    #     return res
