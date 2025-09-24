## 🛠️ 实现方案（GitHub Pages + dpdns.org）

### 1. 准备 GitHub 仓库

1. 新建一个 GitHub 仓库，比如叫 `qr-search`。
2. 在里面放置你的网页文件：
   - `index.html`（主页面）
   - `data.json`（存放你算好的数据）
   - `script.js`（查询逻辑）

📂 目录大概这样：

```
pgsql复制代码qr-search/
 ├─ index.html
 ├─ script.js
 └─ data.json
```

**示例 index.html（简化版）**

```
html复制代码<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>查询系统</title>
</head>
<body>
  <h1>同学查询系统</h1>
  <input id="query" placeholder="输入关键字">
  <button onclick="search()">查询</button>
  <pre id="result"></pre>

  <script src="script.js"></script>
</body>
</html>
```

**示例 script.js**

```
js复制代码async function search() {
  const key = document.getElementById("query").value.trim();
  const res = await fetch("data.json");
  const data = await res.json();

  let result = data[key];
  document.getElementById("result").innerText = result || "未找到结果";
}
```

**示例 data.json**

```
json复制代码{
  "张三": "学号2023001，宿舍A101",
  "李四": "学号2023002，宿舍A102"
}
```

------

### 2. 启用 GitHub Pages

1. 进入仓库 → **Settings** → **Pages**

2. Source 选 `Deploy from branch` → `main` → `/ (root)`

3. 保存后，你就能通过

   ```
   arduino
   
   
   复制代码
   https://tanteijms.github.io/qr-search/
   ```

   访问了。

------

### 3. 申请 dpdns.org 域名

1. 打开 [dpdns.org](https://www.dpdns.org/)

2. 注册账号（一般用邮箱即可）。

3. 申请一个二级域名，比如：

   ```
   复制代码
   bupt-qr.dpdns.org
   ```

------

### 4. 域名解析到 GitHub Pages

1. 在 `dpdns.org` 的控制台里，添加一条 **CNAME 解析**：

   ```
   makefile复制代码主机记录: bupt-qr
   记录类型: CNAME
   记录值: tanteijms.github.io
   ```

   （意思就是把 `bupt-qr.dpdns.org` 指向你的 GitHub Pages 用户站点）

2. 在你的仓库 `qr-search` 里，新建一个 `CNAME` 文件，内容写：

   ```
   复制代码
   bupt-qr.dpdns.org
   ```

------

### 5. 等待生效 ✅

- DNS 一般几分钟到几小时就能生效。

- 成功后，你就能直接用

  ```
  arduino
  
  
  复制代码
  https://bupt-qr.dpdns.org
  ```

  来访问了 🎉

------

## ⚡ 总结

- GitHub Pages：存放静态网页 + 数据
- dpdns.org：提供免费二级域名，绑定到你的 Pages
- 用户访问体验就是：输入名字 → 查询到对应结果