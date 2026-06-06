# Nginx 应急溯源报告

- 生成时间: `2026-06-06T12:24:00.339831+08:00`
- 输入路径: `D:\tmp\anjian\pj\st\tmp\nginxlisten\output-agent-test\_agent_batch\20260606_122348\0000\barmyy-manage.access.log, D:\tmp\anjian\pj\st\tmp\nginxlisten\output-agent-test\_agent_batch\20260606_122348\0001\barmyy-manage.access.log`
- 日志文件数: `2`
- 有效日志条数: `38282`
- 解析失败条数: `0`

## 结论摘要

- 最高风险 IP: `120.234.61.168`，评分 `114.4`，请求 `21851`，原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, server-error-touch, bulk-enumeration`
- 最高风险 URI: `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，评分 `64.2`，请求 `19478`，最大响应 `29053720`
- 热点时间窗: `2026-06-02 14:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `13777`
- 热点时间窗: `2026-06-02 10:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `5650`
- 热点时间窗: `2026-06-02 08:00` `/nh_api/Approval/sys/GetSysConfig` 次数 `2053`
- 热点时间窗: `2026-06-01 18:00` `/actuator` 次数 `46`
- 热点时间窗: `2026-06-01 18:00` `/env` 次数 `46`
- 热点时间窗: `2026-06-01 18:00` `/manage` 次数 `45`
- 热点时间窗: `2026-06-01 18:00` `/manage/env` 次数 `45`
- 热点时间窗: `2026-06-01 18:00` `/api/v2/api-docs` 次数 `45`

## 高风险 IP

