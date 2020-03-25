import requests
import json

# 컨디션을 만족하지 않으면 -1 만족하면 remain값 반환
def chkCondition(data,condition):
    try:
        remain = data['remain_stat'];
    except KeyError:
        remain = ""

    if remain == "plenty":
        remain = "100개 이상";
    elif remain == "some":
        if condition < "2":
            return "-1";
        remain = "30개 이상 100개 미만";
    elif remain == "few":
        if condition < "3":
            return "-1";
        remain = "2개 이상 30개 미만";
    elif remain == "empty":
        if condition < "4":
            return "-1";
        remain = "1개 이하";
    elif remain == "break":
        if condition < "4":
            return "-1";
        remain = "판매 중지";
    else:
        if condition < "4":
            return "-1";
        remain = "정보없음";

    return remain;

url = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json/?address='
conditions = ["1","2","3","4"];

print("----------------------------------------------------------------------------------");
print("-------------------공적마스크 판매처 및 개조 현황 조회 프로그램----------------------");
print("----------------------------------------------------------------------------------");

while True:
    print("==================================================================================");
    print("주소를 기준으로 해당 구 또는 동내에 존재하는 판매처 및 재고 상태 등의 판매 정보 제공."
          + "\n예- '서울특별시 강남구' or '서울특별시 강남구 논현동'"
          + "\n('서울특별시' 와 같이 '시'단위만 입력하는 것은 불가능합니다.)"
          + "\n프로그램 종료를 위해서는 'quit'을 입력해 주시기 바랍니다.");
    print("==================================================================================");
    print("주소 입력: ");
    addr = str(input());
    print("==================================================================================");
    print("검색 조건을 설정. 기본값은 4입니다."
          + "\n 1: 100개 이상"
          + "\n 2: 30개 이상"
          + "\n 3: 2개 이상"
          + "\n 4: 모두");
    print("==================================================================================");
    print("검색 조건: ")
    condition = str(input());
    print("==================================================================================");

    if addr == "quit":
        break;

    if condition not in conditions:
        condition = "4";

    res = requests.get(url+str(addr));
    json_data = json.loads(res.text);

    for data in json_data['stores']:

        remain = chkCondition(data, condition);
        if remain == "-1":
            continue;

        try:
            print("판매처 이름: "+str(data['name']));
        except KeyError:
            print("판매처 이름: ");
        try:
            print("판매처 주소: "+str(data['addr']));
        except KeyError:
            print("판매처 주소: ");
        try:
            print("입고일시: "+str(data['stock_at']));
        except KeyError:
            print("입고일시: ");

        print("재고 상태: "+str(remain));
        print("----------------------------------------------------");

