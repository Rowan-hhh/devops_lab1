# E3 A组 ⑤ 最终整理与交付说明

## 元信息

| 项目       | 内容                                                                               |
| -------- | -------------------------------------------------------------------------------- |
| 交付角色     | A组交付负责人（⑤）                                                                       |
| 对应流程     | ⑤ E03 最终整理与交付                                                                    |
| 对接方      | B组 B4 重跑与交付负责人                                                                   |
| 整理日期     | 2026-10-10（2026-10-11 补齐环境节）                                                     |
| 覆盖范围     | README 重跑步骤、C0/C1/C2 Git SHA、人工预期与实际日志对照、检测报告、**环境信息**、失败定位、相互检查                 |
| 与 E4 的边界 | ⑤ 只做**文档级**整理与往返确认；"交换仓库、按 README 实际重跑并对照结果"属 **E4 相互检查**（E4 PPT E4/20），不在 E3 范围 |
| 交付状态     | ✅ **完成**（内容含环境节 + B4 文档级往返确认已回执；实际重跑对照移交 E4）                                        |

> 本文件是 ⑤ 的整理稿，配合 A组 ①③ 基线目录 `A-BuildChecker-E3测试基线/` 与 ④ 复核记录 `E3-A组④检测复核记录.md` 使用。

> 依据（重新核对）：E3 PPT E3/10「提交要求」（A组 MD/RD+判断依据、C0/C1/C2 版本及预期变化；共同信息 README、环境、命令与日志、仓库 SHA 与个人贡献；未完成也要记录）、E3 PPT E3/11「相互检查」四问、`docs/E3A组分工.png` ⑤ 行。



---

## 1. 交付物总览（共同信息：仓库 / SHA / 个人贡献）

| 项            | 值                                                                |
| ------------ | ---------------------------------------------------------------- |
| 仓库           | <https://github.com/Rowan-hhh/devops_lab1>                       |
| 分支           | `main`                                                           |
| 上游 main（整理时） | `c1a74156`（feat(E3/A): verify MD-RD GHCR handoff）                |
| A组 ①③ 基线提交   | `b7116cd`、`cd7a428`（作者 `pengyu-kong`）                            |
| A组 ④ 复核记录    | `8234bb0`（作者 `SunShine_06`；PR #2 已并入上游 main）                     |
| A组 ② 环境消费/接收 | `c1a74156`（verify MD-RD GHCR handoff，作者 `Zane`）                  |
| B1 环境包提交     | `fa07b7199e985b1dda63cc2efa467e5eb5a0f0ee`（作者 `241880179`）       |
| 主要产物位置       | `A-BuildChecker-E3测试基线/`（基线+证据+`B1-MD-RD环境/`）、`A-检测复核交接/`（④⑤ 记录） |
| 个人贡献（⑤）      | 整理本文与 ④ 复核记录                                                     |

---

## 2. README 重跑步骤（别人如何复现）

在**仓库根目录**执行，Windows 请用 WSL（需 GNU Make + C 编译器，全程不需要网络）：

```text
# 基线（检测项目与全量报告）
python3 A-BuildChecker-E3测试基线/scripts/run_a_buildchecker.py --check-only
python3 A-BuildChecker-E3测试基线/scripts/run_a_buildchecker.py

# B1 MD/RD 专用环境包（不调用 Docker 的静态检查 → 本机构建与验收）
python "A-BuildChecker-E3测试基线/B1-MD-RD环境/run_b1_md_rd.py" --check-only
python "A-BuildChecker-E3测试基线/B1-MD-RD环境/run_b1_md_rd.py"
```

要点：

- 两个脚本**每次都写新的 `evidence/run-YYYYMMDDTHHMMSSZ/` 目录，不覆盖、不删除已有记录**。
- 已核实的工具链版本：GNU Make 4.3、`cc` 13.3.0（Ubuntu 13.3.0-6ubuntu2~24.04.1）、Python 3.12.3、x86_64、WSL2 Ubuntu。
- 构建/验证命令：`make` / `./app`；`make clean` 仅供本地复跑。

---

