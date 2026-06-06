# Nginx 应急溯源报告

- 生成时间: `2026-06-06T13:08:29.014385+08:00`
- 输入路径: `D:\tmp\anjian\pj\st\test`
- 日志文件数: `60`
- 有效日志条数: `2117890`
- 解析失败条数: `14`

## 结论摘要

- 最高风险 IP: `43.247.70.12`，评分 `122.0`，请求 `33523`，原因 `high-volume, scan-probe, burst, large-response, sensitive-path, auth-burst, server-error-touch, bulk-enumeration`
- 最高风险 URI: `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`，评分 `67.0`，请求 `19533`，最大响应 `29053720`
- 热点时间窗: `2026-06-02 14:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `13777`
- 热点时间窗: `2026-06-02 10:00` `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 次数 `5650`
- 热点时间窗: `2026-06-02 17:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3821`
- 热点时间窗: `2026-06-03 10:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3658`
- 热点时间窗: `2026-06-01 17:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3582`
- 热点时间窗: `2026-06-04 15:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3516`
- 热点时间窗: `2026-06-04 14:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3472`
- 热点时间窗: `2026-06-01 11:00` `/ih/appletQuery/api/Message/GetUserMessage` 次数 `3443`

## 高风险 IP

- `43.247.70.12` 分数 `122.0` 请求 `33523` 峰值RPS `49` 路径数 `820` 原因 `high-volume, scan-probe, burst, large-response, sensitive-path, auth-burst, server-error-touch, bulk-enumeration`
  重点路径: /ihtest/appletQuery/api/Message/GetUserMessage(11459), /favicon.ico(3170), /ihtest/appletQuery/api/TreatmentRoom/GetTreatRecordsCount(1393), /ihtest/appletQuery/api/TreatmentRoom/GetTreatRecords(1390)
- `58.60.110.201` 分数 `119.2` 请求 `59428` 峰值RPS `49` 路径数 `839` 原因 `high-volume, scan-probe, burst, large-response, sensitive-path, auth-burst, server-error-touch, bulk-enumeration`
  重点路径: /ih/appletQuery/api/DispMed/GetAllUnAutoprintedInfo(10122), /ih/appletQuery/api/Support/GetHandlePageList(2717), /ih/appletQuery/api/Support/GetSuprtHandleTabSum(2276), /ih/appletQuery/api/SendMed/GetListDrugTraceabilityCode(1858)
- `120.234.61.168` 分数 `114.4` 请求 `21851` 峰值RPS `173` 路径数 `879` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, server-error-touch, bulk-enumeration`
  重点路径: /nh_api/Approval/Apply/GetApplyRecordContextbyApplyId(19426), /actuator(55), /env(55), /manage(54)
- `112.97.203.114` 分数 `113.2` 请求 `16314` 峰值RPS `198` 路径数 `10265` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, bulk-enumeration, large-response`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(3157), /ih/appletQuery/api/Patient/GetPatientList(168), /ih/ihapp/api/dic/ItemOptions(125), /ih/appletQuery/api/Hospital/GetHospitalIntroduction(93)
- `120.234.61.169` 分数 `113.0` 请求 `6660` 峰值RPS `79` 路径数 `1642` 原因 `high-volume, scan-probe, bulk-enumeration, burst, sensitive-path, auth-burst, server-error-touch`
  重点路径: /actuator(158), /env(158), /manage(157), /manage/env(157)
- `219.133.80.155` 分数 `113.0` 请求 `5805` 峰值RPS `61` 路径数 `1288` 原因 `high-volume, scan-probe, bulk-enumeration, burst, sensitive-path, auth-burst, server-error-touch`
  重点路径: /env(160), /actuator(160), /manage(159), /manage/env(159)
