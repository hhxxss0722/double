#coding:utf-8
import math
class Convert62():
    def __init__(self):
        self.initcharset()

    def initcharset(self):
        self.charSet=[]
        slist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        for e in slist:
            self.charSet.append(e)

    #将指定数字转换为指定长度的62进制 
    def ConvertTo62(self,value,length):
        sixtyNum = ""
        if value < 62:
                sixtyNum = str(self.charSet[value]).zfill(length)
        else:
            result = value
            while result > 0:
                val = result % 62
                sixtyNum = self.charSet[val] + sixtyNum
                result = result // 62
            sixtyNum = sixtyNum.zfill(length)
        return sixtyNum

    def SixtyTwoScale(self,value):
        imei = ""
        length = len(value)
        result = 0
        for i in range(0,length):
            val = math.pow(62, (length - i - 1))
            c = value[i]
            tmp = self.charSet.index(c)
            result += tmp * val
        imei = str(int(result))
        return imei

class GetTboxNumber():
    def __init__(self):
        self.head="CTJX"
        self.c62=Convert62()

    #获取6位长度的62进制码
    #v输入的9位IMEI数据
    #返回长度为6的62进制码，高数位不足补0
    def GetDUT62(self,v,length):
        code = ""
        s = self.c62.ConvertTo62(v, length)
        code = s[3:10]
        return code
    #将后四位的数字转化为16进制字符串
    #lastcode 四位数字
    #返回16进制码
    def Get16(self,lastcode):
        code = ""
        code = hex(lastcode)
        code = code.zfill(4)
        return code

    def GetTboxFullCode(self,imei,c4):
        fc = ""
        fc += self.head
        code = self.GetDUT62(imei, 9)
        lc =hex(c4)[2:]
        lc=lc.zfill(4)
        fc += code + "-" + lc
        return fc
    #根据输入的SN，按照算法解析出IMEI
    #CTJX0sdmAS-1067
    #sn 待解析字符串
    #返回imei
    def GetTboxImei(self,sn):
        imei = ""
        c62 = sn[4:10]
        imei += "86"
        imei += self.c62.SixtyTwoScale(c62)
        slist=sn.split('-')
        l4 = slist[1]
        imei += str(int(l4,16))
        return imei
        
"""
imei="868074020985707"
simei=imei[2:11]
print('simei:',simei)
lcode=imei[11:]
print('locde:',lcode)
icode=int(simei)
c4=int(lcode)
g=GetTboxNumber()
sn=g.GetTboxFullCode(icode,c4)
print('sn:',sn)
g=GetTboxNumber()
sn="CTJX0sdmAS-1067"
imei=g.GetTboxImei(sn)
print(imei)
        private static char[] charSet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".ToCharArray();

        /// <summary> 
        /// 将指定数字转换为指定长度的62进制 
        /// </summary> 
        /// <param name="value">要转换的数字</param> 
        /// <param name="length">需要的长度</param> 
        /// <returns>62进制表示格式</returns> 
        public static string ConvertTo62(long value, int length)
        {
            string sixtyNum = string.Empty;
            if (value < 62)
            {
                sixtyNum = charSet[value].ToString().PadLeft(length, '0');
            }
            else
            {
                long result = value;
                while (result > 0)
                {
                    long val = result % 62;
                    sixtyNum = charSet[val] + sixtyNum;
                    result = result / 62;
                }
                sixtyNum = sixtyNum.PadLeft(length, '0');
            }
            return sixtyNum;
        } 

        public static string SixtyTwoScale(string value)
        {
            string imei = string.Empty;
            int length = value.Length;
            Int64 result = 0;
            for (int i = 0; i < length; i++)
            {
                 Int64 val = (Int64)Math.Pow(62, (length - i - 1));
                 char c = value[i];
                 Int64 tmp = Array.IndexOf(charSet,c);
                 result += tmp * val;
             }
             imei = result.ToString();
             return imei;
        }
    }

    public class GetTboxNumber 
    {
        private static string head = "CTJX";
        /// <summary>
        /// 获取6位长度的62进制码
        /// </summary>
        /// <param name="v">输入的9位IMEI数据</param>
        /// <returns>返回长度为6的62进制码，高数位不足补0</returns>
        private static string GetDUT62(long v,int length) 
        {
            string code = string.Empty;
            string s = Convert62.ConvertTo62(v, length);
            code = s.Substring(3, 6);
            //code = new string(code.ToCharArray().Reverse().ToArray());
            return code;
        }
        /// <summary>
        /// 将后四位的数字转化为16进制字符串
        /// </summary>
        /// <param name="lastcode">四位数字</param>
        /// <returns>返回16进制码</returns>
        private static string Get16(int lastcode) 
        {
            string code = string.Empty;
            code = Convert.ToString(lastcode, 16);
            code = code.PadLeft(4, '0');
            return code;
        }

        public static string GetTboxFullCode(long imei,int c4) 
        {
            string fc = string.Empty;
            fc += head;
            string code = GetDUT62(imei, 9);
            string lc = Convert.ToString(c4,16);
            lc=lc.PadLeft(4, '0');
            fc += code + "-" + lc;
            return fc;
        }
        /// <summary>
        /// 根据输入的SN，按照算法解析出IMEI
        /// </summary>
        ///  CTJX0sdmAS-1067
        /// <param name="sn"></param>
        /// <returns></returns>
        public static string GetTboxImei(string sn) 
        {
            string imei = string.Empty;
            string c62 = sn.Substring(4,6);
            imei += "86";
            imei += Convert62.SixtyTwoScale(c62);
            string l4 = sn.Substring(sn.IndexOf('-') + 1, 4);
            imei += (Convert.ToInt32(l4, 16)).ToString();
            return imei;
        }
    }
"""
