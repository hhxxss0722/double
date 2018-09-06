from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Imei(Base):
	__tablename__ = 'Imei'
	id = Column(Integer, primary_key=True)
	imei = Column(String(15))
	url = Column(String(512))
	date = Column(String(15))

	def __repr__(self):
		return "<Imei(imei='%s', url='%s', date='%s')>" % (self.imei, self.url, self.date)
		
class dbhelpper():
	def __init__(self,base,dburl):
		self.db=create_engine(dburl)
		self.base=base
		self.db.echo=False
		self.base.metadata.create_all(self.db)
		Session = sessionmaker(bind=self.db)
		self.session = Session()
		
	def AddImei(self,imeicode):
		s=''
		try:
			self.session.add(imeicode)
			self.session.commit()
			s='aok'
		except Exception as e:
			s=str(e)
		return s
		
	def QueryImei(self,imei):
		ilist = self.session.query(Imei).filter(Imei.imei==imei).all()
		return ilist
		
	def closeall(self):
		s=''
		try:
			self.session.close()
			s='cok'
		except Exception as e:
			s=str(e)
		return s
		
def InitDb(url):
	db=dbhelpper(Base,url)
	return db
	
def AddImei(imeicode,db):
	s=db.AddImei(imeicode)
	return s
	
def QueryImei(imei,db):
	s=db.QueryImei(imei)
	return s
	
def CloseDb(db):
	s=db.closeall()
	return s