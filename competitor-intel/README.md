# 🔍 競合インテリジェンス バトルカード

競合他社の情報をブラウザから入力するだけで、プロフェッショナルな **PowerPoint バトルカード (PPTX)** を自動生成する Web アプリです。

---

## 📁 ディレクトリ構成

```
competitor-intel/
├── app.py                        # Web サーバー（Python 標準ライブラリのみ）
├── requirements.txt              # 依存パッケージ
├── Procfile                      # Heroku / Render 用起動コマンド
├── render.yaml                   # Render デプロイ設定
├── static/
│   └── index.html                # フロントエンド UI（単一ファイル）
├── scripts/
│   ├── generate_battlecard.py    # PPTX 生成エンジン
│   └── scrape_intel.py           # 競合情報スクレイパー（オプション）
└── config/
    └── competitors.json          # 競合情報の設定ファイル（オプション）
```

---

## 🚀 ローカルで起動する

### 1. リポジトリをクローン

```bash
git clone https://github.com/ryokutas/ai-marketer.git
cd ai-marketer/competitor-intel
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

> **requirements.txt の内容**
> - `python-pptx` — PPTX ファイル生成
> - `requests` — HTTP クライアント
> - `beautifulsoup4` — Web スクレイピング（オプション機能用）

### 3. サーバーを起動

```bash
python app.py
```

### 4. ブラウザで開く

```
http://localhost:8080
```

---

## 🖥️ 使い方

### ① 自社情報を入力する

画面上部の「自社情報」カードに以下を入力します。

| 項目 | 説明 | 例 |
|------|------|-----|
| **自社名** | 自社の会社・ブランド名 | 株式会社サンプル |
| **プロダクト・サービス名** | 比較対象の自社製品 | BtoB マーケティング SaaS |
| **独自の提供価値** | 自社の強みや差別化ポイント | 日本語対応・HubSpot の 1/3 の価格 |

「サンプルを入力」ボタンを押すと、デモ用データが自動入力されます。

---

### ② 競合を追加する

「＋ 競合を追加」ボタンを押すと競合入力カードが展開されます。1社につき以下の情報を入力できます。

| セクション | 項目 | 説明 |
|------------|------|------|
| **基本情報** | 競合名 | HubSpot、Salesforce など |
| | カテゴリ | マーケティングオートメーション など |
| **価格・プラン** | 価格情報 | 1行1プランで入力 |
| **機能・メッセージング** | 主な機能 | 1行1機能で入力 |
| | メインヘッドライン | 競合のキャッチコピー |
| | サブヘッドライン | サブコピー |
| | キーメッセージ | 訴求ポイント（1行1件） |
| | CTA | 行動喚起ボタン（1行1件） |
| **最近の変化** | 最近の動向 | 値下げ、新機能、UI改善など（1行1件） |
| **強み・弱み** | 強み / 弱み | 各1〜3件程度 |
| **推奨アクション** | 対抗策 | 自社がとるべき営業・マーケ戦略 |

複数社を追加可能です。不要になったカードは「🗑 削除」ボタンで除去できます。

---

### ③ レポートを確認する（オプション）

「📄 テキストレポートを確認」ボタンを押すと、入力内容がページ下部にビジュアルレポートとして表示されます。印刷ボタンで PDF として保存することもできます。

---

### ④ PPTX を生成・ダウンロードする

「⚡ PPTX をダウンロード」ボタンを押すと、バックエンドで PowerPoint ファイルが生成され、自動的にダウンロードされます。

ファイル名は `battlecard_YYYYMMDD_HHMMSS.pptx` 形式で保存されます。

---

## 📊 生成される PPTX の構成

競合1社につき以下のスライドが生成されます：

1. **タイトルスライド** — 自社名・対象競合・生成日時
2. **競合概要** — カテゴリ・価格・主要機能
3. **メッセージング分析** — ヘッドライン・キーメッセージ・CTA
4. **最近の変化** — 直近の動向まとめ
5. **強み・弱み** — 競合の SWOT 的分析
6. **推奨アクション** — 営業・マーケへの提言

---

## ☁️ クラウドにデプロイする

### Render（無料プランあり）

1. [Render](https://render.com) にサインアップ
2. 「New Web Service」→ GitHub リポジトリ（`ryokutas/ai-marketer`）を選択
3. Root Directory に `competitor-intel` を指定
4. 自動的に `render.yaml` の設定が読み込まれます
5. 「Create Web Service」でデプロイ完了

デプロイ後は `https://[サービス名].onrender.com` でアクセスできます。

### その他のプラットフォーム

`Procfile` に `web: python app.py` が設定されているため、**Heroku** や **Railway** でもそのままデプロイできます。

---

## ⚙️ 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `PORT` | サーバーのリッスンポート | `8080` |

---

## 🛠️ 技術スタック

| レイヤー | 技術 |
|----------|------|
| フロントエンド | HTML / CSS / Vanilla JS（単一ファイル、外部依存なし） |
| バックエンド | Python 標準ライブラリ (`http.server`) |
| PPTX 生成 | `python-pptx` |
| デプロイ | Render / Heroku / Railway |

---

## 📝 データ形式（上級者向け）

`scripts/generate_battlecard.py` を直接実行することも可能です。

```bash
python scripts/generate_battlecard.py --input reports/intel_data.json
```

入力 JSON の形式：

```json
{
  "generated_at": "2026-03-23T...",
  "my_company": {
    "name": "自社名",
    "product": "製品名",
    "unique_value": "独自の提供価値"
  },
  "competitors": [
    {
      "id": "hubspot",
      "name": "HubSpot",
      "category": "マーケティングオートメーション",
      "pricing": ["Starter: $20/月", "Professional: $890/月"],
      "features": ["CRM統合", "メールオートメーション"],
      "messaging_headline": "あなたのビジネスを成長させる",
      "key_messages": ["使いやすいUI", "充実したサポート"],
      "ctas": ["無料で始める", "デモを見る"],
      "recent_changes": ["Starter プランを値下げ", "AI機能を追加"],
      "strengths": ["豊富な機能", "ブランド認知"],
      "weaknesses": ["高価格帯", "カスタマイズが複雑"],
      "recommended_action": "価格と日本語サポートで差別化する"
    }
  ]
}
```
