import os

import pytest

from src.armajor import ArabicMnemonicMajor  # type: ignore


@pytest.fixture
def armajor():
    return ArabicMnemonicMajor(
        filename=os.path.join(os.path.dirname(__file__), "../src/words.txt")
    )


table = {
    "0": {"ماء", "داء"},
    "1": {"لا", "ناء"},
    "2": {"باء"},
    "3": {"ساء"},
    "4": {"ري"},
    "5": {"جاء"},
    "6": {"أضاء"},
    "7": {"وحي"},
    "8": {"هيئ"},
    "9": {"قيء", "فيء"},
    # below examples are taken from the book
    "00": {"دم"},
    "01": {"ندى"},
    "02": {"بوم"},
    "03": {"سد", "عود"},
    "04": {"ورم", "ورد"},
    "25": {"يخت"},
    "26": {"ضب"},
    "27": {"حب"},
    "28": {"هبة"},
    "29": {"قبة"},
    "50": {"مخ"},
    "51": {"ناجي"},
    "52": {"تاج"},
    "53": {"عاج"},
    "54": {"رجاء"},
    "75": {"جحا"},
    "76": {"أطاح"},
    "77": {"صوص"},
    "78": {"كح"},
    "79": {"قص"},
    "05": {"خد"},
    "06": {"ضم"},
    "07": {"صدأ"},
    "08": {"هدية"},
    "09": {"فم"},
    "10": {"دلو"},
    "11": {"ذيل"},
    "12": {"تل"},
    "13": {"غول"},
    "14": {"وزن"},
    "15": {"جن", "خوذة"},
    "16": {"ظل", "طاولة"},
    "17": {"حلوى", "صل"},
    "18": {"هول"},
    "19": {"فول"},
    "20": {"دب"},
    "21": {"لبوة"},
    "22": {"باب"},
    #'23': {'كعب'},
    #'24': {'ساعة'},
    "31": {"ولاعة"},
    "33": {"عش"},
    "34": {"وزغ"},
    "35": {"خس"},
    "36": {"طاووس"},
    "37": {"وحش"},
    "38": {"كأس"},
    "39": {"قوس"},
    "40": {"موز"},
    "41": {"نار", "لوز"},
    "42": {"بئر"},
    "43": {"سوار"},
    "44": {"رز"},
    "45": {"جرة"},
    "46": {"إطار"},
    "47": {"صرة"},
    "48": {"كرة"},
    "49": {"فأر"},
    "55": {"خوخ"},
    "56": {"ضخ"},
    "57": {"حاج"},
    "58": {"كجة"},
    "59": {"فخ"},
    "60": {"وميض"},
    "61": {"لوط"},
    "62": {"إبط", "بطة"},
    "63": {"سوط", "غطاء"},
    "64": {"أرض"},
    "65": {"خيط"},
    "66": {"وطواط"},
    "67": {"حائط"},
    "68": {"وهط"},
    "69": {"قط"},
    "70": {"دوح"},
    "71": {"لوح"},
    "72": {"باص"},
    "73": {"غواص", "وشاح"},
    "74": {"رحى"},
    "80": {"ديك"},
    "81": {"لهو"},
    "82": {"بكى"},
    "83": {"سواك"},
    "84": {"زكاة"},
    "85": {"وجه"},
    "86": {"طهي"},
    "87": {"صك"},
    "88": {"كيك"},
    "89": {"قهوة"},
    "90": {"دف"},
    "91": {"ناقة"},
    "92": {"بوق"},
    "93": {"سيف"},
    "94": {"ريق"},
    "95": {"خف"},
    "96": {"طوق", "طاف"},
    "97": {"صوف", "حافي"},
    "98": {"كف"},
    "99": {"قف"},
    "101": {"ليمون", "نمل"},
    "104": {"رمان"},
    "105": {"جمل"},
    "107": {"حامل"},
    "113": {"أسنان"},
    #'117': {'حديد'}, # 007
    "118": {"هلال"},
    "124": {"زيتون"},
    "125": {"جبن", "جبل"},
    #'126': {'صابون', 'طبل'}, # 127
    "127": {"حبل"},
    "131": {"لسان"},
    "133": {"غسالة", "عسل"},
    "143": {"غزال", "سروال"},
    "151": {"نخل"},
    "153": {"سجن"},
    "154": {"رجل"},
    "169": {"قطن"},
    "173": {"شاحنة"},
    "177": {"حصان", "صحن"},
    "197": {"حافلة"},
    #'207': {'صمغ', 'صداع'},
    "214": {"أرنب"},
    "219": {"قلب"},
    "226": {"طبيب"},
    "233": {"عشب"},
    "235": {"خشب"},
    "242": {"تراب"},
    "243": {"غراب"},
    "257": {"حجاب"},
    "273": {"سحاب"},
    "281": {"ذهب"},
    "283": {"شهاب"},
    "291": {"نقاب"},
    "302": {"تماس"},
    "303": {"شمس"},
    "305": {"جامع"},
    "324": {"ربع"},
    "327": {"إصبع"},
    "334": {"رشاش"},
    "340": {"درع"},
    "349": {"قرع", "فراش"},
    "371": {"نحاس"},
    "401": {"نمر"},
    "402": {"تمر"},
    "404": {"رادار"},
    "405": {"جدار", "خمر", "جمر"},
    "407": {"حمار"},
    "409": {"قمر"},
    "422": {"بيتزا"},
    "423": {"ستار", "غبار"},
    "425": {"جبيرة"},
    "430": {"ماعز"},
    "435": {"جسر"},
    "451": {"نجار"},
    "452": {"باخرة"},
    #'456': {'صخر'},
    "460": {"مطر"},
    "469": {"فطر"},
    "470": {"محار"},
    "472": {"بحر", "بحيرة"},
    "477": {"صحراء"},
    "481": {"نهر"},
    "486": {"ظهر"},
    "492": {"بقر"},
    "496": {"ظفر"},
    "499": {"قفز"},
    "542": {"برج"},
    "543": {"سرج"},
    "554": {"زجاج"},
    "613": {"سلطة"},
    "643": {"شريط"},
    #'699': {'قفص'}, # 799
    "723": {"شبح", "سبح"},
    "740": {"مروحة"},
    "745": {"جراح"},
    "774": {"رصاص"},
    "910": {"ملف"},
    "913": {"غلاف", "علف", "عنق"},
    "914": {"زلق"},
    "917": {"حلاق"},
    "928": {"هاتف"},
    "942": {"برق"},
    "979": {"قصف"},
}


def test_examples(armajor):
    for k, v in table.items():
        res = armajor.lookup(k)
        assert v <= res, (k, v, res)


def test_inverse_examples(armajor):
    for k, v in table.items():
        for i in v:
            r = armajor.word_to_num(i)
            assert r == k, (i, k, r)


def test_number_validation():
    clean_num = ArabicMnemonicMajor.clean_num
    assert clean_num(23) == "23"
    assert clean_num(-23) == "23"
    assert clean_num(" 23  ") == "23"
    assert clean_num(" 23.1") == "231"
    assert clean_num(" 23,1") == "231"
    assert clean_num("023") == "023"
    assert clean_num("00") == "00"
    assert clean_num("0.23") == "023"
    assert clean_num(" +23") == "23"
    assert clean_num(" -23 ") == "23"
    assert clean_num(" ۲۳") == "23"
    assert clean_num("  ") == ""
    assert clean_num("junk") == ""
    assert clean_num("23junk") == "23"
    assert clean_num("23junk32") == "2332"
