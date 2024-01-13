## 初回環境構築
```
$ make init
```

## Dev Containers起動
DockerコンテナとVSCodeの統合を行います。<br>
これによってDockerコンテナ内のファイルに対してVSCodeからアクセスできます。

- `Cmd/Ctrl + Shift + P`でコマンドパレットを開き、`Dev-Containers: Open Folder in Container`を選択。
- プロジェクトフォルダ`python`を選択（compose.ymlファイルを配置しているフォルダ）。

## Dev Containers終了・再開
### 終了
```
$ make down
```
### 再開
VSCode左下の`開発コンテナー`をクリックし、`ウィンドウの再読み込み`を選択。
