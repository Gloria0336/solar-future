# Metaverse Sim UI Test

使用 Next.js 14（App Router）建置的「測試用 UI 整合」專案骨架，可在瀏覽器中查看最小引擎互動。

## 安裝

```bash
npm install
```

## 開發模式

```bash
npm run dev
```

啟動後打開瀏覽器：`http://localhost:3000`

## 專案重點

- MapView：支援 zoom 0/1/2 顯示不同層級內容
- StatusPanel：顯示 tick、位置、credits、energy、mode
- EventLog：最多顯示最近 30 行
- ActionPanel：可觸發打工、移動、戰鬥模式切換、存檔/讀檔
- 存檔：`localStorage` key `metaverse_save_1`
