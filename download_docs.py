#!/usr/bin/env python3
"""
Git Sparse Checkout 脚本 V4
优化版本：统一docs目录结构 + 断点续传 + 智能更新检测
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple, List

class DownloadStatus:
    """下载状态管理器"""

    def __init__(self, status_file: Path):
        self.status_file = status_file
        self.status = self.load_status()

    def load_status(self) -> Dict:
        """加载状态文件"""
        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 状态文件损坏，重新创建: {e}")
        return {"repositories": {}, "last_updated": None}

    def save_status(self):
        """保存状态文件"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(self.status, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"错误: 无法保存状态文件: {e}")

    def get_repo_status(self, repo_name: str) -> Dict:
        """获取仓库状态"""
        return self.status["repositories"].get(repo_name, {})

    def update_repo_status(self, repo_name: str, status_info: Dict):
        """更新仓库状态"""
        if "repositories" not in self.status:
            self.status["repositories"] = {}
        self.status["repositories"][repo_name] = status_info
        self.status["last_updated"] = datetime.now().isoformat()
        self.save_status()

    def mark_repo_failed(self, repo_name: str, error_msg: str):
        """标记仓库失败状态"""
        current_status = self.get_repo_status(repo_name)
        current_status.update({
            "status": "failed",
            "last_error": error_msg,
            "last_attempt": datetime.now().isoformat()
        })
        self.update_repo_status(repo_name, current_status)

def run_command(cmd: List[str], cwd: Optional[Path] = None, capture_output: bool = False) -> Tuple[bool, str]:
    """执行命令并处理输出"""
    try:
        print(f"执行: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture_output,
            text=True
        )

        if capture_output:
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()

        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else f"命令失败，返回码: {result.returncode}"
            return False, error_msg

        return True, ""

    except Exception as e:
        error_msg = f"执行异常: {e}"
        return False, error_msg

def parse_github_url(url: str) -> Tuple[str, str, str, str]:
    """解析GitHub URL，返回 (基础URL, 分支, 目录路径, 最终目录名)"""
    url = url.rstrip('/')

    if "/tree/" in url:
        base_url, path_part = url.split("/tree/", 1)
        if "/" in path_part:
            branch, dir_path = path_part.split("/", 1)
        else:
            branch = path_part
            dir_path = ""
    else:
        base_url = url
        branch = "main"
        dir_path = ""

    # 提取最终目录名
    if dir_path:
        final_dir_name = dir_path.split('/')[-1]  # 取最后一部分作为目录名
    else:
        final_dir_name = "docs"  # 默认目录名

    return base_url, branch, dir_path, final_dir_name

def get_remote_latest_commit(repo_url: str, branch: str = "main") -> Optional[str]:
    """获取远程仓库最新提交哈希"""
    try:
        success, stdout, stderr = run_command(
            ["git", "ls-remote", repo_url, branch],
            capture_output=True
        )

        if success and stdout:
            # git ls-remote 输出格式: <commit-hash>\trefs/heads/main
            commit_hash = stdout.split('\t')[0]
            return commit_hash
        else:
            print(f"  获取远程提交失败: {stderr}")
            return None
    except Exception as e:
        print(f"  获取远程提交异常: {e}")
        return None

def check_local_repo_status(repo_dir: Path) -> Dict:
    """检查本地仓库状态"""
    status = {
        "exists": repo_dir.exists(),
        "is_git_repo": False,
        "current_commit": None,
        "file_count": 0,
        "last_modified": None
    }

    if not status["exists"]:
        return status

    try:
        # 检查是否是git仓库
        git_dir = repo_dir / ".git"
        status["is_git_repo"] = git_dir.exists()

        if status["is_git_repo"]:
            # 获取当前提交
            success, stdout, stderr = run_command(
                ["git", "rev-parse", "HEAD"],
                cwd=repo_dir,
                capture_output=True
            )
            if success:
                status["current_commit"] = stdout

            # 统计文件数量
            success, stdout, stderr = run_command(
                ["git", "ls-files"],
                cwd=repo_dir,
                capture_output=True
            )
            if success:
                status["file_count"] = len(stdout.split('\n')) if stdout else 0

        # 获取最后修改时间
        if repo_dir.exists():
            status["last_modified"] = datetime.fromtimestamp(
                repo_dir.stat().st_mtime
            ).isoformat()

    except Exception as e:
        print(f"  检查本地状态异常: {e}")

    return status

