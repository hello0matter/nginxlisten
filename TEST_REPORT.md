# Nginx Trace Hunter 测试报告

测试时间：2026-06-08

## 测试目标

本次测试验证以下能力：

- 普通日志目录是否能被识别。
- `zip` 归档里的 access log 是否能被识别。
- 日期范围过滤是否能正常工作。
- 风险评分和告警阈值是否能触发。
- 钉钉机器人是否能收到带关键词的告警。
- 输出报告是否能具体到涉及文件。

## 测试样本

本次没有改动真实业务日志，只在隔离目录下生成测试数据：

- 普通日志：`test-fixtures/alert-case/logs/demo-api.access.log`
- 压缩包：`test-fixtures/alert-case/packed-logs.zip`
- 压缩包内日志：`home/nginx/var/log/nginx/2026-06-08/demo-zipped.access.log`

样本内容：

- `demo-api.access.log`：216 行，模拟高频访问 `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，并附带 `/actuator/env`、`/api-docs`、`/.env` 等探测 URI。
- `demo-zipped.access.log`：160 行，模拟压缩包中的 `/nh_api/auth/login/Authenticket` 和 `/nh_api/Patient/GetPatientList` 高频访问。

## 执行命令

```powershell
python nginx_trace_hunter.py test-fixtures\alert-case\logs test-fixtures\alert-case\packed-logs.zip --once --from-date 2026-06-08 --to-date 2026-06-08 --output-dir test-output\ding-alert --state-file test-output\ding-alert-state.json --alert --alert-min 30
```

## 阈值说明

`--alert-min 30` 的含义是“告警触发最低分数为 30”。

脚本会分别计算：

- 最高风险 IP 的分数。
- 最高风险 URI 的分数。

然后取两者中的较大值作为本轮告警分数：

```text
alert_score = max(top_ip.score, top_uri.score)
```

如果 `alert_score >= alert_min`，并且没有被告警去重命中，就会推送告警。

本次结果：

- 最高风险 IP：`198.51.100.88`，分数 `28.3`
- 最高风险 URI：`/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，分数 `30.8`
- 本轮告警分数：`30.8`
- 告警阈值：`30`
- 结论：达到阈值，触发推送。

## 测试结果

输出目录：

- `test-output/ding-alert/report.md`
- `test-output/ding-alert/report.json`
- `test-output/ding-alert/suspicious_ips.csv`
- `test-output/ding-alert/suspicious_uris.csv`
- `test-output/ding-alert/review_ips.csv`
- `test-output/ding-alert/hunter.log`

关键结果：

- 扫描文件数：`2`
- 有效日志记录：`376`
- 归档日志已被解压并纳入分析。
- 高风险 URI：`/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`
- 高风险 URI 分数：`30.8`
- 观察 IP 数量：`2`
- 高优先级研判 IP 数量：`0`

## 钉钉推送结果

本机配置中已存在钉钉 Webhook 和关键词：

- 钉钉关键词：`应急告警`

本次推送结果见：

- `test-output/ding-alert/hunter.log`
- `test-output/ding-alert-state.json`

结果：

```json
{"errcode":0,"errmsg":"ok"}
```

说明钉钉机器人已接受推送。推送内容前面会自动加上钉钉关键词，满足自定义关键词校验。

## 发现并修复的问题

测试过程中发现两个问题，并已修复：

1. 当输入同时包含普通日志和 `zip` 归档时，脚本原先发现普通日志后会提前返回，导致同次输入的归档日志没有被分析。
   - 修复：改为合并“直接发现日志”和“归档内日志”。
2. 单轮分析 `--once --alert` 原先只生成报告，不执行告警推送。
   - 修复：单轮分析在启用告警时也执行推送，并把推送结果写入状态文件。

## 结论

本次测试通过：

- 普通日志可识别。
- `zip` 内日志可识别。
- 日期范围过滤可用。
- 报告能具体到文件。
- 告警阈值逻辑符合预期。
- 钉钉推送成功。

后续建议：

- 在 GUI 中增加“测试钉钉推送”按钮，避免必须制造风险日志才能验证机器人配置。
- 在 GUI 中显示当前告警阈值说明，例如“达到该分数才推送”。
- 增加一份“测试样本生成器”，方便后续回归测试。