- `223.104.79.91` 分数 `100.8` 请求 `6239` 峰值RPS `27` 路径数 `248` 原因 `high-volume, scan-probe, burst, sensitive-path, large-response, auth-burst`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(523), /ih/appletQuery/api/SystemData/GetSystemConfig(235), /ih/appletQuery/api/StaticResources/GetStaticResources(209), /ih/appletQuery/api/Hospital/GetHospitalIntroduction(188)
- `219.133.80.154` 分数 `96.39` 请求 `1773` 峰值RPS `32` 路径数 `836` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, server-error-touch, large-response`
  重点路径: /actuator(31), /env(31), /manage(30), /manage/env(30)
- `223.104.68.197` 分数 `96.25` 请求 `1269` 峰值RPS `29` 路径数 `76` 原因 `high-volume, burst, scan-probe, large-response, sensitive-path, auth-burst`
  重点路径: /ih/ihapp/api/dic/ItemOptions(126), /ih/appletQuery/api/Message/GetUserMessage(92), /ih/appletQuery/api/Report/GetMZJCReportList(67), /ih/appletQuery/api/Report/GetMZJYReportList(58)
- `223.104.79.99` 分数 `96.13` 请求 `2604` 峰值RPS `28` 路径数 `186` 原因 `high-volume, scan-probe, burst, sensitive-path, auth-burst, large-response, bulk-enumeration`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(147), /ih/appletquery/api/register/GetInquirePic(121), /ih/appletQuery/api/SystemData/GetSystemConfig(110), /ih/appletQuery/api/Hospital/GetHospitalIntroduction(92)
- `123.207.100.105` 分数 `95.77` 请求 `834` 峰值RPS `22` 路径数 `105` 原因 `high-volume, scan-probe, burst, large-response, sensitive-path, server-error-touch`
  重点路径: /favicon.ico(79), /im/IHFile/HospitalPicture/552438833074245_20240530105924001872.png(57), /im/IHFile/HospitalPicture/552438555787333_20240530105816304142.png(57), /im/IHFile/HospitalPicture/552438481199173_20240530105758094180.png(57)
- `223.104.79.66` 分数 `95.54` 请求 `1388` 峰值RPS `30` 路径数 `243` 原因 `high-volume, scan-probe, burst, sensitive-path, bulk-enumeration, auth-burst, large-response`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(65), /ih/ihapp/api/dic/ItemOptions(54), /ih/appletQuery/api/Patient/GetPatientList(50), /ih/appletquery/api/register/GetInquirePic(47)
- `223.104.79.46` 分数 `95.27` 请求 `1354` 峰值RPS `25` 路径数 `116` 原因 `high-volume, burst, scan-probe, large-response, sensitive-path, auth-burst`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(111), /ih/appletQuery/api/Report/GetMZJCReportList(107), /ih/appletQuery/api/Report/GetMZJYReportList(100), /ih/ihapp/api/dic/ItemOptions(99)
- `10.17.99.67` 分数 `94.0` 请求 `38821` 峰值RPS `15` 路径数 `373` 原因 `high-volume, burst, large-response, sensitive-path, auth-burst, server-error-touch`
  重点路径: /hlwyy_wxjk/sns/jscode2session(16182), /hlwyy_ca/am/v2/recipe/getSignOrderStatus(4378), /sfwulnew/(3616), /med-biz/api/mipuserquery/userQuery/20003892(2165)
- `113.84.64.206` 分数 `93.03` 请求 `2395` 峰值RPS `35` 路径数 `273` 原因 `high-volume, scan-probe, burst, sensitive-path, bulk-enumeration, auth-burst`
  重点路径: /ih/appletQuery/api/Message/GetUserMessage(738), /ih/appletQuery/api/Inquiry/GetInquiryRecord(130), /GetResDataInfo(102), /ih/appletQuery/api/Patient/GetPatientList(101)

## 高风险 URI

- `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId` 分数 `67.0` 请求 `19533` 源IP `20` 峰值RPS `173` 最大响应 `29053720`
  主要来源: 120.234.61.168(19426), 183.238.10.154(27), 112.97.203.114(20), 111.55.210.80(17), 219.133.80.154(16)
- `/ih/appletquery/api/register/GetInquirePic` 分数 `56.0` 请求 `10034` 源IP `818` 峰值RPS `22` 最大响应 `6246037`
  主要来源: 58.60.110.201(717), 163.125.239.52(260), 113.84.130.208(176), 113.84.169.105(165), 119.123.135.200(160)
- `/favicon.ico` 分数 `49.0` 请求 `3704` 源IP `208` 峰值RPS `32` 最大响应 `1163`
  主要来源: 43.247.70.12(3170), 58.60.110.201(129), 123.207.100.105(79), 183.238.10.154(34), 183.17.53.247(13)
- `/ih/appletQuery/api/Inquiry/GetInquiryRecord` 分数 `49.0` 请求 `3257` 源IP `210` 峰值RPS `80` 最大响应 `14343`
  主要来源: 112.97.65.47(654), 113.84.160.86(351), 223.104.67.51(323), 116.22.207.174(230), 120.229.202.64(136)
- `/ih/appletQuery/api/Message/GetUserMessage` 分数 `48.5` 请求 `168523` 源IP `8401` 峰值RPS `27` 最大响应 `49198`
  主要来源: 112.97.203.114(3157), 120.229.162.96(1140), 112.97.65.47(967), 123.168.84.249(921), 58.60.110.201(851)
- `/nh_api/Approval/sys/GetSysConfig` 分数 `47.0` 请求 `2782` 源IP `4` 峰值RPS `37` 最大响应 `768`
  主要来源: 223.160.224.36(2047), 223.104.79.38(707), 183.238.10.154(27), 43.247.70.12(1)
- `/api-docs` 分数 `46.26` 请求 `404` 源IP `6` 峰值RPS `20` 最大响应 `607`
  主要来源: 219.133.80.155(159), 120.234.61.169(157), 120.234.61.168(54), 219.133.80.154(30), 112.97.203.114(3)
- `/actuator` 分数 `45.8` 请求 `408` 源IP `6` 峰值RPS `19` 最大响应 `607`
  主要来源: 219.133.80.155(160), 120.234.61.169(158), 120.234.61.168(55), 219.133.80.154(31), 112.97.203.114(3)
- `/swagger-ui/index.html` 分数 `45.76` 请求 `404` 源IP `6` 峰值RPS `19` 最大响应 `583`
  主要来源: 219.133.80.155(159), 120.234.61.169(157), 120.234.61.168(54), 219.133.80.154(30), 112.97.203.114(3)
- `/ih/ihapp/api/dic/ItemOptions` 分数 `45.0` 请求 `114187` 源IP `8387` 峰值RPS `20` 最大响应 `26247`
  主要来源: 58.60.110.201(1273), 123.168.84.249(334), 223.104.79.91(183), 111.55.210.75(177), 119.123.66.43(161)
- `/ih/appletQuery/api/Report/GetMZJYReportList` 分数 `45.0` 请求 `18463` 源IP `2607` 峰值RPS `4` 最大响应 `144137`
  主要来源: 112.97.57.97(144), 183.7.151.128(143), 120.229.94.39(114), 223.104.79.46(100), 14.31.228.156(97)
- `/` 分数 `45.0` 请求 `13837` 源IP `1470` 峰值RPS `4` 最大响应 `14193411`
  主要来源: 10.17.100.212(73), 171.105.52.115(48), 45.148.10.67(35), 116.8.56.107(24), 116.8.54.87(24)
- `/ih/appletQuery/api/Inquiry/GetInquiryRecords` 分数 `45.0` 请求 `10003` 源IP `1349` 峰值RPS `4` 最大响应 `51164`
  主要来源: 58.60.110.201(574), 113.84.65.63(158), 120.229.67.56(146), 223.104.79.58(145), 223.104.79.91(144)
- `/ih/ihapp/api/user/detail` 分数 `45.0` 请求 `9778` 源IP `1400` 峰值RPS `3` 最大响应 `118064`
  主要来源: 58.60.110.201(773), 223.104.79.58(237), 223.104.79.91(183), 223.104.80.74(153), 113.84.65.63(138)
- `/ih/appletQuery/api/Prescription/GetAllPresTmp` 分数 `45.0` 请求 `3641` 源IP `231` 峰值RPS `3` 最大响应 `271417`
  主要来源: 58.60.110.201(397), 42.80.117.72(144), 112.97.84.188(91), 223.104.79.91(87), 113.84.34.169(75)

## 异常大响应样本

- `2026-06-04T00:10:21+08:00` `10.17.99.67` `/27653671vodcq1258870619/dff5ae185001834805833223048/f0.mp4` 状态 `200` 响应 `71984563` 原因 `large-response`
- `2026-06-04T00:15:54+08:00` `10.17.99.67` `/27653671vodcq1258870619/2859f4bc5001834805834037453/f0.mp4` 状态 `200` 响应 `71880633` 原因 `large-response`
- `2026-06-04T10:58:27+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%B8%80%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260604_%E5%BC%A0%E6%B4%AA%E5%AE%9D.zip` 状态 `200` 响应 `63884311` 原因 `large-response`
- `2026-06-04T00:09:28+08:00` `10.17.99.67` `/27653671vodcq1258870619/d441e2bf5001834805392193940/f0.mp4` 状态 `200` 响应 `51778350` 原因 `large-response`
- `2026-06-04T00:06:38+08:00` `10.17.99.67` `/27653671vodcq1258870619/d49597ed5145403728229767187/f0.mp4` 状态 `200` 响应 `44954936` 原因 `large-response`
- `2026-06-04T00:11:31+08:00` `10.17.99.67` `/27653671vodcq1258870619/d4a3d9845145403728229770166/f0.mp4` 状态 `200` 响应 `44055125` 原因 `large-response`
- `2026-06-04T00:14:12+08:00` `10.17.99.67` `/27653671vodcq1258870619/76fa98ab5001834805726996373/f0.mp4` 状态 `200` 响应 `43223269` 原因 `large-response`
- `2026-06-04T00:11:02+08:00` `10.17.99.67` `/27653671vodcq1258870619/1f6ee15b5001834805718710426/f0.mp4` 状态 `200` 响应 `43084428` 原因 `large-response`
- `2026-06-04T00:16:11+08:00` `10.17.99.67` `/27653671vodcq1258870619/8cfcf3d55001834805920732250/f0.mp4` 状态 `200` 响应 `41276629` 原因 `large-response`
- `2026-06-04T00:06:25+08:00` `10.17.99.67` `/27653671vodcq1258870619/139f41ba5001834805419912711/f0.mp4` 状态 `200` 响应 `40721608` 原因 `large-response`
- `2026-06-04T00:08:01+08:00` `10.17.99.67` `/27653671vodcq1258870619/57d54eb85001834805410615835/f0.mp4` 状态 `200` 响应 `40156701` 原因 `large-response`
- `2026-06-04T00:07:01+08:00` `10.17.99.67` `/27653671vodcq1258870619/05f5930a5001834805854299257/f0.mp4` 状态 `200` 响应 `39523013` 原因 `large-response`
- `2026-06-04T00:05:50+08:00` `10.17.99.67` `/27653671vodcq1258870619/e7a57e3a5001834805382143455/f0.mp4` 状态 `200` 响应 `38853375` 原因 `large-response`
- `2026-06-02T08:09:53+08:00` `183.238.10.154` `/nh_img/Files/Approval/%E4%BA%8C%E7%B1%BB%E9%97%A8%E8%AF%8A%E7%89%B9%E7%97%85%E7%94%B3%E8%AF%B7_20260602_%E6%9D%A8%E6%98%A5%E6%9E%97.zip` 状态 `200` 响应 `37318134` 原因 `large-response`
- `2026-06-04T00:20:01+08:00` `10.17.99.67` `/27653671vodcq1258870619/acd121c35001834805768071906/f0.mp4` 状态 `200` 响应 `32604158` 原因 `large-response`

## 路由/源码候选

### `/nh_api/Approval/Apply/GetApplyRecordContextbyApplyId`

### `/ih/appletquery/api/register/GetInquirePic`

### `/favicon.ico`

### `/ih/appletQuery/api/Inquiry/GetInquiryRecord`

### `/ih/appletQuery/api/Message/GetUserMessage`

### `/nh_api/Approval/sys/GetSysConfig`

### `/api-docs`

### `/actuator`

### `/swagger-ui/index.html`

### `/ih/ihapp/api/dic/ItemOptions`

### `/ih/appletQuery/api/Report/GetMZJYReportList`

### `/ih/appletQuery/api/Inquiry/GetInquiryRecords`

### `/ih/ihapp/api/user/detail`

### `/ih/appletQuery/api/Prescription/GetAllPresTmp`
