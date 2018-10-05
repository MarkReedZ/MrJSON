# coding=UTF-8

import mrjson as j
import json
import inspect

def raises( o, f, exc,details ):
  try:
    f(o)
    if len(o) > 100: o = o[:100]
    print("ERROR ", o, " didn't raise exception")
  except Exception as e:
    if len(o) > 100: o = o[:100]
    if type(e) != exc:
      print("ERROR",o," rose wrong exception",type(e),e)
    if str(e) != details:
      print("ERROR",o," rose wrong exception details actual vs expected:\n",e,"\n",details)

def eq( a, b ):
  if a != b:
    cf = inspect.currentframe()
    print( "ERROR Line", cf.f_back.f_lineno, a, "!=", b )
    return -1
  return 0


print("Running tests...")

#
jtxt = '[[{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0},{"c":"blw_2IgLc","up":true,"type":"upv","s":0,"t":0}],{"username":"1","id":1}]'
j.loads(jtxt)

tsts =[
 [ {1:2}, '{"1":2}' ],
 [ [0,0,1], "[0,0,1]" ],
 [ [-1.002,0,1], "[-1.002,0,1]" ],
 [ [-1,0,1], "[-1,0,1]" ],
 [ ["string",0,float("inf")], '["string",0,Infinity]' ],
 [ {"string":True,"b":False}, '{"string":true,"b":false}'],
 [ {"type":"add","s":0,"t":0,"c":199454061429160,"p":0,"au":"6133","uid":6133,"ago":"1 hour ago","txt":"Floors bulkhead a tongues gage patrols winter gage records. Because. This stuffing airspeeds submarines farm marks cloud specialists coughs disasters. Shortage this democracy cameras have pulls shoe personality. Fishes jurisdiction problem crowd cash rebounds how well braces."}, '{"type":"add","s":0,"t":0,"c":199454061429160,"p":0,"au":"6133","uid":6133,"ago":"1 hour ago","txt":"Floors bulkhead a tongues gage patrols winter gage records. Because. This stuffing airspeeds submarines farm marks cloud specialists coughs disasters. Shortage this democracy cameras have pulls shoe personality. Fishes jurisdiction problem crowd cash rebounds how well braces."}' ],
]

for t in tsts:
  eq( j.dumps(t[0]), t[1] )

objs = [
[float("inf"),2],
[1,float("-inf"),2],
-1, 12, 1,
-132123123123,
1.002, -1.31,
-312312312312.31,
2**31, 2**32, 2**32-1,
1337E40, 1.337E40, 3937e+43, 7e+3, 
7e-3, 1e-1, 1e-4,
[1, 2, 3, 4],
[1, 2, 3, [4,5,6,7,8]],
{"k1": 1, "k2": 2, "k3": 3, "k4": 4},
'\u273f\u2661\u273f',  # ✿♡✿
{},
"\x00", "\x19", 
"afsd \x00 fdasf",
"\xe6\x97\xa5\xd1\x88",
"\xf0\x90\x8d\x86",
"\xf3\xbf\xbf\xbffadfadsfas",
"fadsfasd\xe6\x97\xa5\xd1\x88",
[[[[]]]] * 20,
[31337.31337, 31337.31337, 31337.31337, 31337.31337] * 10,
{'a': -12345678901234.56789012},
"fadfasd \\ / \r \t \n \b \fxx fadsfas",
"这是unicode吧你喜欢吗？我的中文最漂亮",
["别","停","believing", -1,True,"zero",False, 1.0],
None, True,False,float('inf'),
[18446744073709551615, 18446744073709551615, 18446744073709551615],
]

# NaN != Nan so check str rep
o = j.loads( j.dumps( float('nan') ) )
eq( str(o), 'nan' )


for o in objs:
  try:
    eq( o, j.loads(j.dumps(o)) )
  except Exception as e:
    print( "ERROR",str(e), o )


print("Testing Exceptions..")
raises( "NaNd",         j.loads, ValueError, "Expecting 'NaN' at pos 0" )
raises( '"',            j.loads, ValueError, "Unterminated string starting at 0")
raises( "[",            j.loads, ValueError,  "Unexpected end of json string - could be a bad utf-8 encoding or check your [,{,\"")
raises( "]",            j.loads, ValueError, "Closing bracket ']' without an opening bracket at pos 0" )
raises( "{",            j.loads, ValueError,  "Unexpected end of json string - could be a bad utf-8 encoding or check your [,{,\"")
raises( "}",            j.loads, ValueError, "Closing bracket '}' without an opening bracket at pos 0")
raises( "[1,2,,]",      j.loads, ValueError, "Unexpected character ',' at pos 5")
raises( "[1,z]",        j.loads, ValueError, "Unexpected character at pos 3")
raises( "[1:,z]",       j.loads, ValueError, "Unexpected character ':' while parsing JSON string at pos 2")
raises( "[1,2}]",       j.loads, ValueError, "Closing bracket '}' without an opening bracket at pos 4")
raises( '{"foo":1]',    j.loads, ValueError, "Mismatched closing bracket, expected a }")
raises( '{"foo"}:2}',   j.loads, ValueError, 'Expected a "key":value, but got a closing bracket \'}\' at pos 6')
raises( '{"foo":}2}',         j.loads, ValueError, 'Expected a "key":value, but got a closing bracket \'}\' at pos 7')
raises( "["*(1024*1024),      j.loads, ValueError, "Too many nested objects, the max depth is 32")
raises( "-[1,2]",             j.loads, ValueError, "Saw a - without a number following it at pos 0")
raises( "123[1,2]",           j.loads, ValueError, "A number must be followed by a delimiter at pos 2")
raises( '[1,2,"yay\\u232G]',  j.loads, ValueError, "Unicode escape malformed at pos 9")
raises( '"yay\ztest"',        j.loads, ValueError, "Unexpected escape character 'z' at pos 4")
raises( 'truez',              j.loads, ValueError, "Expecting 'true' at pos 0")
raises( 'fals',               j.loads, ValueError, "Expecting 'false' at pos 0")
raises( 'nul',                j.loads, ValueError, "Expecting 'null' at pos 0")
raises( 'Infinty',            j.loads, ValueError, "Expecting 'Infinity' at pos 0")
raises( '-Infinit',           j.loads, ValueError, "Expecting '-Infinity' at pos 0")


# Check bytes 
for o in objs:
  try:
    eq( o, j.loadb(j.dumpb(o)) )
  except Exception as e:
    print( "ERROR Unexpected exception: ",str(e), "on object ", o, "json bytes",j.dumpb(o) )


eq( j.dumpb(1), b'1' )
raises( "NaNd",    j.loadb, TypeError, "Expected bytes, use loads for a unicode string" )  

class JSONTest:
  def __json__(self):
    return '{"k":"v"}'
eq( j.dumps({u'key': JSONTest()}),'{"key":{"k":"v"}}')

print("Trying JSONTestSuite")
from os import walk
for (dirpath, dirnames, filenames) in walk("test_data"):
  for fn in filenames:
    if not "invalid" in fn: continue
    f = open( "test_data/"+fn,"rb")
    try:
      #print(fn)
      o = j.load(f)
    except Exception as e:
      if fn[0] != 'n':
        print( "ERROR",str(e), fn )
      continue

    try:
      eq( o, j.loads(j.dumps(o)) )
      if fn[0] == 'n':
        print( "ERROR Should have thrown an exception:", fn )
    except Exception as e:
      if fn[0] != 'n':
        print( "ERROR",str(e), o, fn )


print("Done")
