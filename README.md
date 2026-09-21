# 张荣庭 个人学术主页

张荣庭（Rongting Zhang）· 南京工业大学 测绘科学与技术学院

基于 **GitHub Pages** 的纯静态个人学术主页，无需构建工具，浏览器直接运行，免费托管，绑定域名后即可全球访问。

在线地址（部署后）：**https://NJTechZhang.github.io**

---

## 一、项目结构

```
个人学术主页/
├── index.html                  # 主页（个人简介 / 研究方向 / 论文列表 / 联系方式）
├── papers/                     # 论文中文导读（每篇论文一个页面）
│   ├── index.html              # 论文导读总览（按年份索引 22 篇）
│   ├── mesh-based-dgcnn.html   # 例：Mesh-Based DGCNN 导读
│   └── ...（共 22 篇）
├── assets/
│   ├── css/style.css           # 主页样式
│   ├── css/paper.css           # 论文导读页样式
│   ├── js/main.js              # 交互脚本（导航、年份等）
│   └── img/avatar.jpg          # 个人照片（可选，未放置时显示"张"字头像）
├── tools/                      # 维护工具（Python，需 PyMuPDF）
│   ├── build_digest.py         # 从 PDF 批量提取全文与内容摘要素材
│   └── check_site.py           # 站点自检：链接、结构、条目一致性
├── 论文原文/                    # 论文 PDF 原文（已在 .gitignore 中排除，不会上线）
├── .gitignore                  # 排除 PDF 原文与临时文件
├── .nojekyll                   # 声明纯静态站点
└── README.md                   # 本说明
```

### 维护工具用法

```bash
# 站点自检（提交前建议运行）：检查内部链接、页面结构、论文条目是否一致
python tools/check_site.py

# 新增论文时：从 论文原文/*.pdf 批量提取全文与摘要素材到 .tmp_extract/
python tools/build_digest.py
```

两个脚本均需 `pip install pymupdf`。

## 一之二、论文中文导读

「发表论文」列表中，**点击论文标题或「中文导读」标签**即进入该论文的中文导读页。每篇导读包含：

- 摘要（中文完整复述）
- 研究背景与动机
- 方法与主要创新（分条说明）
- 实验与结果（含数据集、对比方法与真实数值）
- 结论与意义
- 一句话总结
- 标准引用格式与原文链接

共 **22 篇**，可在 `papers/index.html`（论文导读总览）中按年份浏览全部导读。

### 新增论文导读的步骤

1. 把论文 PDF 放入 `论文原文/` 目录
2. 复制任一 `papers/*.html` 作为模板，替换标题、作者、期刊、摘要等各节内容
3. 在 `index.html` 的「发表论文」章节对应年份下新增条目，并在 `papers/index.html` 中登记

## 二、修改个人信息

主页内容在 `index.html` 中，搜索 `TODO` 注释即可找到待补充位置：

| 待补充项 | 位置（index.html 内搜索） | 说明 |
|---|---|---|
| 职称（讲师/副教授等） | `TODO: 职称确认后替换` | 页头 title-line 处 |
| 个人照片 | 复制照片为 `assets/img/avatar.jpg` | 建议正方形，约 500×500px |
| 论文列表 | 「发表论文」章节 | 核对作者顺序、补充新论文并链接到导读页 |

联系方式（邮箱 `zrt@njtech.edu.cn`）已按学院公开信息填写。

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
- 论文中文导读均依据论文 PDF 原文撰写，实验数值取自原文；作者顺序请对照 Google Scholar 最终核实
- 学院地址为南京工业大学江北校区公共信息，请按实际确认
- **两篇论文未能获取全文 PDF**（IEEE 订阅论文，无开放获取版本），其导读依据**公开摘要**整理，页面中已明确标注：
  - *RADANet: Road Augmented Deformable Attention Network for Road Extraction...*（IEEE TGRS 2023）
  - *A Deformable Attention Network for High-Resolution Remote Sensing Images Semantic Segmentation*（IEEE TGRS 2021）
  若在校内网络下载到 PDF 并放入 `论文原文/`，可据此补充完善这两篇导读。
- **版权提示**：`论文原文/` 目录中的 PDF 归各出版商所有，已在 `.gitignore` 中排除，不会随站点上线。若您有把握获得授权并希望公开，删除 `.gitignore` 中对应的 `论文原文/` 一行即可。

## 六、技术说明

- 纯 HTML + CSS + JavaScript，无外部依赖、无框架，任何静态托管服务（GitHub Pages / Gitee Pages / 自有服务器）均可直接部署
- 无需 Jekyll 构建，已通过 `.nojekyll` 标记（见仓库根目录）
- 响应式设计，支持手机浏览
