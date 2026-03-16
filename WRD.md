# pSEO US City Data Site - 项目需求文档

## 一、项目定位与核心逻辑
- **网站类型**: 程序化生成的美国本地数据聚合站 (US City Relocation & Data Hub)
- **目标受众**: 准备搬家、找工作、买房、或单纯好奇某个城市的美国人
- **盈利模式**:
  - 前期/中期：Ezoic 或 Journey by Mediavine (展示广告)
  - 后期：Mediavine (顶级展示广告，目标RPM $30-$50)
  - 附加：Affiliate 联盟（推荐搬家公司估价、个人信用分查询等）

## 二、技术栈
- 前端框架：Astro
- CSS 框架：Tailwind CSS
- 数据格式：JSON/CSV
- 托管：Cloudflare Pages

## 三、URL 结构
- 首页: /
- 州聚合页: /state/california
- 城市详情页: /city/austin-tx

## 四、页面模板
1. 首页 (Home)
2. 州聚合页 (State Hub)
3. 城市详情页 (City Detail)

## 五、数据源
- Simplemaps US Cities Database (免费版，3万城市)
- Kaggle: US cost of living, crime datasets
- Zillow Research Data
- Census.gov

## 六、广告位
- Header: 728x90
- Sidebar: 300x250 / 300x600
- In-content: Module 1 & 2 之间
- Sticky Footer: 手机端

## 行动路径
1. 域名确定
2. 整理100个测试城市数据
3. 开发Astro模板
4. 全量上线 (30,000页面)
5. 提交Sitemap，等待收录
