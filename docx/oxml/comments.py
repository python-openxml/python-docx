"""
Custom element classes related to the comments part
"""

from . import OxmlElement
from .simpletypes import ST_DecimalNumber, ST_String
from .xmlchemy import (
	BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne
)

class CT_Com(BaseOxmlElement):
	"""
	A ``<w:comment>`` element, a container for Comment properties 
	"""
	initials = RequiredAttribute('w:initials', ST_String)
	_id = RequiredAttribute('w:id', ST_DecimalNumber)
	date = RequiredAttribute('w:date', ST_String)
	author = RequiredAttribute('w:author', ST_String)
	
	paragraph = ZeroOrOne('w:p', successors=('w:comment',))

	@classmethod
	def new(cls, initials, comm_id, date, author):
		"""
		Return a new ``<w:comment>`` element having _id of *comm_id* and having
		the passed params as meta data 
		"""
		comment = OxmlElement('w:comment')
		comment.initials = initials
		comment.date = date
		comment._id = comm_id
		comment.author = author

		return comment
	def _add_p(self):
		_p = OxmlElement('w:p')
		self._insert_paragraph(_p)
		return _p

class CT_Comments(BaseOxmlElement):
	"""
	A ``<w:comments>`` element, a container for Comments properties
	"""
	comment = ZeroOrMore ('w:comment', successors=('w:comments',))

	def add_comment(self,author, initials, date):
		_next_id = self._next_commentId
		comment = CT_Com.new(initials, _next_id, date, author)
		comment = self._insert_comment(comment)

		return comment
	
	@property
	def _next_commentId(self):
		ids = self.xpath('./w:comment/@w:id')
		len(ids)
		_ids = [int(_str) for _str in ids]
		_ids.sort()

		print(_ids)
		try:
			return _ids[-1] + 2
		except:
			return 0
	

