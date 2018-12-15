#coding:utf-8

class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

#import sys
#sys.modules[__name__] = _const()

const = _const()
const.VENDORPATH = "D:/dev/PycharmProjects/qicaixiang/qi/vendor/"
const.PLUGINSPATH = "D:/dev/PycharmProjects/qicaixiang/qi/plugins/"

#---------------------
#作者：tzw0745
#来源：CSDN
#原文：https://blog.csdn.net/my_precious/article/details/50954622
#版权声明：本文为博主原创文章，转载请附上博文链接！