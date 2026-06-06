# Nginx 应急溯源报告

- 生成时间: `2026-06-06T12:11:19.342920+08:00`
- 输入路径: `D:\tmp\anjian\pj\st\test\2026-06-01\home\nginx\var\log\nginx\2026-06-01\barmyy-manage.access.log, D:\tmp\anjian\pj\st\test\2026-06-02\home\nginx\var\log\nginx\2026-06-02\barmyy-manage.access.log, D:\tmp\anjian\pj\st\test\2026-06-03\home\nginx\var\log\nginx\2026-06-03\barmyy-manage.access.log, D:\tmp\anjian\pj\st\test\2026-06-04\home\nginx\var\log\nginx\2026-06-04\barmyy-manage.access.log`
- 日志文件数: `4`
- 有效日志条数: `65737`
- 解析失败条数: `0`

## 结论摘要

- 最高风险 IP: `120.234.61.168`，评分 `114.4`，请求 `21851`，原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, server-error-touch, bulk-enumeration`
- 最高风险 URI: `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，评分 `67.0`，请求 `19533`，最大响应 `29053720`
- 热点时间窗: `2026-06-02 14:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `13777`
- 热点时间窗: `2026-06-02 10:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `5650`
- 热点时间窗: `2026-06-02 08:00` `/nh_api/Approval/sys/GetSysConfig` 次数 `2053`
- 热点时间窗: `2026-06-03 10:00` `/nh_api/Approval/sys/GetSysConfig` 次数 `708`
- 热点时间窗: `2026-06-04 10:00` `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord` 次数 `53`
- 热点时间窗: `2026-06-04 10:00` `/nh_api/HealthInstruction/SearchHealthInstructionInfoList` 次数 `47`
- 热点时间窗: `2026-06-01 18:00` `/actuator` 次数 `46`
- 热点时间窗: `2026-06-01 18:00` `/env` 次数 `46`

## 高风险 IP

- `120.234.61.168` 分数 `114.4` 请求 `21851` 峰值RPS `173` 路径数 `879` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, server-error-touch, bulk-enumeration`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(19426), /actuator(55), /env(55), /manage(54)
- `112.97.203.114` 分数 `105.2` 请求 `10422` 峰值RPS `197` 路径数 `9424` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(59), /nh_api/HealthInstruction/SearchHealthInstructionInfoList(55), /nh_api/auth/login/Authenticket(34), /nh_api/Approval/ReservePay/CreateReserve(31)
- `219.133.80.154` 分数 `96.39` 请求 `1773` 峰值RPS `32` 路径数 `836` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /actuator(31), /env(31), /manage(30), /manage/env(30)
- `183.238.10.154` 分数 `79.41` 请求 `1590` 峰值RPS `24` 路径数 `159` 原因 `high-volume, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /Home/GetWebSiteAddress(166), /nh_api/Approval/Sys/GetUserInfo(64), /nh_api/Approval/Apply/GetApprovalApplyResultList(59), /nh_api/Survey/ExternalMedicalRecord/GetQuestSubjectAnswer(58)
- `223.160.224.36` 分数 `64.76` 请求 `2211` 峰值RPS `37` 路径数 `62` 原因 `high-volume, burst, sensitive-path, bulk-enumeration`
  重点路径: /nh_api/Approval/sys/GetSysConfig(2047), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(15), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(15), /nh_api/Survey/AnswerCard/GetAnswerCardById(15)
- `223.104.79.38` 分数 `61.33` 请求 `824` 峰值RPS `27` 路径数 `98` 原因 `high-volume, burst, sensitive-path, bulk-enumeration`
  重点路径: /nh_api/Approval/sys/GetSysConfig(707), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(5), /nh_api/Survey/AnswerCard/GetAnswerCardById(5), /nh_approvalweb/css/basic.css(4)
- `113.84.194.100` 分数 `57.36` 请求 `700` 峰值RPS `35` 路径数 `173` 原因 `high-volume, burst, sensitive-path, auth-burst`
  重点路径: /nh_api/Approval/Project/GetProjectList(30), /nh_api/Approval/Apply/GetApprovalApplyList(22), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(15), /nh_img/Imgs/Original/HealthInstruction/quitmenu/057bccfe-9349-49cd-9229-db9aa0d397e8.png(15)
- `43.247.70.12` 分数 `53.2` 请求 `495` 峰值RPS `49` 路径数 `168` 原因 `burst, large-response, sensitive-path, auth-burst, server-error-touch`
  重点路径: /Home/GetWebSiteAddress(30), /Content/lib/layuiadmin/layui/css/modules/layer/default/layer.css(13), /Content/lib/layuiadmin/layui/css/modules/laydate/default/laydate.css(11), /Content/lib/layuiadmin/layui/css/modules/code.css(11)
- `113.88.95.148` 分数 `46.0` 请求 `150` 峰值RPS `22` 路径数 `88` 原因 `burst, large-response, sensitive-path`
  重点路径: /nh_api/Approval/Project/GetProjectList(6), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(6), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(6), /nh_api/Survey/AnswerCard/GetAnswerCardById(6)
- `112.97.81.121` 分数 `42.0` 请求 `131` 峰值RPS `15` 路径数 `101` 原因 `burst, sensitive-path, large-response`
  重点路径: /nh_api/Approval/Project/GetProjectList(4), /nh_api/Approval/sys/GetDepartmentDiseasePageList(4), /nh_api/Approval/Apply/GetApprovalApplyList(3), /nh_api/Approval/process/ProcessApply(3)