## 3. C0 / C1 / C2 的 Git SHA 与预期输出

| 标签       | SHA                                        | 干净构建 `./app` | 预期发现                        | configuration_id |
| -------- | ------------------------------------------ | ------------ | --------------------------- | ---------------- |
| C0       | `4f985129bb100b082fe2cfb4f95f846d00752a25` | `10`         | 无                           | `cc-MODE0`       |
| C1       | `9c3e06606aa42afef25c53dbb5eb0c5a6330e5ea` | `12`         | MD `feature.h`              | `cc-MODE0`       |
| C2       | `5efd7ece7569439950881a9b52b184356aa91687` | `19`         | 上述 MD 仍在（`feature.h`）       | `cc-MODE7`       |
| MD/RD 快照 | `39430e3cdcf16403eec63bf592129b50ab1ff53d` | `1`          | MD `config.h`，RD `unused.h` | `cc-default`     |

- SHAs 取自 canonical 运行 `evidence/run-20261010T051714Z/commits/*.sha`（由运行器生成，与课件行为绑定），**不是** GitHub `main` 上的三个独立 commit。
- MD/RD 有两个身份，勿混用：**canonical repository commit** = `29c02d6604d7071d4b249ec958dd8a553caa670a`（GH `main` 可检出）；**standalone snapshot bundle SHA** = `39430e3...`（运行器内部快照，`snapshot_commit`，仅本地重现用）。`snapshot-equivalence.json` 证明二者五个项目文件字节一致。
- C1→C2 仅 `CFLAGS` 增加 `-DMODE=7`（源码不变）；C2 保留 C1 产物后普通 `make` 输出仍 `12`（`Nothing to be done for 'all'`），干净构建 `19`。这是命令变化，**不是**新的 MISSING/RD。

---

## 4. 人工预期与实际日志对照

### 4.1 MD/RD（canonical 运行 `evidence/run-20261010T051714Z/`）

| 检查                     | 人工预期（oracle）                 | 实际观察                                       | 结论 |
| ---------------------- | ---------------------------- | ------------------------------------------ | -- |
| 首次 `./app`             | `1\n`                        | 匹配                                         | ✅  |
| 只改 `config.h` 后普通 make | 仍为 `1\n`（漏重建）                | 匹配                                         | ✅  |
| `make clean && make`   | `2\n`                        | 匹配                                         | ✅  |
| 只改 `unused.h`          | 触发再次 `cc -c main.c`（RD 多余编译） | 匹配                                         | ✅  |
| 依赖发现                   | MD `config.h`、RD `unused.h`  | 与 `oracle/md-rd/expected-findings.json` 一致 | ✅  |

### 4.2 C0 / C1 / C2

| 版本 | 干净输出 预期→实际  | 增量行为 预期→实际                  | 结论 |
| -- | ----------- | --------------------------- | -- |
| C0 | `10` → `10` | —                           | ✅  |
| C1 | `12` → `12` | —                           | ✅  |
| C2 | `19` → `19` | 保留 C1 产物普通 make `12` → `12` | ✅  |

> 依据文件：`docs/md-rd-oracle.md`（人工预期与判断依据）、`oracle/*/expected-findings.json`、`evidence/FINAL_RESULT.md`。

---

## 5. 检测报告（ERROR_REPORT 汇总）

范围：`main.o` 的项目头文件；系统头文件不在范围内。检测器 `detector = INSTRUCTOR_ORACLE`（仅作人工预期，不计入工具准确率）。

**canonical 报告**：`evidence/run-20261010T051714Z/md-rd/artifacts/error-report.json`，`repository.commit = 29c02d66…`，`producer_job_id = job-e3-a-md-rd-29c02d66`，报告 SHA-256 = `7b021f47912e16bf43e084f23eaa7ecae59f42fa34a33f02b0c97b7ccdb00f22`。