def main():
    parser = argparse.ArgumentParser(description="Git Sparse Checkout 优化版本")
    parser.add_argument("--force", action="store_true", help="强制重新下载所有仓库")
    parser.add_argument("--check", action="store_true", help="仅检查状态，不执行下载")
    parser.add_argument("--repo", help="仅处理指定仓库")
    args = parser.parse_args()

    # 基础目录设置
    base_dir = Path.home() / "dev/dev_docs"
    base_dir.mkdir(parents=True, exist_ok=True)

    # 统一的docs目录
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    # 状态管理
    status_manager = DownloadStatus(base_dir / "download_status.json")

    os.chdir(base_dir)
    print(f"工作目录: {base_dir}")
    print(f"文档目录: {docs_dir}")

    # 仓库配置
    repos = [
        {
            "name": "dspy",
            "url": "https://github.com/stanfordnlp/dspy/tree/main/docs/docs",
            "description": "DSPy 框架文档"
        },
        {
            "name": "ten-framework",
            "url": "https://github.com/TEN-framework/portal/tree/main/content/docs",
            "description": "TEN 框架文档"
        },
        {
            "name": "langchain",
            "url": "https://github.com/langchain-ai/docs/tree/main/src/oss/langchain",
            "description": "LangChain 文档"
        },
        {
            "name": "langgraph",
            "url": "https://github.com/langchain-ai/docs/tree/main/src/oss/langgraph",
            "description": "LangGraph 文档"
        },
        {
            "name": "langsmith",
            "url": "https://github.com/langchain-ai/docs/tree/main/src/langsmith",
            "description": "LangSmith 文档"
        },
        {
            "name": "copilotkit",
            "url": "https://github.com/CopilotKit/CopilotKit/tree/main/docs/content/docs",
            "description": "CopilotKit 文档"
        }
    ]

    # 过滤指定仓库
    if args.repo:
        repos = [repo for repo in repos if repo["name"] == args.repo]
        if not repos:
            print(f"错误: 未找到仓库 '{args.repo}'")
            return False

    results = {"success": 0, "failed": 0, "skipped": 0, "errors": []}

    for i, repo in enumerate(repos, 1):
        name = repo["name"]
        url = repo["url"]
        description = repo["description"]

        print(f"\n[{i}/{len(repos)}] 处理: {name}")
        print(f"  URL: {url}")
        print(f"  说明: {description}")

        base_url, branch, dir_path, final_dir_name = parse_github_url(url)
        repo_dir = docs_dir / name  # 使用配置文件中的name作为本地目录名

        print(f"  仓库: {base_url}")
        print(f"  分支: {branch}")
        print(f"  远程路径: {dir_path}")
        print(f"  最终目录: {final_dir_name}")
        print(f"  本地目录: {name}")
        print(f"  本地路径: {repo_dir}")

        # 获取仓库状态
        local_status = check_local_repo_status(repo_dir)
        repo_status = status_manager.get_repo_status(name)

        print(f"  本地状态: 存在={local_status['exists']}, Git仓库={local_status['is_git_repo']}")
        if local_status['current_commit']:
            print(f"  当前提交: {local_status['current_commit'][:8]}")

        # 获取远程最新提交
        remote_commit = get_remote_latest_commit(base_url, branch)
        if remote_commit:
            print(f"  远程提交: {remote_commit[:8]}")
        else:
            print(f"  ⚠ 无法获取远程提交信息")

        # 判断是否需要更新
        needs_update = False
        update_reason = ""

        if args.force:
            needs_update = True
            update_reason = "强制更新"
        elif not local_status["exists"]:
            needs_update = True
            update_reason = "首次下载"
        elif not local_status["is_git_repo"]:
            needs_update = True
            update_reason = "非Git仓库，重新下载"
        elif remote_commit and remote_commit != local_status["current_commit"]:
            needs_update = True
            update_reason = f"有更新 ({local_status['current_commit'][:8]} -> {remote_commit[:8]})"
        else:
            print(f"  ✓ 已是最新，跳过")
            results["skipped"] += 1
            continue

        if args.check:
            print(f"  需要更新: {update_reason}")
            continue

        print(f"  需要更新: {update_reason}")

        try:
            # 如果存在且不是git仓库，删除重建
            if local_status["exists"] and not local_status["is_git_repo"]:
                print(f"  删除非git目录...")
                import shutil
                shutil.rmtree(repo_dir)

            if local_status["exists"] and local_status["is_git_repo"]:
                # 更新现有仓库
                print(f"  拉取最新内容...")
                success, error = run_command(["git", "pull", "origin", branch], cwd=repo_dir)
                if not success:
                    raise Exception(f"拉取失败: {error}")
            else:
                # 创建临时目录用于sparse-checkout
                temp_dir = docs_dir / f"temp_{name}_{int(datetime.now().timestamp())}"
                print(f"  创建临时目录: {temp_dir}")

                # 克隆到临时目录
                print(f"  克隆仓库并启用sparse-checkout...")
                success, error = run_command([
                    "git", "clone",
                    "--depth", "1",
                    "--filter=blob:none",
                    "--sparse",
                    base_url,
                    str(temp_dir)
                ])
                if not success:
                    raise Exception(f"克隆失败: {error}")

                # 设置sparse-checkout目录
                if dir_path:
                    print(f"  设置sparse-checkout目录: {dir_path}")
                    success, error = run_command([
                        "git", "sparse-checkout", "set", dir_path
                    ], cwd=temp_dir)
                    if not success:
                        raise Exception(f"sparse-checkout设置失败: {error}")

                    # 移动最终目录到目标位置
                    source_dir = temp_dir / dir_path
                    print(f"  移动目录: {source_dir} -> {repo_dir}")

                    if source_dir.exists():
                        import shutil
                        shutil.move(str(source_dir), str(repo_dir))
                        print(f"  ✓ 目录移动完成")
                    else:
                        raise Exception(f"源目录不存在: {source_dir}")

                # 清理临时目录
                print(f"  清理临时目录...")
                import shutil
                shutil.rmtree(temp_dir)

            # 验证下载结果 - 检查最终目录是否在docs目录下
            if dir_path:
                final_dir = repo_dir
                if final_dir.exists():
                    file_count = len(list(final_dir.rglob("*")))
                    print(f"  ✓ 成功！本地目录 '{name}' (源目录: {final_dir_name}) 包含 {file_count} 个文件/目录")

                    # 更新状态
                    new_status = {
                        "status": "success",
                        "last_commit": remote_commit,
                        "file_count": file_count,
                        "last_updated": datetime.now().isoformat(),
                        "update_reason": update_reason,
                        "local_dir": name,
                        "source_dir": final_dir_name
                    }
                    status_manager.update_repo_status(name, new_status)
                    results["success"] += 1
                else:
                    raise Exception(f"目标目录不存在: {final_dir}")
            else:
                print(f"  ✓ 成功！")
                results["success"] += 1

        except Exception as e:
            print(f"  ✗ 失败: {e}")
            results["failed"] += 1
            results["errors"].append(f"{name}: {str(e)}")
            status_manager.mark_repo_failed(name, str(e))

    # 输出结果
    print(f"\n{'='*50}")
    print(f"处理完成:")
    print(f"  成功: {results['success']}")
    print(f"  跳过: {results['skipped']}")
    print(f"  失败: {results['failed']}")

    if results["errors"]:
        print(f"\n错误详情:")
        for error in results["errors"]:
            print(f"  - {error}")

    return results["failed"] == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)