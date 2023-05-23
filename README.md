# LifeRecorder
OOAD 專題

kivymd 文件
https://kivymd.readthedocs.io/en/1.1.1/getting-started/

下載專案
```
git clone https://github.com/OOAD-LifeRecorder/LifeRecorder.git
```

初次使用
```
pip install -r requirements.txt
```

執行專案
```
python3 MainApp.py
```

## 簡單的 git 教學
若需要修改或添加專案，請另外開 branch 去修改再合回來 （**請不要直接在 main 上修改**）
```
git checkout -b <branch_name>
```

切換 branch
```
git checkout <branch_name>
```

上傳的步驟
```
1. git add . (. 代表全部 若要單獨上傳 files 的話 就輸入檔名)
2. git commit -m "輸入這個 commit 主要的目的" （commit 是只會在本地上）
3. git push (會上傳到 github 上， 第一次 push 會需要加上其他的，command line 會提示，直接複製就好)
```

發 Pull Request
1. 在 GitHub 上選擇 Pull Request -> Create Pull Request -> 選擇 (main <- 你的 branch)
2. 有 conflict 就請自行解決， 若涉及別人的 code，請找當事人解決
3. 接著合回去就好
