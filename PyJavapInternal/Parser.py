__author__ = 'jasonlee'

import os.path
import os
from PyJavapInternal.ParsingResult import ParsingResult
from PyJavapInternal.ParsingException import ParsingException
from PyJavapInternal import ByteToDec
from PyJavapInternal.ConstantPool import ConstantPool

class Parser:


    def __init__(self, cls_file_name):
        self.cls_file_name = cls_file_name
        self.result = ParsingResult(self.cls_file_name)
        self.clsFile = None

    def __verify(self):
        """
        Verify the given arguments.
        """

        if not (os.path.exists(self.cls_file_name) and os.path.isfile(self.cls_file_name)):
            raise ParsingException("Can't find the class file %s" % self.cls_file_name)

    def __parseMagicNum(self):
        """
        Parse the magic num (the first 4 bytes)
        """

        assert self.clsFile is not None

        # get first four bytes
        magicNumBytes = self.clsFile.read(4)
        self.result.setMagicNumber(magicNumBytes)

    def __parseVersion(self):
        """
        Parse the version of this class file.
        Version is composed by minor version and major version.
        Each will occupy 2 bytes.
        """

        assert self.clsFile is not None

        minorVerBytes = self.clsFile.read(2)
        majorVerBytes = self.clsFile.read(2)

        self.result.setVersion(ByteToDec(minorVerBytes), ByteToDec(majorVerBytes))

    def __parseConstantPool(self):
        """
        Parse the constant pool of class file
        First 2 bytes of this section is the count.
        Pay attention here. Constant index starts from 1, not 0.
        """

        assert self.clsFile is not None

        const_count = ByteToDec(self.clsFile.read(2)) - 1
        self.result.setConstPoolCount(const_count)

        constants = ConstantPool.parse(const_count, self.clsFile)
        self.result.setConstants(constants)


    def __parseAccessFlag(self):
        """
        Parse the access flag
        """

        assert self.clsFile is not None

        accessFlag = ByteToDec(self.clsFile.read(2))
        self.result.setAccessFlag(accessFlag)

    def __parseThis(self):
        """
        Parse "this" section
        """

        assert self.clsFile is not None

        thisIndex = ByteToDec(self.clsFile.read(2))
        self.result.setThisIndex(thisIndex)

    def __parseSuper(self):
        """
        Parse "super" section
        """

        assert self.clsFile is not None

        superIndex = ByteToDec(self.clsFile.read(2))
        self.result.setSuperIndex(superIndex)

    def __parseInterface(self):
        """
        Parse "interface" section
        """

        assert self.clsFile is not None

        interfaceCount = ByteToDec(self.clsFile.read(2))

        interfaceIndex = []
        if interfaceCount > 0:
            for i in range(interfaceCount):
                interfaceIndex.append(ByteToDec(self.clsFile.read(2)))

        self.result.setInterfaces(interfaceCount, interfaceIndex)

    def parse(self):

        try:
            self.__verify()

            # parse the magic number of class file
            self.clsFile = open(self.cls_file_name, 'rb')

            # following functions' order is very important
            self.__parseMagicNum()
            self.__parseVersion()
            self.__parseConstantPool()
            self.__parseAccessFlag()
            self.__parseThis()
            self.__parseSuper()
            self.__parseInterface()

        except ParsingException,e:

            raise e

        finally:
            if self.clsFile:
                self.clsFile.close()
                self.clsFile = None

        return self.result


