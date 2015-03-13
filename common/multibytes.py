#!/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import zenhan

import jctconv

class BaseBytes(object):
    @staticmethod
    def convert2unicode(strings):
        """ 引数を unicode にする。unicode だったら何もしない """
        if isinstance(strings, str):
            strings = strings.decode('utf-8')

        return strings

    @staticmethod
    def normalize(strings, unistr = 'NFKC'):
        """ 引数を normalize する。"""
        strings = BaseBytes.convert2unicode(strings)
        return unicodedata.normalize(unistr, strings)


class MultiBytes(BaseBytes):

    """
    マルチバイト系の変換メソッド

        c.f.
          http://atasatamatara.hatenablog.jp/entry/2013/04/15/201955
    """

    @staticmethod
    def zenNum2hanNum(str):
        """
        全角数字を半角数字に変換する
        その他の文字はそのまま
        """
        str = MultiBytes.convert2unicode(str)
        return zenhan.z2h(str, mode=2)


    @staticmethod
    def hanKana2zenKana(str):
        """
        半角カナを全角カナに変換する
        その他の文字はそのまま
        """

        str = MultiBytes.convert2unicode(str)
        return jctconv.h2z(str)


    @staticmethod
    def hira2kana(str):
        """
        全角ひらがなを全角カタカナに変換する
        その他の文字はそのまま

        http://d.hatena.ne.jp/mohayonao/20101213/1292237816
        """
        str = MultiBytes.convert2unicode(str)
        return jctconv.hira2kata(str)


##################################################

if __name__ == '__main__':
    import unittest

    class MultiByteTest(unittest.TestCase):
        def test_zenNum2hanNum(self):
            self.assertEqual(u'123', MultiBytes.zenNum2hanNum('１２３'))
            self.assertEqual(u'123', MultiBytes.zenNum2hanNum(u'１２３'))

            self.assertEqual(u'あいうえお123かきくけこ', MultiBytes.zenNum2hanNum(u'あいうえお１２３かきくけこ'))
            self.assertEqual(u'あいうえお123かきくけこ', MultiBytes.zenNum2hanNum('あいうえお１２３かきくけこ'))
            self.assertEqual(u'あい1うえ2お1か', MultiBytes.zenNum2hanNum(u'あい1うえ２お１か'))

            self.assertEqual(u'1aAａＡ23', MultiBytes.zenNum2hanNum(u'1aAａＡ２3'))
            self.assertEqual(u'1aAａＡ23', MultiBytes.zenNum2hanNum(u'1aAａＡ23'))

            self.assertEqual(u'123ー4567', MultiBytes.zenNum2hanNum('１２３ー４５６７'))


        def test_hanKana2zenKana(self):
            self.assertEqual(u'アアア', MultiBytes.hanKana2zenKana(u'ｱｱｱ'))
            self.assertEqual(u'アアア', MultiBytes.hanKana2zenKana('ｱｱｱ'))
            self.assertEqual(u'アアア', MultiBytes.hanKana2zenKana(u'アアア'))
            self.assertEqual(u'アアア', MultiBytes.hanKana2zenKana('アアア'))

            self.assertEqual(u'あああ', MultiBytes.hanKana2zenKana(u'あああ'))
            self.assertEqual(u'1２3', MultiBytes.hanKana2zenKana(u'1２3'))
            self.assertEqual(u'1２3', MultiBytes.hanKana2zenKana('1２3'))
            self.assertEqual(u'オオ１ａaAＡ漢！”＃＄％', MultiBytes.hanKana2zenKana(u'ｵオ１ａaAＡ漢！”＃＄％'))

        def test_hira2kana(self):
            self.assertEqual(u'アアア', MultiBytes.hira2kana(u'あああ'))
            self.assertEqual(u'アアア', MultiBytes.hira2kana(u'アアア'))
            self.assertEqual(u'1２ｱ', MultiBytes.hira2kana(u'1２ｱ'))

    unittest.main()
