# E3 B组分工

## 分工表

| 流程 | B组负责人 | A组对应负责人 | 交互内容 |
|---|---|---|---|
| ① 接口与 README 定义 | B3 谢真婷：接口与 README 负责人 | A组 BuildChecker 负责人 | 项目版本、输入文件、构建命令、验证命令、预期输出、退出码 |
| ② DRAFT 环境与失败样例 | B1 史美一：环境与构建负责人 | A组环境负责人 | Dockerfile、镜像版本、源码 SHA、失败日志、失败原因 |
| ③ MDFixer 固定输入与参考答案 | B2 易容卉：MDFixer 修复负责人 | A组 BuildChecker 负责人 | MD 报告、对应 Makefile、参考 Patch、修复理由 |
| ④ Patch 验证与拒绝恢复 | B4 周逸涵：重跑与验证负责人 | A组检测／复核负责人 | 修复前后行为、无效 Patch 拒绝、原始副本恢复 |
| ⑤ E3 最终整理 | B4 周逸涵：统筹负责人 | A组交付负责人 | README 重跑、人工预期与实际日志对照、失败记录定位 |

## B组 E3 最终留存内容

- DRAFT 源码、Makefile、README 和版本信息。
- `Dockerfile.broken` 与失败日志。
- `Dockerfile.reference`、成功日志、镜像 ID 和功能输出。
- MDFixer 固定 MD 报告及对应 Makefile。
- 参考 Patch、修复验证和拒绝恢复记录。
- 命令、环境、源码 SHA 和个人贡献记录。