| 报告    | configuration_id | findings                                                                                                  |
| ----- | ---------------- | --------------------------------------------------------------------------------------------------------- |
| MD/RD | `cc-default`     | `finding-e3-md-rd-missing-001`（MISSING，`config.h`）、`finding-e3-md-rd-redundant-001`（REDUNDANT，`unused.h`） |
| C0    | `cc-MODE0`       | 无                                                                                                         |
| C1    | `cc-MODE0`       | `finding-e3-c1-missing-001`（MISSING，`feature.h`）                                                          |
| C2    | `cc-MODE7`       | `finding-e3-c2-missing-001`（MISSING，`feature.h`）                                                          |

- 给 B2 的旧交接副本仍为 `handoff/b2/md-rd.error-report.json`、`handoff/b2/c1.error-report.json`（绑定 standalone SHA `39430e3…`，B2/B4 候选验证沿用此 base）。
- B2 只应选 `MISSING`，RD（`unused.h`）必须保留在报告里、不进入修复流程。

---

## 6. 失败定位

| 目录                     | 结果           | 定位（卡在哪 / 试过什么 / 版本）                                                           |
| ---------------------- | ------------ | ----------------------------------------------------------------------------- |
| `run-20261010T051714Z` | `ACCEPTED`   | **canonical-main 报告**：`repository.commit=29c02d6…`，`producer_job_id` 唯一       |
| `run-20261010T050126Z` | `SUPERSEDED` | 中间 canonical-main 尝试复用了 producer Job ID；保留原始记录，不用于交接                          |
| `run-20261005T071837Z` | `ACCEPTED`   | WSL2 Ubuntu；含 `strace` 读取 `config.h` 记录；绑定 standalone snapshot SHA `39430e3…` |
| `run-20261005T071754Z` | `REJECTED`   | 复制 C2 源码刷新了 `main.c` 时间戳，导致增量误重建（定位到 **C2 增量判定**）                             |
| `run-20261005T071651Z` | 中断           | 建 C0/C1/C2 证据目录前失败（`commits/` 未 mkdir）；MD/RD 行为实验已跑完。见该目录 `FAILED.txt`        |

- 上述失败/中间目录**全部保留、不覆盖**，可直接引用作为“未完成也要记录：当前代码与失败日志、卡在哪里”。
- **可复现性佐证**：`run-20261005T071837Z`、`run-20261005T073014Z`、`run-20261005T073037Z` 三次均为 `ACCEPTED`，MD/RD 与 C0/C1/C2 的 SHA、输出、发现逐项一致。
- 说明：上游 `FINAL_RESULT.md` 现已明确 **canonical 运行 = `run-20261010T051714Z`**，`071837Z` 列为历史（WSL2/strace）。此前对“最新有效运行”口径的疑虑由此关闭；`073014Z`/`073037Z` 仍在 evidence 目录中，但未列入该 `FINAL_RESULT.md` 的历史表。

---

## 7. 相互检查（对照 PPT「相互检查」四问）

| 检查项             | 自查结论                                                                                                            | 支撑    |
| --------------- | --------------------------------------------------------------------------------------------------------------- | ----- |
| 别人能按 README 运行吗 | 材料已就绪：README 给出基线与环境包两条命令 + WSL/Linux（GNU Make + cc，无需网络），三次同构 `ACCEPTED` 运行佐证可复现；**实际按 README 重跑对照留待 E4 相互检查** | §2、§6 |
| 人工答案和实际日志分清了吗   | 已分离：人工预期在 `oracle/` 与 `docs/md-rd-oracle.md`（标 `INSTRUCTOR_ORACLE`），实际观察在 `evidence/run-*/`                     | §4    |
| 预期结果能说明依据吗      | 能：`docs/md-rd-oracle.md` 给出行为证据（改 `config.h` 输出不变、改 `unused.h` 触发重编译）                                           | §4.1  |
| 失败记录能定位到具体版本吗   | 能：`071651Z` 定位到“建目录步骤”，`071754Z` 定位到 **C2 增量**；目录保留不覆盖                                                          | §6    |

---

## 8. 环境信息（② 已完成，本节补齐）

环境部分由 **B1（环境包）+ A组环境负责人（消费与跨机器接收验证）** 完成。E3 **不要求部署或调用 DRAFT API**（`draft-input.json.api_status = NOT_INVOKED_OUT_OF_E3_SCOPE`）。

