from datetime import datetime

from sqlalchemy.dialects.postgresql.ranges import dc_kwonly
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column


Base = declarative_base()



class Picture(Base):

    __tablename__ = "Picture"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    path: Mapped[str]
    load_date: Mapped[datetime] = mapped_column(default=datetime.now())
    resolution: Mapped[str]
    size: Mapped[float]





