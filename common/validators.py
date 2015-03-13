#!/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import unicodedata


class CMNValid(object):
    """
    Common Validation Class
        validationに徹するべきなので、str.strip() とかはやらず、
        引数を愚直にvalidateするだけ
    """

    @staticmethod
    def isValid_withCharType(str, comparedType):
        """型を指定して validateする"""

        strtype = type(str)
        if strtype == str:
            str_unicode = unicode(str)
        elif strtype == unicode:
            str_unicode = str
        else:
            return False

        for c in str_unicode:
            if unicodedata.name(c).split()[0] != comparedType:
                return False

        return True


    @staticmethod
    def isValid_katakana(str):
        """引数がカタカナのみなら Trueを返す"""

        return CMNValid.isValid_withCharType(str, 'KATAKANA')


    @staticmethod
    def isValid_date(year, month, day):
        """正しい年月日なら True を返す"""

        try:
            datetime.datetime(int(year),int(month),int(day))
            return True
        except ValueError:
            return False


    @staticmethod
    def isValid_zip(str):
        """正しい郵便番号なら True を返す"""

        ptn = re.compile(r'^\d{3}-?\d{4}$')
        if ptn.search(str):
            return True

        return False


    @staticmethod
    def isValid_tel(str):
        """正しい電話番号なら True を返す"""

        ptns = []
        ptns += [re.compile(r'^\d{2}-?\d{4}-?\d{4}$')]
        ptns += [re.compile(r'^\d{3}-?\d{3,4}-?\d{4}$')]
        ptns += [re.compile(r'^\d{4}-?\d{2}-?\d{4}$')]
        ptns += [re.compile(r'^\d{4}-?\d{3}-?\d{3}$')]
        ptns += [re.compile(r'^\d{5}-?\d{1}-?\d{4}$')]

        for ptn in ptns:
            if ptn.search(str):
                return True

        return False



if __name__ == '__main__':
    import unittest

    class ValidatorTests(unittest.TestCase):

        def test_isValid_katakana(self):
            str1 = u'アイウエオカキクケコサシスセソタチツテト'
            str2 = u'ナニヌネノハヒフヘホマミムメモヤユヨワオンャュョ'
            str_h = u'あいうえお'
            str_n = '123'

            isValid_katakana = CMNValid.isValid_katakana

            self.assertTrue(isValid_katakana(str1))
            self.assertTrue(isValid_katakana(str2))
            self.assertTrue(isValid_katakana(str1+str2))

            self.assertFalse(isValid_katakana(123))
            self.assertFalse(isValid_katakana(str_h))
            self.assertFalse(isValid_katakana(unicode(str_h)))
            self.assertFalse(isValid_katakana(str_n))
            self.assertFalse(isValid_katakana(str1+str_h))
            self.assertFalse(isValid_katakana(str1+str_n))


        def test_date(self):
            isValid_date = CMNValid.isValid_date

            self.assertTrue(isValid_date(2015, 1, 1))
            self.assertTrue(isValid_date(2015, 12, 31))
            self.assertTrue(isValid_date(2016, 2, 28))
            self.assertTrue(isValid_date(2016, 2, 29))

            self.assertFalse(isValid_date(2015, 13, 1))
            self.assertFalse(isValid_date(2015, 12, 32))
            self.assertFalse(isValid_date(2015, 2, 29))


        def test_zip(self):
            isValid_zip = CMNValid.isValid_zip
            self.assertTrue(isValid_zip('105-0011'))
            self.assertTrue(isValid_zip('1050011'))

            self.assertFalse(isValid_zip('abc-defg'))
            self.assertFalse(isValid_zip('105--0011'))
            self.assertFalse(isValid_zip('105-00111'))
            self.assertFalse(isValid_zip('10500111'))
            self.assertFalse(isValid_zip('105 0011'))
            self.assertFalse(isValid_zip('105 001'))
            self.assertFalse(isValid_zip('10-001'))
            self.assertFalse(isValid_zip('0105-0011'))
            self.assertFalse(isValid_zip('105-00111'))
            self.assertFalse(isValid_zip('105'))


        def test_tel(self):
            isValid_tel = CMNValid.isValid_tel

            self.assertTrue(isValid_tel('03-1234-5678'))
            self.assertTrue(isValid_tel('090-1234-5678'))
            self.assertTrue(isValid_tel('90-1234-5678'))
            self.assertTrue(isValid_tel('0120-123-456'))

            self.assertTrue(isValid_tel('0312345678'))
            self.assertTrue(isValid_tel('09012345678'))
            self.assertTrue(isValid_tel('0120123456'))

            self.assertTrue(isValid_tel('03-12345678'))
            self.assertTrue(isValid_tel('090-12345678'))
            self.assertTrue(isValid_tel('0120-123456'))

            self.assertTrue(isValid_tel('031234-5678'))
            self.assertTrue(isValid_tel('0901234-5678'))
            self.assertTrue(isValid_tel('0120123-456'))

            self.assertFalse(isValid_tel('03 1234 5678'))
            self.assertFalse(isValid_tel('1234-5678'))
            self.assertFalse(isValid_tel('123-456-789'))



    unittest.main()

