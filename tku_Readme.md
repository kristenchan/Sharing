# 台灣某一個行政區內的基地台資料

# 資料相關說明
1.資料時間 : 2017/04/1 - 2017/09/30 共六個月，每小時會有一筆紀錄
2.資料維度 : 
3.資料欄位說明 : 
  a. time : 
  a. bts_id : 此組資料 bts_id + cell_id 為一個unique id
  b. cell_id : 此組資料 bts_id + cell_id 為一個unique id
  c. dl_quailty : 每個測站每小時的信號品質 (該值越大表示？)
  d. dl_utilization :  下行頻譜使用率 (該值越大表示？)
  e. drop_rate : 斷線比率(斷線/總連線數) 

# Note
1. 因為需保密資料，所以這裡有遮蔽部分的資訊，遮蔽的資訊如下 : 
   a. 基地台經緯度 (資料中不提供經緯度等詳細座標資訊)
   b. 基地台 id (資料中的 bts_id ,cell_id 為假 id，但 bts_id ,cell_id 間的關係不影響 )
   c. kpi 的正確名稱 (資料中的 dl_quailty, dl_utilization, drop_rate 是使用相似名稱取代)
2. 資料間的關係 : 
   a. 一個 bts_id 下會有 2-3 個 cell_id
      e.g. http://www.commscope.com/uploadedImages/CommScopecom/Blog/Blog_Resources/Network%20Mod%20aerial%20view(1).jpg?n=2610
   b. drop_rate 和 dl_quailty 間有一定程度的關聯
      e.g. dl_quailty 下降到某個程度時 drop_rate 會上升 
3. Data Clean : 此組資料還需要處理遺失值
4. 專有名詞解釋
   a. 下行 : 基地台資料傳到手機，大部分人都是使用下行，少部分人如網紅需要上傳影片或...才會使用上行
   b. 頻譜 : 頻譜越寬傳資料的資源越多


# 有興趣且可能可以做的方向
1. drop_rate 和 dl_quailty 間的關係
2. 如何準確預測下一筆 dl_utilization

drop_rate  <->  E-RAB DR RAN  line講電話的時候會明顯感覺(互動影音) netfilx或kkbox因為有buffer fb或line文字會在短時間重建
dl_utilization  <->  E-UTRAN Avg PRB usage per TTI DL
dl_quailty  <->  Average_CQI