### 8.1 环境包（B1）

| 项         | 值                                                                                           |
| --------- | ------------------------------------------------------------------------------------------- |
| B1 环境包提交  | `fa07b7199e985b1dda63cc2efa467e5eb5a0f0ee`                                                  |
| 目录        | `A-BuildChecker-E3测试基线/B1-MD-RD环境/`（`Dockerfile`、`run_b1_md_rd.py`、`README.md`、`evidence/`） |
| 源码目录 / 基线 | `A-BuildChecker-E3测试基线/fixtures/md-rd/`，commit `29c02d6604d7071d4b249ec958dd8a553caa670a`   |
| 项目标识      | `e3-buildchecker-md-rd@2026-09-10`                                                          |
| 镜像 tag    | `e3-buildchecker-md-rd:b1-20260910`                                                         |
| 平台        | `linux/amd64`                                                                               |
| 本机验收      | `B1-MD-RD环境/evidence/run-20261010T080813Z/` = `ACCEPTED`                                    |

### 8.2 跨机器 image_ref（GHCR）

```text
image_ref = ghcr.io/zaneow0/e3-buildchecker-md-rd@sha256:5be5d74a921c8600aeb4ac7a62bdea27f74521008264130039849b8309c285d6
```

| 项               | 值                                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| Registry        | GitHub Container Registry (GHCR)                                                                     |
| 拉取命令            | `docker pull --platform linux/amd64 ghcr.io/zaneow0/e3-buildchecker-md-rd@sha256:5be5d74a…`（退出码 `0`） |
| manifest digest | `sha256:5be5d74a921c8600aeb4ac7a62bdea27f74521008264130039849b8309c285d6`                            |
| Docker Image ID | `sha256:5be5d74a…`（与发布 digest 一致）                                                                    |
| OS / 架构         | `linux/amd64`                                                                                        |
| label           | 源码 revision `29c02d66…`；项目 `e3-buildchecker-md-rd@2026-09-10`                                        |
| 断网运行            | `docker run --rm --network none e3-buildchecker-md-rd:b1-20260910` → 退出码 `0`，stdout `1\n`            |

本地 tar 交付（备用，非跨机器依据）：`B1-MD-RD环境/evidence/e3-buildchecker-md-rd.tar`，`98049024` bytes，SHA-256 `02ee7f60fccf2392d1895e1cee616d31ba05488faab83e1c76ee07121e6e5681`；清单见 `transfer-manifest.json`。

### 8.3 A组消费与 GHCR 接收验证

| 记录                                      | 结果               | 位置                                                                                                      |
| --------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------- |
| A组本地 DRAFT 环境消费（基于 B1 工具链镜像派生 MD/RD 镜像） | `ACCEPTED_LOCAL` | `evidence/run-20261010T043534Z-md-rd-main-29c02/`（`DRAFT_ENVIRONMENT_VALIDATION.md`、`draft-input.json`） |
| A组按 B1 Dockerfile 独立构建本地验收              | `PASS_LOCAL`     | `evidence/run-20261010T114727Z/`                                                                        |
| A组按 GHCR digest 接收 B1 原始镜像并复测           | **`ACCEPTED`**   | `evidence/run-20261010T160627Z-ghcr/`，回执 `A_CROSS_MACHINE_RECEIPT.md`、机读 `registry-replay.json`         |

- 接收端镜像身份核对全部通过：RepoDigest、Image ID、源码 revision、`linux/amd64` 平台、项目 label 均与 B1 记录一致。
- 接收端功能复测全部通过（断网 `--network none`）：`./app` 输出 `1\n`；MD stale 不重编译、输出 `1`；MD clean rebuild 重编译、输出 `2`；RD 改 `unused.h` 触发 `main.c` 重编译。
- 接收主机：macOS 27 / arm64 + Colima Docker Engine（镜像按 `linux/amd64` 运行）。

### 8.4 DRAFT 输入形状（E3 不调用 API）

