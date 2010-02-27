#!/usr/bin/python

import epics

class Device(object):
    """A simple collection of related PVs, all sharing a prefix,
    but having many 'attributes'. This almost describes an
    Epics Record, but as it is concerned only with PV names,
    the mapping to an Epics Record is not exact.

    Many PVs will have names made up of prefix+attribute, with
    a common prefix for several related PVs.  This class allows
    this case to be represented simply such as with:

      >>> struck = epics.Device('13IDC:str:')
      >>> struck.put('EraseStart',1)
      >>> time.sleep(1)
      >>> struck.put('StopAll',1)
      >>> struck.get('mca1')

    This will put a 1 to 13IDC:str:EraseStart, wait, put a 1
    to 13IDC:str:StopAll, then read 13IDC:str:mca1

    The attribute PVs are built as needed and held in an internal
    buffer (self._pvs).  This class is kept intentionally simple
    so that it may be subclassed.

    To pre-load attribute names on initialization, provide a
    list or tuple of attributes:

      >>> struck = epics.Device('13IDC:str:',
      ...                       attrs=('ChannelAdvance',
      ...                              'EraseStart','StopAll'))
      >>> print struck.PV('ChannelAdvance').char_value
      'External'

    The prefix is optional, and when left off, this class can
    be used as an arbitrary container of PVs, or to turn
    any subclass into an epics Device:

      >>> class MyClass(epics.Device):
      ...     def __init__(self,**kw):
      ...         epics.Device.__init__() # no Prefix!!
      ...
      >>> x = MyClass()
      >>> pv_m1 = x.PV('13IDC:m1.VAL')
      >>> x.put('13IDC:m3.VAL', 2)
      >>> print x.PV('13IDC:m3.DIR').get(as_string=True)
    """
    def __init__(self,prefix=None,attrs=None):
        self.__prefix__ = prefix
        self._pvs = {}
        if attrs is not None:
            for p in attrs: self.PV(p)
        
    def PV(self,attr):
        """return epics.PV for a device attribute"""
        pvname = attr        
        if self.__prefix__ is not None: 
            pvname = "%s%s" % (self.__prefix__, attr)
        if pvname not in self._pvs:
            self._pvs[pvname] = epics.PV(pvname)
        return self._pvs[pvname]
    
    def put(self,attr,value,wait=False,timeout=10.0):
        """put an attribute value, 
        optionally wait for completion or
        up to a supplied timeout value"""
        return self.PV(attr).put(value,wait=wait,timeout=timeout)
        
    def get(self,attr,as_string=False):
        """get an attribute value, 
        option as_string returns a string representation"""
        return self.PV(attr).get(as_string=as_string)

