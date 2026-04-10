# getuscompliance.com - 自动更新

## 定时任务

**cron job**: 每周日 凌晨2点自动更新

```bash
# /etc/cron.d/getuscompliance
0 2 * * 0 root /root/.openclaw/workspace-geo-all/all-seo/scripts/auto_update.sh >> /var/log/getuscompliance.log 2>&1
```

## 手动更新

```bash
cd /root/.openclaw/workspace-geo-all/all-seo
./scripts/auto_update.sh
```

## 日志

- `/var/log/getuscompliance.log`

## 注意
- 确保 cron 服务已启动
- API Token 已配置在脚本中 (需重新生成，已暴露)
