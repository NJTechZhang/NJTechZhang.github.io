# 张荣庭 个人学术主页

张荣庭（Rongting Zhang）· 南京工业大学 测绘科学与技术学院

基于 **GitHub Pages** 的纯静态个人学术主页，无需构建工具，浏览器直接运行，免费托管，绑定域名后即可全球访问。

在线地址（部署后）：**https://NJTechZhang.github.io**

---

## 一、项目结构

```
个人学术主页/
├── index.html          # 主页（所有内容都在这里）
├── assets/
│   ├── css/style.css   # 样式
│   ├── js/main.js      # 交互脚本（导航、年份等）
│   └── img/avatar.jpg  # 个人照片（可选，未放置时显示"张"字头像）
└── README.md           # 本说明
```

## 二、修改个人信息

所有内容都在 `index.html` 中，搜索 `TODO` 注释即可找到待补充位置：

| 待补充项 | 位置（index.html 内搜索） | 说明 |
|---|---|---|
| 职称（讲师/副教授等） | `TODO: 职称确认后替换` | 页头 title-line 处 |
| 教育背景 / 工作经历 | `TODO: 教育背景、工作经历确认后在此补充` | 个人简介卡片中 |
| 邮箱 | `TODO: 确认后填写邮箱` | 联系方式卡片中 |
| 个人照片 | 复制照片为 `assets/img/avatar.jpg` | 建议正方形，约 500×500px |
| 论文列表 | 「发表论文」章节 | 对照 Google Scholar 核对作者与补充新论文 |

## 三、部署到 GitHub Pages（约 5 分钟）

### 第 1 步：准备 GitHub 账号

访问 https://github.com 注册账号（用户名需为 `NJTechZhang`，或注册后改为此用户名——若昵称已被占用，可改用其他名字，主页地址随之变化，代码中页脚链接需同步修改）。

### 第 2 步：创建仓库

1. 登录 GitHub，点击右上角 **+** → **New repository**
2. Repository name 填写：**`NJTechZhang.github.io`**（必须与用户名一致，这是 GitHub Pages 用户主页的固定命名）
3. 选择 **Public**
4. 点击 **Create repository**

### 第 3 步：本地推送代码

在项目文件夹内打开终端（Windows 可在文件夹地址栏输入 `cmd` 回车），依次执行：

```bash
git init
git add .
git commit -m "init: 个人学术主页"
git branch -M main
git remote add origin https://github.com/NJTechZhang/NJTechZhang.github.io.git
git push -u origin main
```

> 推送时需输入 GitHub 用户名与 Personal Access Token（密码框内粘贴）。
> Token 获取：GitHub 头像 → Settings → Developer settings → Personal access tokens → Generate new token，勾选 `repo` 权限，复制生成的 token。

### 第 4 步：启用 Pages 并访问

1. 仓库页面 → **Settings** → 左侧 **Pages**
2. Build and deployment → Source 选择 **Deploy from a branch**
3. Branch 选择 **main** / **/ (root)** → **Save**
4. 等待 1–2 分钟构建，访问 **https://NJTechZhang.github.io** 即可看到主页

### 第 5 步（可选）：绑定自定义域名

在 Pages 设置页的 Custom domain 中填入您的域名（如 `zhangrongting.cn`），并按提示在域名服务商处添加 CNAME 记录指向 `NJTechZhang.github.io`。

## 四、日常更新

修改 `index.html` 后：

```bash
git add .
git commit -m "更新内容说明"
git push
```

推送后约 1 分钟内 GitHub Pages 自动更新。

## 五、信息核实说明

- 身份与论文信息依据学院主页（https://cge.njtech.edu.cn/info/1045/4427.htm）与 Google Scholar（https://scholar.google.com.hk/citations?user=4arxHdYAAAAJ&hl=zh-CN&oi=ao）整理
- 论文作者顺序请对照 Google Scholar 最终核实；`index.html` 中已标注 `TODO` 项待您补充
- 学院地址为南京工业大学江北校区公共信息，请按实际确认

## 六、技术说明

- 纯 HTML + CSS + JavaScript，无外部依赖、无框架，任何静态托管服务（GitHub Pages / Gitee Pages / 自有服务器）均可直接部署
- 无需 Jekyll 构建，已通过 `.nojekyll` 标记（见仓库根目录）
- 响应式设计，支持手机浏览
