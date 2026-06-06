# Nginx 应急溯源报告

- 生成时间: `2026-06-06T12:40:08.810979+08:00`
- 输入路径: `D:\tmp\anjian\pj\st\test\2026-06-02\home\nginx\var\log\nginx\2026-06-02\barmyy-manage.access.log`
- 日志文件数: `1`
- 有效日志条数: `30557`
- 解析失败条数: `0`

## 结论摘要

- 最高风险 IP: `120.234.61.168`，评分 `104.4`，请求 `19701`，原因 `high-volume, scan-probe, burst, sensitive-path, large-response, server-error-touch, bulk-enumeration`
- 最高风险 URI: `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，评分 `62.6`，请求 `19473`，最大响应 `29053720`
- 热点时间窗: `2026-06-02 14:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `13777`
- 热点时间窗: `2026-06-02 10:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `5650`
- 热点时间窗: `2026-06-02 08:00` `/nh_api/Approval/sys/GetSysConfig` 次数 `2053`
- 热点时间窗: `2026-06-02 09:00` `/actuator` 次数 `30`
- 热点时间窗: `2026-06-02 09:00` `/env` 次数 `30`
- 热点时间窗: `2026-06-02 09:00` `/manage` 次数 `29`
- 热点时间窗: `2026-06-02 09:00` `/manage/env` 次数 `29`
- 热点时间窗: `2026-06-02 09:00` `/api/v2/api-docs` 次数 `29`

## 高风险 IP

- `120.234.61.168` 分数 `104.4` 请求 `19701` 峰值RPS `173` 路径数 `46` 原因 `high-volume, scan-probe, burst, sensitive-path, large-response, server-error-touch, bulk-enumeration`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(19426), /actuator(9), /manage(9), /manage/env(9)
- `219.133.80.154` 分数 `96.39` 请求 `1773` 峰值RPS `32` 路径数 `836` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /actuator(31), /env(31), /manage(30), /manage/env(30)
- `223.160.224.36` 分数 `71.96` 请求 `2211` 峰值RPS `37` 路径数 `62` 原因 `high-volume, burst, sensitive-path, bulk-enumeration, large-response`
  重点路径: /nh_api/Approval/sys/GetSysConfig(2047), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(15), /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(15), /nh_api/Survey/AnswerCard/GetAnswerCardById(15)
- `183.238.10.154` 分数 `50.5` 请求 `440` 峰值RPS `20` 路径数 `82` 原因 `burst, large-response, sensitive-path, server-error-touch`
  重点路径: /Home/GetWebSiteAddress(50), /nh_api/Approval/Sys/GetUserInfo(19), /nh_api/Approval/Apply/GetApprovalApplyResultList(19), /nh_api/Survey/ExternalMedicalRecord/GetQuestSubjectAnswer(15)
- `123.168.84.249` 分数 `45.6` 请求 `94` 峰值RPS `12` 路径数 `79` 原因 `burst, large-response, sensitive-path`
  重点路径: /nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam(4), /nh_api/Survey/AnswerCard/GetAnswerCardById(4), /nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById(3), /nh_api/auth/login/Authenticket(2)
- `45.138.16.206` 分数 `32.0` 请求 `57` 峰值RPS `28` 路径数 `57` 原因 `burst, server-error-touch, sensitive-path`
  重点路径: /(1), /assets/main.js(1), /config.yaml(1), /signin(1)
- `223.104.79.67` 分数 `30.0` 请求 `423` 峰值RPS `33` 路径数 `182` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Approval/sys/GetDepartmentDiseasePageList(24), /nh_api/FileUpload/FileUpload/UploadPictures(20), /nh_api/Approval/Sys/GetDiseaseList(15), /nh_api/Approval/Project/GetProjectList(10)
- `113.84.209.96` 分数 `30.0` 请求 `111` 峰值RPS `12` 路径数 `81` 原因 `burst, sensitive-path`
  重点路径: /nh_api/Approval/Project/GetProjectList(5), /nh_api/Approval/Sys/GetDiseaseList(5), /nh_api/Approval/sys/GetDepartmentDiseasePageList(4), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(3)
- `223.104.79.118` 分数 `24.0` 请求 `173` 峰值RPS `16` 路径数 `33` 原因 `burst, sensitive-path`
  重点路径: /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(15), /nh_healthinstructionweb/(10), /nh_api/auth/login/Authenticket(10), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(10)
- `223.74.154.68` 分数 `21.6` 请求 `50` 峰值RPS `15` 路径数 `46` 原因 `burst, large-response`
  重点路径: /nh_api/HealthInstruction/SearchHealthInstructionInfoList(3), /nh_api/HealthInstruction/Tag/GetHomeTabpageConfigList(2), /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(2), /nh_healthinstructionweb/(1)
- `223.160.229.96` 分数 `21.3` 请求 `65` 峰值RPS `11` 路径数 `59` 原因 `burst, sensitive-path`
  重点路径: /nh_api/auth/login/Authenticket(2), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(2), /nh_img/Imgs/Original/HealthInstruction/quitmenu/60379f51-541a-4c5e-b67e-5d63ef21ce17.png(2), /nh_img/Imgs/Original/HealthInstruction/quitmenu/fbeb2582-0018-42f1-87b4-af5b16b33604.png(2)
- `120.231.210.110` 分数 `19.2` 请求 `56` 峰值RPS `35` 路径数 `56` 原因 `burst, large-response`
  重点路径: /Account/PartnerLogin(1), /Content/lib/layuiadmin/style/admin.css(1), /Content/lib/slider/slider.css(1), /Content/lib/layuiadmin/layui/css/layui.css(1)
- `223.104.77.199` 分数 `19.2` 请求 `31` 峰值RPS `26` 路径数 `31` 原因 `burst, large-response`
  重点路径: /Account/PartnerLogin(1), /Content/lib/layuiadmin/layui/css/layui.css(1), /Content/lib/layuiadmin/style/admin.css(1), /Content/js/jsencrypt.min.js(1)
- `111.55.210.80` 分数 `18.6` 请求 `19` 峰值RPS `2` 路径数 `3` 原因 `sensitive-path, server-error-touch, large-response`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(17), /(1), /favicon.ico(1)
- `120.229.67.97` 分数 `18.0` 请求 `131` 峰值RPS `19` 路径数 `45` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(8), /nh_api/auth/login/Authenticket(7), /nh_img/Imgs/Original/HealthInstruction/quitmenu/b4e3f1bf-bc32-415f-bca7-8cb579113708.png(7), /nh_img/Imgs/Original/HealthInstruction/banner/63a4cf1a-f334-4d59-b71d-df0f35866b06.png(7)
- `223.104.86.75` 分数 `18.0` 请求 `129` 峰值RPS `20` 路径数 `34` 原因 `burst`
  重点路径: /nh_healthinstructionweb/(5), /nh_api/auth/login/Authenticket(5), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(5), /nh_img/Imgs/Original/HealthInstruction/quitmenu/89258f01-c27a-48e6-90c0-977ea8a7f201.png(5)
- `223.104.77.165` 分数 `18.0` 请求 `119` 峰值RPS `21` 路径数 `46` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(8), /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(6), /nh_api/auth/login/Authenticket(4), /nh_healthinstructionweb/(3)
- `223.104.79.22` 分数 `18.0` 请求 `109` 峰值RPS `20` 路径数 `46` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(7), /nh_api/HealthInstruction/ViewRecord/SaveViewRecord(7), /nh_healthinstructionweb/(4), /nh_api/auth/login/Authenticket(4)
- `121.35.185.45` 分数 `18.0` 请求 `88` 峰值RPS `14` 路径数 `45` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(4), /nh_img/Imgs/Original/HealthInstruction/quitmenu/8bdc156e-4d99-441f-a77d-d1c22e15699f.png(4), /nh_img/Imgs/Original/HealthInstruction/quitmenu/a5992422-d41f-4d20-8cbb-209d3b233a2d.png(4), /nh_img/Imgs/Original/HealthInstruction/quitmenu/89258f01-c27a-48e6-90c0-977ea8a7f201.png(4)
- `202.46.225.199` 分数 `18.0` 请求 `81` 峰值RPS `14` 路径数 `33` 原因 `burst`
  重点路径: /nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup(5), /nh_img/Imgs/Original/HealthInstruction/quitmenu/8bdc156e-4d99-441f-a77d-d1c22e15699f.png(5), /nh_img/Imgs/Original/HealthInstruction/quitmenu/a5992422-d41f-4d20-8cbb-209d3b233a2d.png(5), /nh_img/Imgs/Original/HealthInstruction/quitmenu/89258f01-c27a-48e6-90c0-977ea8a7f201.png(5)

## 高风险 URI

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 分数 `62.6` 请求 `19473` 源IP `7` 峰值RPS `173` 最大响应 `29053720`
  主要来源: 120.234.61.168(19426), 111.55.210.80(17), 219.133.80.154(16), 183.238.10.154(7), 223.160.224.36(5)
- `/nh_api/Approval/sys/GetSysConfig` 分数 `47.0` 请求 `2054` 源IP `2` 峰值RPS `37` 最大响应 `768`
  主要来源: 223.160.224.36(2047), 183.238.10.154(7)
- `/nh_api/auth/login/Authenticket` 分数 `39.06` 请求 `219` 源IP `128` 峰值RPS `2` 最大响应 `561`
  主要来源: 219.133.80.154(10), 223.104.79.118(10), 223.104.79.67(8), 120.229.67.97(7), 223.104.86.75(5)
- `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup` 分数 `31.39` 请求 `238` 源IP `126` 峰值RPS `2` 最大响应 `11288`
  主要来源: 219.133.80.154(13), 223.104.79.118(10), 223.104.79.67(8), 120.229.67.97(8), 223.104.79.22(7)
- `/nh_healthinstructionweb/` 分数 `30.65` 请求 `197` 源IP `128` 峰值RPS `1` 最大响应 `8123`
  主要来源: 223.104.79.118(10), 223.104.86.75(5), 120.229.67.97(5), 223.104.79.22(4), 223.104.77.186(4)
- `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord` 分数 `29.86` 请求 `161` 源IP `70` 峰值RPS `2` 最大响应 `88`
  主要来源: 223.104.79.118(15), 223.104.77.165(8), 223.104.79.22(7), 223.104.77.186(6), 116.30.141.124(6)
- `/` 分数 `28.15` 请求 `104` 源IP `74` 峰值RPS `3` 最大响应 `607`
  主要来源: 91.237.124.245(9), 123.160.223.72(4), 114.250.49.47(3), 45.148.10.67(3), 114.250.44.7(3)
- `/nh_api/HealthInstruction/ViewRecord/GetClientId` 分数 `10.0` 请求 `67` 源IP `65` 峰值RPS `1` 最大响应 `88`
  主要来源: 219.133.80.154(2), 223.73.7.78(2), 202.46.225.199(1), 223.73.211.248(1), 119.123.169.14(1)
- `/nh_api/Approval/Project/GetProjectList` 分数 `8.0` 请求 `41` 源IP `6` 峰值RPS `3` 最大响应 `2648`
  主要来源: 219.133.80.154(18), 223.104.79.67(10), 113.84.209.96(5), 120.234.61.168(4), 223.160.229.96(2)
- `/manage` 分数 `8.0` 请求 `40` 源IP `3` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(30), 120.234.61.168(9), 45.138.16.206(1)
- `/actuator` 分数 `8.0` 请求 `40` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(31), 120.234.61.168(9)
- `/manage/env` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/api/v2/api-docs` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/v2/api-docs` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/api-docs` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `607`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/swagger-ui.html` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/swagger-ui/index.html` 分数 `8.0` 请求 `39` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 219.133.80.154(30), 120.234.61.168(9)
- `/nh_api/actuator` 分数 `8.0` 请求 `38` 源IP `2` 峰值RPS `4` 最大响应 `539`
  主要来源: 219.133.80.154(29), 120.234.61.168(9)
