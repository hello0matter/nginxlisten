# Nginx 应急溯源报告

- 生成时间: `2026-06-06T13:39:21.206009+08:00`
- 输入路径: `D:\tmp\anjian\pj\st\tmp\nginxlisten\output-log-test4\_agent_batch\20260606_133915\0000\barmyy-manage.access.log`
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

## 待人工研判 IP

- 分层明细: [D:\tmp\anjian\pj\st\tmp\nginxlisten\output-log-test4\review_ips.csv](D:\tmp\anjian\pj\st\tmp\nginxlisten\output-log-test4\review_ips.csv)
- 高优先级研判: `120.234.61.168, 219.133.80.154, 223.160.224.36`
- 观察 IP: `183.238.10.154, 123.168.84.249, 45.138.16.206, 223.104.79.67, 113.84.209.96, 223.104.79.118, 223.74.154.68, 120.231.210.110, 223.104.77.199, 120.229.67.97, 223.104.86.75, 223.104.77.165, 223.104.79.22, 223.104.77.186, 223.73.7.78, 39.146.13.74, 112.97.82.125, 223.104.67.51, 113.84.82.114, 113.84.130.208`

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

## AI 研判

**研判结论**

本次日志显示存在明显异常访问，核心风险是“敏感业务接口高频批量调用 + 管理/调试端点探测 + 大响应数据疑似泄露”。

攻击方式主要包括：

1. **业务接口批量枚举/数据拉取**
   - 重点 IP：`120.234.61.168`
   - 对 `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 发起 `19426` 次请求，峰值 `173 rps`。
   - 该接口返回大量 `200`，且多次出现 `29MB` 级响应，疑似批量获取审批申请详情、病种/患者/附件等敏感审批数据。
   - 状态码中同时存在大量 `400`、`500`，说明可能伴随参数探测、越权尝试或接口压力触发异常。

2. **Spring Boot / Swagger / 管理端点探测**
   - 出现 `/actuator`、`/env`、`/manage`、`/manage/env`、`/v2/api-docs`、`/swagger-ui.html`、`/api-docs` 等路径探测。
   - 重点 IP：`120.234.61.168`、`219.133.80.154`、`45.138.16.206`
   - 多数返回 `500` 或 `404`，但这类路径属于高危敏感面，若暴露可能导致环境变量、配置、接口文档或管理能力泄露。

3. **目录/路径扫描**
   - `219.133.80.154` 请求 `1773` 次，访问 `836` 个不同路径，`404` 占比较高，符合自动化扫描特征。
   - `45.138.16.206` 请求 `/config.yaml`、`/cp.php`、`/signin`、`/security.txt`、`/assets/main.js` 等通用探测路径，偏互联网扫描器行为。

4. **大文件/敏感附件访问**
   - `/nh_img/Files/Approval/...zip` 返回 `37MB`，文件名包含“二类门诊特病申请”等敏感业务语义。
   - 该类附件访问需要重点确认是否经过鉴权、是否存在直链可下载或越权下载问题。

**是否疑似成功**

疑似成功，至少存在较高概率的数据读取成功。

依据：

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 返回 `200` 达 `14429` 次。
- 单个攻击 IP `120.234.61.168` 总响应流量约 `251MB`，该接口多次返回 `29MB`。
- 该接口属于审批详情类敏感接口，且命中量远超正常用户行为。
- 另有审批附件 ZIP 文件成功返回 `200`，大小 `37MB`。
- 管理端点探测多数为 `500/404`，暂不支持“管理端点已成功利用”的结论，但说明存在被扫描探测。

综合判断：**业务数据批量读取/越权访问疑似成功；管理端点利用暂未见成功证据；存在接口被打爆导致 500 的服务稳定性风险。**

**后续核查建议**

1. **优先核查应用业务日志**
   - 按 `real_ip=120.234.61.168`、`111.55.210.80`、`219.133.80.154` 查询 2026-06-02 `10:00-15:30` 期间的登录态、用户 ID、token、审批单 ID、请求体参数。
   - 特别还原 `/GetApplyRecordContextbyApplyId` 的请求参数，确认是否固定 ID、批量 ID、空参数、越权 ID 或绕过鉴权。

2. **核查鉴权与越权**
   - 检查 `GetApplyRecordContextbyApplyId` 是否仅依赖前端传参或 referer。
   - 验证当前用户是否只能访问自己权限范围内的审批单。
   - 检查接口是否在 POST body 中传 `applyId`，日志未记录 query 参数，需结合应用日志或 WAF 日志补齐。

3. **核查数据泄露范围**
   - 统计 `200` 响应对应的审批单、患者、附件、病种、科室、手机号、身份证、医保等敏感字段访问量。
   - 对 `29MB` 响应内容对应的业务对象做落库审计。
   - 核查 `/nh_img/Files/Approval/*.zip` 是否可被未授权下载，是否存在可猜测路径。

4. **核查账号风险**
   - 对异常 IP 使用的账号执行强制下线、token 失效、密码重置或二次验证。
   - 排查 `/nh_api/auth/login/Authenticket` 的登录票据是否可重放，是否存在弱校验、固定 ticket、跨用户复用。

5. **核查服务器异常**
   - 对 `/actuator`、`/env`、`/manage`、`/swagger*`、`/api-docs` 的 `500` 查应用错误日志，确认是否抛出敏感异常、堆栈、配置路径或触发后端异常。
   - 检查是否有异常文件写入、计划任务、webshell、异常出站连接。

6. **立即处置**
   - 临时封禁或限速：`120.234.61.168`、`219.133.80.154`、`45.138.16.206`。
   - 对 `/GetApplyRecordContextbyApplyId` 加强限流、鉴权、审计和响应字段脱敏。
   - 关闭公网暴露的 actuator、swagger、api-docs、env、manage 类端点。

**需要优先保护的接口**

高优先级：

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`
- `/nh_api/Approval/sys/GetSysConfig`
- `/nh_img/Files/Approval/*`
- `/nh_api/auth/login/Authenticket`
- `/nh_api/Approval/Apply/GetApprovalApplyList`
- `/nh_api/Approval/Sys/GetUserInfo`
- `/nh_api/Approval/process/ProcessApply`
- `/nh_api/FileUpload/FileUpload/UploadPictures`

管理/调试端点必须封闭：

- `/actuator`
- `/env`
- `/manage`
- `/manage/env`
- `/v2/api-docs`
- `/api/v2/api-docs`
- `/api-docs`
- `/swagger-ui.html`
- `/swagger-ui/index.html`
- `/nh_api/actuator`
- `/nh_api/env`
- `/nh_api/manage`
- `/nh_api/manage/env`

业务敏感数据接口也建议纳入重点审计：

- `/nh_api/Survey/QuestionnaireManage/GetQuestSubjectsById`
- `/nh_api/Survey/ExternalMedicalRecord/QueryAnswerCardIdByQParam`
- `/nh_api/Survey/AnswerCard/GetAnswerCardById`
- `/nh_api/Survey/ExternalMedicalRecord/GetQuestSubjectAnswer`

总体定级建议：**高危事件，按疑似敏感数据泄露处置。**
