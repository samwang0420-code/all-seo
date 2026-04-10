# 分批扩充计划

## 策略：渐进式扩充

### 第1批 (已完成 ✅)
- 数量：6,400 城市
- 状态：已部署

### 第2批 (目标: 12,000)
- 增加：5,600 城市
- 预计构建时间：~5分钟

### 第3批 (目标: 20,000)
- 增加：8,000 城市
- 预计构建时间：~10分钟

### 第4批 (目标: 30,000)
- 增加：10,000 城市
- 预计构建时间：~15分钟

## 执行命令

```bash
# 第2批：增加到 12,000 城市
python scripts/batch_generate.py --target 12000
npm run build
wrangler pages deploy

# 第3批：增加到 20,000
python scripts/batch_generate.py --target 20000
npm run build  
wrangler pages deploy

# 第4批：增加到 30,000
python scripts/batch_generate.py --target 30000
npm run build
wrangler pages deploy
```

## 注意事项
- 每次构建会增加部署时间
- 建议每批间隔几分钟
- 可以随时暂停/继续
