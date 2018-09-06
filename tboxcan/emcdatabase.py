from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImeiRecord(Base):
	__tablename__ = 'ImeiRecord'
	id = Column(Integer, primary_key=True)
	imei = Column(String(15))
	head = Column(String(15))
	state=Column(String(15))
	xml=Column(String(1024))
	date = Column(String(15))

	def __repr__(self):
		return "<Imei(imei='%s', head='%s', state='%s',xml='%s',date='%s')>" % (self.imei, self.head,self.state,self.xml, self.date)
		
class xmldbhelpper():
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
		ilist = self.session.query(ImeiRecord).filter(ImeiRecord.imei==imei).all()
		return ilist

	def QueryHead(self,head,b):
		pagination = self.session.query(ImeiRecord).filter(ImeiRecord.head==head).order_by(ImeiRecord.id.desc()).limit(10).offset(b).all()
		return pagination

	def QueryAll(self):
		pagination = self.session.query(ImeiRecord).order_by(ImeiRecord.id.desc()).all()
		return pagination

	def QueryC(self):
		pagination = self.session.query(ImeiRecord).filter(ImeiRecord.state=='0').order_by(ImeiRecord.id.desc()).all()
		return pagination
		
	def closeall(self):
		s=''
		try:
			self.session.close()
			s='cok'
		except Exception as e:
			s=str(e)
		return s
		
def InitDb(url):
	db=xmldbhelpper(Base,url)
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

def QueryHead(db,head,b):
	p=db.QueryHead(head,b)
	return p

def QueryAll(db):
	p=db.QueryAll()
	return p

def QueryC(db):
	p=db.QueryC()
	return p
"""
sqlpath="sqlite:///emcdb//emc.db"
db=InitDb(sqlpath)
QueryHead(db,'l99m',0)
QueryHead(db,'l99m',1)
QueryHead(db,'l99m',2)
QueryHead(db,'l99m',3)
"""