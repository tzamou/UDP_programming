# UDP_programming
網路程式設計CBD109035陳冠霖  

## How to used：
1__init__.py放在python 中site-packages/gym/envs裡面(替換掉原本的__init__.py)  
2.bouncyball也放在python 中site-packages/gym/envs裡面(新增這個資料夾)  

## How to train:
run train.py  
然後底下algo=Algorithm()下面輸入 
algo.train()  

## How to play:
1.run server.py  
2.run client.py  
tips:
按左右鍵可以往做＝左或往右(操作很難 我故意的)  
按p可以停止/播放音樂  
按a可以自動接球(推薦這個 遊戲已經變成AI的形狀了)  
按m可以手動操作  

## packages
pip install gym  
pip install pygame  
pip install stable_baselines3  
pip install sb3_contrib  

## other
只有兩個禮拜時間要寫code 拍影片 剪輯所以時間不太夠，程式碼可能有bug請見諒  
本來要加fuzzy的 但沒時間了 哭阿  

## 0614update
教完報告後想新增的東西就隨便寫一下  
todo:  
1.訓練紀錄還有每2000000step儲存一次模型  
2.環境更新  
3.想要加fuzzy  
4.遊戲規則再難一點  