| 字段                               | 值                                              |
| -------------------------------- | ---------------------------------------------- |
| `repository.url`                 | `https://github.com/Rowan-hhh/devops_lab1.git` |
| `repository.commit`              | `29c02d6604d7071d4b249ec958dd8a553caa670a`     |
| `repository.project_root`        | `A-BuildChecker-E3测试基线/fixtures/md-rd`         |
| `build_command` / `test_command` | `make` / `./app`                               |
| 预期                               | build/test 退出码 `0`，stdout 精确为 `1\n`            |

---

## 9. 双方交换与确认（文档级往返；实际重跑移交 E4）

按 E3 分工图，⑤ 需与 **B4 重跑与交付负责人** 交换结果。但"**交换仓库、按 README 实际重跑一遍并对照**"是 **E4 的相互检查**（E4 PPT E4/20：相邻两组交换仓库地址，只看 README 尝试重跑；E4/18 第六步、E4/19 重跑对照）。两者边界：

| 归属                | 动作          | 说明                                      |
| ----------------- | ----------- | --------------------------------------- |
| **A组 / E3 ⑤（本轮）** | **文档级往返确认** | A组交出本整理包，B4 确认"能按 README 重跑"，**无需现在真跑** |
| **E4（后续）**        | **实际重跑对照**  | 相邻两组交换仓库，按 README 实际重跑并对比结果             |

请 B4 做**文档级**回执（不必实际重跑）：

| 项           | 请确认                                     |
| ----------- | --------------------------------------- |
| README 可重跑性 | §2 的命令 + 环境要求，是否足以让你按 README 重跑（无需现在真跑） |
| SHA 一致      | C0/C1/C2 与 MD/RD 的 SHA 是否与你方一致（§3）      |
| 预期 vs 实际    | §4 对照是否可解释                              |
| 失败定位        | §6 两条失败记录是否可定位到版本                       |
| 环境（可选）      | §8 的 GHCR image_ref 与接收结论是否知悉           |

> 实际"交换仓库、按 README 重跑并对照结果"留待 **E4 相互检查**，不在 E3 内完成。

### 9.1 文档级往返确认结果（已回执）

| 项   | 内容                                                                                                    |
| --- | ----------------------------------------------------------------------------------------------------- |
| 参与方 | A组交付负责人（⑤） ↔ B4 重跑与交付负责人                                                                             |
| 方式  | 文档级往返确认（本整理包 ↔ B4 回执），**未实际重跑**                                                                       |
| 日期  | 2026-10-11                                                                                            |
| 结论  | **确认通过**：B4 认可本整理包（README 重跑步骤、C0/C1/C2 与 MD/RD 的 SHA、预期 vs 实际对照、检测报告、环境信息、失败定位）足以按 README 重跑；实际「交换仓库 + 按 README 重跑对照」移交 **E4 相互检查** |

④ 的三方确认（接受 Patch）已完成，见 `E3-A组④检测复核记录.md` §8。

---

## 10. 整理发现与待办

- [x] **（已完成）** 补齐 §8 环境信息（B1 环境包 `fa07b719` + A组 GHCR 接收 `c1a74156`，`ACCEPTED`）。
- [x] **（已关闭）** "最新有效运行"口径：上游 `FINAL_RESULT.md` 已明确 canonical = `run-20261010T051714Z`。
- [x] **（已完成）** 收齐 §9 **文档级**往返确认——**B4 已回执确认通过**（未实际重跑）。
- [ ] **（移交 E4）** "交换仓库 + 按 README 实际重跑 + 结果对照"由 **E4 相互检查**完成。
- [ ] **（提示）** 若 B2 改用 canonical-main 报告（`29c02d66…`），需以新 commit 为 base 重新校验候选 Patch 与 B4 记录（旧交接沿用 `39430e3…`，本次未覆盖）。

---

## 附：后续任务（PPT 第10页）

| 任务  | 主题                   |
| --- | -------------------- |
| E4  | 环境和密钥管理              |
| E5  | BuildChecker / DRAFT |
| E8  | EChecker / MDFixer   |
| E12 | 接入真实数据联调             |