- `120.234.61.168` 分数 `114.4` 请求 `21851` 峰值RPS `173` 路径数 `879` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, server-error-touch, bulk-enumeration`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(19426), /actuator(55), /env(55), /manage(54)
- `219.133.80.154` 分数 `96.39` 请求 `1773` 峰值RPS `32` 路径数 `836` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /actuator(31), /env(31), /manage(30), /manage/env(30)
- `223.160.224.36` 分数 `71.96` 请求 `2211` 峰值RPS `37` 路径数 `62` 原因 `high-volume, burst, sensitive-path, bulk-enumeration, large-response`
  重点路径: /nh_api/Approval/sys/GetSysConfig(2047), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(15), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(15), /nh_api/Survey/AnswerCard/GetAnswerCardById(15)
- `183.238.10.154` 分数 `69.26` 请求 `720` 峰值RPS `24` 路径数 `118` 原因 `high-volume, burst, sensitive-path, large-response, server-error-touch`
  重点路径: /Home/GetWebSiteAddress(82), /nh_api/Approval/Apply/GetApprovalApplyResultList(30), /nh_api/Approval/Sys/GetUserInfo(29), /nh_api/Manage/Config/GetConfigPlatform(25)
- `123.168.84.249` 分数 `45.6` 请求 `94` 峰值RPS `12` 路径数 `79` 原因 `burst, large-response, sensitive-path`
  重点路径: /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(4), /nh_api/Survey/AnswerCard/GetAnswerCardById(4), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(3), /nh_api/auth/login/Authenticket(2)
- `223.104.86.72` 分数 `33.6` 请求 `75` 峰值RPS `18` 路径数 `64` 原因 `burst, sensitive-path, large-response`
  重点路径: /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(3), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(3), /nh_api/Survey/AnswerCard/GetAnswerCardById(3), /nh_api/auth/login/Authenticket(2)
- `45.138.16.206` 分数 `32.0` 请求 `57` 峰值RPS `28` 路径数 `57` 原因 `burst, server-error-touch, sensitive-path`
  重点路径: /(1), /assets/main.js(1), /config.yaml(1), /signin(1)
- `223.104.79.67` 分数 `30.0` 请求 `423` 峰值RPS `33` 路径数 `182` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Approval/sys/GetDepartmentDiseasePageList(24), /nh_api/FileUpload/FileUpload/UploadPictures(20), /nh_api/Approval/Sys/GetDiseaseList(15), /nh_api/Approval/Project/GetProjectList(10)
- `113.84.209.96` 分数 `30.0` 请求 `111` 峰值RPS `12` 路径数 `81` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Approval/Project/GetProjectList(5), /nh_api/Approval/Sys/GetDiseaseList(5), /nh_api/Approval/sys/GetDepartmentDiseasePageList(4), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(3)
- `223.104.87.157` 分数 `30.0` 请求 `84` 峰值RPS `17` 路径数 `41` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(6), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(6), /nh_api/Survey/AnswerCard/GetAnswerCardById(6), /nh_api/auth/login/Authenticket(4)
- `223.104.68.131` 分数 `26.4` 请求 `101` 峰值RPS `12` 路径数 `61` 原因 `burst, sensitive-path`
  重点路径: /nh_api/auth/login/Authenticket(5), /nh_api/HealthInstruction/Sys/Login(4), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(4), /nh_img/Imgs/Original/HealthInstruction/quitmenu/fbeb2582-0018-42f1-87b4-af5b16b33604.png(4)
- `14.154.6.6` 分数 `25.8` 请求 `69` 峰值RPS `14` 路径数 `66` 原因 `burst, sensitive-path`
  重点路径: /nh_api/auth/login/Authenticket(2), /nh_api/Approval/Project/GetProjectList(2), /nh_api/Approval/Apply/GetApprovalApplyList(2), /nh_healthinstructionweb/(1)
- `223.104.79.118` 分数 `24.0` 请求 `173` 峰值RPS `16` 路径数 `33` 原因 `burst, sensitive-path`
  重点路径: /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(15), /nh_healthinstructionweb/(10), /nh_api/auth/login/Authenticket(10), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(10)
- `113.92.75.228` 分数 `24.0` 请求 `71` 峰值RPS `14` 路径数 `63` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Approval/Project/GetProjectList(3), /nh_api/auth/login/Authenticket(2), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(2), /nh_img/Imgs/Original/HealthInstruction/quitmenu/60379f51-541a-4c5e-b67e-5d63ef21ce17.png(2)
- `223.74.154.68` 分数 `21.6` 请求 `50` 峰值RPS `15` 路径数 `46` 原因 `burst, large-response`
  重点路径: /nh_api/HealthInstruction/SearchHealthInstructionInfoList(3), /nh_api/HealthInstruction/Tag/GetHomeTabpageConfigList(2), /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(2), /nh_healthinstructionweb/(1)
- `223.160.229.96` 分数 `21.3` 请求 `65` 峰值RPS `11` 路径数 `59` 原因 `burst, sensitive-path`
  重点路径: /nh_api/auth/login/Authenticket(2), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(2), /nh_img/Imgs/Original/HealthInstruction/quitmenu/60379f51-541a-4c5e-b67e-5d63ef21ce17.png(2), /nh_img/Imgs/Original/HealthInstruction/quitmenu/fbeb2582-0018-42f1-87b4-af5b16b33604.png(2)
- `219.133.176.8` 分数 `20.1` 请求 `45` 峰值RPS `11` 路径数 `41` 原因 `burst, large-response`
  重点路径: /nh_api/HealthInstruction/SearchHealthInstructionInfoList(3), /nh_api/HealthInstruction/Tag/GetHomeTabpageConfigList(2), /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(2), /nh_healthinstructionweb/(1)
- `111.55.210.80` 分数 `18.6` 请求 `19` 峰值RPS `2` 路径数 `3` 原因 `sensitive-path, server-error-touch, large-response`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(17), /(1), /favicon.ico(1)
- `223.104.86.75` 分数 `18.0` 请求 `162` 峰值RPS `20` 路径数 `34` 原因 `burst`
  重点路径: /nh_healthinstructionweb/(6), /nh_api/auth/login/Authenticket(6), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(6), /nh_img/Imgs/Original/HealthInstruction/quitmenu/8bdc156e-4d99-441f-a77d-d1c22e15699f.png(6)
- `223.104.79.22` 分数 `18.0` 请求 `144` 峰值RPS `20` 路径数 `47` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(8), /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(8), /nh_healthinstructionweb/(6), /nh_api/auth/login/Authenticket(5)

## 高风险 URI

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 分数 `64.2` 请求 `19478` 源IP `9` 峰值RPS `173` 最大响应 `29053720`
  主要来源: 120.234.61.168(19426), 111.55.210.80(17), 219.133.80.154(16), 183.238.10.154(9), 223.160.224.36(5)
- `/nh_api/Approval/sys/GetSysConfig` 分数 `47.0` 请求 `2056` 源IP `2` 峰值RPS `37` 最大响应 `768`
  主要来源: 223.160.224.36(2047), 183.238.10.154(9)
- `/nh_api/auth/login/Authenticket` 分数 `41.43` 请求 `401` 源IP `248` 峰值RPS `2` 最大响应 `561`
  主要来源: 219.133.80.154(10), 223.104.79.118(10), 120.234.61.168(9), 223.104.79.67(8), 120.229.67.97(7)
- `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup` 分数 `33.62` 请求 `421` 源IP `241` 峰值RPS `3` 最大响应 `11288`
  主要来源: 219.133.80.154(13), 120.234.61.168(10), 223.104.79.118(10), 223.104.79.22(8), 223.104.79.67(8)
- `/nh_healthinstructionweb/` 分数 `33.09` 请求 `368` 源IP `252` 峰值RPS `2` 最大响应 `8123`
  主要来源: 223.104.79.118(10), 223.104.79.22(6), 223.104.86.75(6), 223.104.77.186(5), 120.229.67.97(5)
- `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord` 分数 `31.76` 请求 `262` 源IP `125` 峰值RPS `2` 最大响应 `88`
  主要来源: 223.104.79.118(15), 223.104.79.22(8), 223.104.77.165(8), 223.104.77.186(6), 116.30.141.124(6)
- `/` 分数 `31.01` 请求 `216` 源IP `139` 峰值RPS `3` 最大响应 `607`
  主要来源: 123.57.13.121(15), 45.148.10.67(15), 114.250.50.173(9), 114.250.44.7(9), 91.237.124.245(9)
- `/nh_api/HealthInstruction/ViewRecord/GetClientId` 分数 `28.51` 请求 `114` 源IP `110` 峰值RPS `1` 最大响应 `88`
  主要来源: 223.104.79.22(2), 223.104.86.75(2), 219.133.80.154(2), 223.73.7.78(2), 223.73.114.60(1)
- `/nh_api/HealthInstruction/Sys/Login` 分数 `18.0` 请求 `55` 源IP `37` 峰值RPS `2` 最大响应 `1152`
  主要来源: 120.234.61.168(7), 219.133.80.154(7), 223.104.68.131(4), 223.104.79.67(3), 121.15.144.218(2)
- `/nh_api/Approval/Project/GetProjectList` 分数 `16.8` 请求 `65` 源IP `11` 峰值RPS `3` 最大响应 `2648`
  主要来源: 120.234.61.168(19), 219.133.80.154(18), 223.104.79.67(10), 113.84.209.96(5), 113.92.75.228(3)
- `/nh_api/Approval/Apply/GetApprovalApplyList` 分数 `15.2` 请求 `54` 源IP `9` 峰值RPS `3` 最大响应 `3032`
  主要来源: 120.234.61.168(21), 219.133.80.154(15), 223.104.79.67(8), 113.84.209.96(3), 113.92.75.228(2)
- `/Home/GetWebSiteAddress` 分数 `10.0` 请求 `95` 源IP `13` 峰值RPS `2` 最大响应 `56`
  主要来源: 183.238.10.154(82), 113.84.65.187(2), 223.104.79.111(1), 116.25.93.118(1), 113.90.135.223(1)
- `/actuator` 分数 `8.0` 请求 `86` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 120.234.61.168(55), 219.133.80.154(31)
- `/manage` 分数 `8.0` 请求 `85` 源IP `3` 峰值RPS `4` 最大响应 `607`
  主要来源: 120.234.61.168(54), 219.133.80.154(30), 45.138.16.206(1)
- `/manage/env` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)
- `/api/v2/api-docs` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `5` 最大响应 `607`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)
- `/v2/api-docs` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)
- `/api-docs` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)
- `/swagger-ui.html` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)
- `/swagger-ui/index.html` 分数 `8.0` 请求 `84` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 120.234.61.168(54), 219.133.80.154(30)

## 异常大响应样本

- `2026-06-02T08:09:53+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%BA%8C%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260602_%E6%9D%A8%E6%98%A5%E6%9E%97.zip` 状态 `200` 响应 `37318134` 原因 `large-response`
- `2026-06-02T15:11:09+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T15:10:20+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T15:05:21+08:00` `219.133.80.154` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T14:55:10+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T14:47:59+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T14:47:16+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T14:47:15+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T14:47:14+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T10:05:02+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29052992` 原因 `size>812(p95),size>16292x2,size>mean+3stdev`
- `2026-06-02T10:51:32+08:00` `219.133.80.154` `/nh_img/Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `23444828` 原因 `large-response`
- `2026-06-02T10:29:40+08:00` `120.234.61.168` `/nh_img//Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `23444828` 原因 `large-response`
- `2026-06-02T18:40:37+08:00` `123.168.84.249` `/nh_img/Imgs/Original/Approval/039d41ca-3aec-4b7c-9326-338faefb86ff.jpg` 状态 `200` 响应 `3158767` 原因 `large-response`
- `2026-06-02T18:40:37+08:00` `123.168.84.249` `/nh_img/Imgs/Original/Approval/f7234b19-e2ef-4eec-be56-da6c268bae52.jpg` 状态 `200` 响应 `2770909` 原因 `large-response`
- `2026-06-02T18:40:37+08:00` `123.168.84.249` `/nh_img/Imgs/Original/Approval/18419935-a4a1-478b-818a-db4ed14d8783.jpg` 状态 `200` 响应 `2752957` 原因 `large-response`
- `2026-06-02T18:40:37+08:00` `123.168.84.249` `/nh_img/Imgs/Original/Approval/bc2ae5e2-90ef-430b-9796-1a73679c69b5.jpg` 状态 `200` 响应 `2621435` 原因 `large-response`
- `2026-06-02T18:40:37+08:00` `123.168.84.249` `/nh_img/Imgs/Original/Approval/dc6874e8-a1fd-4a52-84b7-602d15a8c41d.jpg` 状态 `200` 响应 `2494545` 原因 `large-response`
- `2026-06-02T10:29:40+08:00` `180.163.29.234` `/nh_img//Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `995448` 原因 `large-response`
- `2026-06-02T18:40:33+08:00` `123.168.84.249` `/nh_approvalweb/static/js/16.76167c81.chunk1751633278474.js` 状态 `200` 响应 `584061` 原因 `large-response`
- `2026-06-02T08:34:43+08:00` `223.160.224.36` `/nh_approvalweb/static/js/16.76167c81.chunk1751633278474.js` 状态 `200` 响应 `584061` 原因 `large-response`

## 路由/源码候选

### `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`

### `/nh_api/Approval/sys/GetSysConfig`

### `/nh_api/auth/login/Authenticket`

### `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup`

### `/nh_healthinstructionweb/`

### `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord`

### `/nh_api/HealthInstruction/ViewRecord/GetClientId`

### `/nh_api/HealthInstruction/Sys/Login`

### `/nh_api/Approval/Project/GetProjectList`

### `/nh_api/Approval/Apply/GetApprovalApplyList`

### `/Home/GetWebSiteAddress`

### `/actuator`

### `/manage`

### `/manage/env`

### `/api/v2/api-docs`

### `/v2/api-docs`

### `/api-docs`

### `/swagger-ui.html`

### `/swagger-ui/index.html`
