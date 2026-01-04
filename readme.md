# Git Sparse-Checkout 仓库下载脚本

这个脚本用于从 GitHub 仓库下载指定的目录，使用 `git sparse-checkout` 技术只下载需要的目录内容，而不是整个仓库。

## 功能特性

- ✅ 只下载指定目录，不包含整个仓库
- ✅ 不包含 Git 历史记录 (`--depth 1`)
- ✅ 支持增量更新：新增仓库和更新现有内容
- ✅ 使用 YAML 配置文件管理仓库列表
- ✅ 完善的错误处理和进度显示
- ✅ 支持测试模式（只处理第一个仓库）

## 文件说明

- `update_repos.sh` - 主脚本文件
- `clone_list.yml` - 仓库配置文件
- `README_update_repos.md` - 使用说明文档

## 配置文件格式

`clone_list.yml` 示例：

```yaml
# 仓库配置列表
repositories:
  - name: dspy
    url: https://github.com/stanfordnlp/dspy/tree/main/docs/docs
    description: DSPy 框架文档

  - name: ten-framework
    url: https://github.com/TEN-framework/portal/tree/main/content/docs
    description: TEN 框架文档
```

### 配置字段说明

- `name`: 本地目录名称
- `url`: GitHub 仓库目录的完整 URL（包含 tree/分支/路径）
- `description`: 仓库描述（可选）

## 使用方法

### 1. 基本使用

```bash
# 给脚本执行权限
chmod +x update_repos.sh

# 运行脚本下载/更新所有仓库
./update_repos.sh
```

### 2. 测试模式

如果只想测试第一个仓库，可以修改脚本中的 `TEST_MODE`：

```bash
# 编辑脚本，将 TEST_MODE 设置为 true
# TEST_MODE=true

./update_repos.sh
```

### 3. 添加新仓库

在 `clone_list.yml` 中添加新的仓库配置：

```yaml
  - name: new-repo
    url: https://github.com/user/repo/tree/main/path/to/docs
    description: 新仓库描述
```

## 目录结构

脚本执行后会创建如下目录结构：

```
docs/
├── dspy/           # DSPy 文档
├── ten-framework/  # TEN 框架文档
├── langchain/      # LangChain 文档
├── langgraph/      # LangGraph 文档
└── copilotkit/     # CopilotKit 文档
```

## 技术实现

脚本使用以下 Git 技术：

1. **浅克隆**: `git clone --depth 1` - 只下载最新提交，无历史记录
2. **无检出克隆**: `git clone --no-checkout` - 克隆仓库结构但不检出文件
3. **稀疏检出**: `git sparse-checkout init --cone` + `git sparse-checkout set <path>` - 只检出指定目录

## 环境要求

- Git 2.25+ (支持 sparse-checkout)
- Bash 4.0+
- Python3 (推荐，用于解析 YAML 配置)

## 错误处理

脚本包含完善的错误处理机制：

- 网络连接失败自动重试
- 无效 URL 跳过处理
- 目录权限问题处理
- 临时文件自动清理

## 故障排除

### 1. 网络连接问题

如果遇到 GitHub 连接问题：

```bash
# 检查网络连接
ping github.com

# 或配置代理（如需要）
git config --global http.proxy http://proxy.example.com:8080
```

### 2. YAML 解析错误

如果 Python3 不可用，脚本会使用简单的文本解析作为后备方案，但建议安装 Python3：

```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-yaml

# CentOS/RHEL
sudo yum install python3 python3-pip
pip3 install pyyaml
```

### 3. 权限问题

确保脚本有执行权限：

```bash
chmod +x update_repos.sh
```

## 更新和维护

1. **定期运行**: 建议定期运行脚本以更新仓库内容
2. **清理旧内容**: 如需重新下载，删除 `docs/` 目录后重新运行脚本
3. **配置管理**: 通过修改 `clone_list.yml` 管理要下载的仓库