- `123.168.84.249` 分数 `42.0` 请求 `94` 峰值RPS `12` 路径数 `79` 原因 `burst, sensitive-path, large-response`
  重点路径: /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(4), /nh_api/Survey/AnswerCard/GetAnswerCardById(4), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(3), /nh_api/auth/login/Authenticket(2)
- `113.84.65.63` 分数 `32.9` 请求 `188` 峰值RPS `34` 路径数 `59` 原因 `burst, sensitive-path, server-error-touch`
  重点路径: /nh_api/User/Login/PartnerLogin(7), /favicon.ico(7), /Home/ClearApiToken(7), /Account/PartnerLogin(4)

## 高风险 URI

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 分数 `67.0` 请求 `19533` 源IP `20` 峰值RPS `173` 最大响应 `29053720`
  主要来源: 120.234.61.168(19426), 183.238.10.154(27), 112.97.203.114(20), 111.55.210.80(17), 219.133.80.154(16)
- `/nh_api/Approval/sys/GetSysConfig` 分数 `47.0` 请求 `2782` 源IP `4` 峰值RPS `37` 最大响应 `768`
  主要来源: 223.160.224.36(2047), 223.104.79.38(707), 183.238.10.154(27), 43.247.70.12(1)
- `/nh_api/auth/login/Authenticket` 分数 `43.0` 请求 `895` 源IP `511` 峰值RPS `2` 最大响应 `561`
  主要来源: 112.97.203.114(34), 113.84.194.100(14), 223.104.79.118(12), 219.133.80.154(10), 120.234.61.168(9)
- `/nh_api/HealthInstruction/GetHealthInstructionInfoById` 分数 `38.58` 请求 `116` 源IP `73` 峰值RPS `1` 最大响应 `65955`
  主要来源: 112.97.203.114(24), 223.104.79.22(4), 183.238.10.154(3), 223.104.77.165(3), 223.104.77.171(3)
- `/nh_api/Approval/Project/GetProjectList` 分数 `37.86` 请求 `161` 源IP `23` 峰值RPS `3` 最大响应 `2648`
  主要来源: 113.84.194.100(30), 112.97.203.114(22), 120.234.61.168(19), 219.133.80.154(18), 58.60.110.201(13)
- `/nh_api/HealthInstruction/Sys/Login` 分数 `36.96` 请求 `128` 源IP `81` 峰值RPS `3` 最大响应 `1152`
  主要来源: 112.97.203.114(18), 120.234.61.168(7), 219.133.80.154(7), 113.84.194.100(6), 223.104.68.131(4)
- `/nh_api/Approval/Apply/GetApprovalApplyList` 分数 `36.75` 请求 `121` 源IP `21` 峰值RPS `3` 最大响应 `3032`
  主要来源: 113.84.194.100(22), 120.234.61.168(21), 112.97.203.114(18), 219.133.80.154(15), 58.60.110.201(9)
- `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup` 分数 `35.0` 请求 `924` 源IP `498` 峰值RPS `3` 最大响应 `11288`
  主要来源: 112.97.203.114(22), 113.84.194.100(15), 219.133.80.154(13), 223.104.79.118(12), 120.234.61.168(10)
- `/nh_healthinstructionweb/` 分数 `35.0` 请求 `812` 源IP `526` 峰值RPS `2` 最大响应 `8123`
  主要来源: 112.97.203.114(20), 223.104.79.118(12), 223.104.77.171(7), 223.104.79.22(6), 223.104.86.75(6)
- `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord` 分数 `35.0` 请求 `653` 源IP `266` 峰值RPS `3` 最大响应 `88`
  主要来源: 112.97.203.114(59), 223.104.79.118(16), 223.104.77.171(15), 119.136.31.253(13), 113.84.40.140(9)
- `/` 分数 `34.45` 请求 `521` 源IP `320` 峰值RPS `3` 最大响应 `607`
  主要来源: 45.148.10.67(35), 123.57.13.121(17), 114.250.44.7(15), 121.29.51.109(13), 114.250.50.173(9)
- `/nh_api/HealthInstruction/ViewRecord/GetClientId` 分数 `31.45` 请求 `242` 源IP `230` 峰值RPS `2` 最大响应 `88`
  主要来源: 112.97.203.114(5), 223.104.80.69(2), 223.104.79.22(2), 223.104.86.75(2), 219.133.80.154(2)

## 异常大响应样本

- `2026-06-04T10:58:27+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260604_%E5%BC%A0%E6%B4%AA%E5%AE%9D.zip` 状态 `200` 响应 `63884311` 原因 `large-response`
- `2026-06-02T08:09:53+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%BA%8C%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260602_%E6%9D%A8%E6%98%A5%E6%9E%97.zip` 状态 `200` 响应 `37318134` 原因 `large-response`
- `2026-06-02T15:11:09+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T15:10:20+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T15:05:21+08:00` `219.133.80.154` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T14:55:10+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T14:47:59+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T14:47:16+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T14:47:15+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T14:47:14+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T10:05:02+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29052992` 原因 `size>812(p95),size>16330x2,size>mean+3stdev`
- `2026-06-02T10:51:32+08:00` `219.133.80.154` `/nh_img/Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `23444828` 原因 `large-response`

## 路由/源码候选

### `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`

### `/nh_api/Approval/sys/GetSysConfig`

### `/nh_api/auth/login/Authenticket`

### `/nh_api/HealthInstruction/GetHealthInstructionInfoById`

### `/nh_api/Approval/Project/GetProjectList`

### `/nh_api/HealthInstruction/Sys/Login`

### `/nh_api/Approval/Apply/GetApprovalApplyList`

### `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup`

### `/nh_healthinstructionweb/`

### `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord`

### `/nh_api/HealthInstruction/ViewRecord/GetClientId`