- `/nh_api/swagger-ui.html` 分数 `8.0` 请求 `37` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 219.133.80.154(28), 120.234.61.168(9)
- `/nh_api/swagger-ui/index.html` 分数 `8.0` 请求 `37` 源IP `2` 峰值RPS `4` 最大响应 `583`
  主要来源: 219.133.80.154(28), 120.234.61.168(9)

## 异常大响应样本

- `2026-06-02T08:09:53+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%BA%8C%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260602_%E6%9D%A8%E6%98%A5%E6%9E%97.zip` 状态 `200` 响应 `37318134` 原因 `large-response`
- `2026-06-02T15:11:09+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T15:10:20+08:00` `111.55.210.80` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T15:05:21+08:00` `219.133.80.154` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T14:55:10+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T14:47:59+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T14:47:16+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T14:47:15+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T14:47:14+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29053720` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T10:05:02+08:00` `120.234.61.168` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 状态 `200` 响应 `29052992` 原因 `size>812(p95),size>16267x2,size>mean+3stdev`
- `2026-06-02T10:51:32+08:00` `219.133.80.154` `/nh_img/Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `23444828` 原因 `large-response`
- `2026-06-02T10:29:40+08:00` `120.234.61.168` `/nh_img//Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20250618_%E7%A8%8B%E9%88%BA%E5%A9%B7.zip` 状态 `200` 响应 `23444828` 原因 `large-response`
- `2026-06-02T08:15:05+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/cfc1075d-afff-4d92-abaf-d1a7f9d7a9d9.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:15:03+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/497e82f2-936b-40ce-92ec-77f8180bf9c1.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:09:42+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/cfc1075d-afff-4d92-abaf-d1a7f9d7a9d9.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:09:41+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/497e82f2-936b-40ce-92ec-77f8180bf9c1.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:09:22+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/cfc1075d-afff-4d92-abaf-d1a7f9d7a9d9.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:09:20+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/497e82f2-936b-40ce-92ec-77f8180bf9c1.jpeg` 状态 `200` 响应 `3617707` 原因 `large-response`
- `2026-06-02T08:15:03+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/31968741-f9c6-44f5-b9df-cc2768010516.jpeg` 状态 `200` 响应 `3185454` 原因 `large-response`
- `2026-06-02T08:09:40+08:00` `183.238.10.154` `/nh_img/Imgs/Original/Approval/31968741-f9c6-44f5-b9df-cc2768010516.jpeg` 状态 `200` 响应 `3185454` 原因 `large-response`

## 路由/源码候选

### `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`

### `/nh_api/Approval/sys/GetSysConfig`

### `/nh_api/auth/login/Authenticket`

### `/nh_api/HealthInstruction/SpecColumn/GetSpecColumnModuleGroup`

### `/nh_healthinstructionweb/`

### `/nh_api/HealthInstruction/ViewRecord/SaveViewRecord`

### `/nh_api/HealthInstruction/ViewRecord/GetClientId`

### `/nh_api/Approval/Project/GetProjectList`

### `/manage`

### `/actuator`

### `/manage/env`

### `/api/v2/api-docs`

### `/v2/api-docs`

### `/api-docs`

### `/swagger-ui.html`

### `/swagger-ui/index.html`

### `/nh_api/actuator`

### `/nh_api/swagger-ui.html`

### `/nh_api/swagger-ui/index.html`
