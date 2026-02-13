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
import yaml
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
    """检查本地目录状态"""
    status = {
        "exists": repo_dir.exists()
    }
    return status

def main():
    script_dir = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(description="Git Sparse Checkout 优化版本")
    parser.add_argument("--force", action="store_true", help="强制重新下载所有仓库")
    parser.add_argument("--check", action="store_true", help="仅检查状态，不执行下载")
    parser.add_argument("--repo", help="仅处理指定仓库")
    parser.add_argument(
        "--base-dir",
        default=str(script_dir),
        help="基础目录（默认: 脚本所在目录）"
    )
    args = parser.parse_args()

    # 基础目录设置
    base_dir = Path(args.base_dir).expanduser().resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    # 统一的docs目录
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)

    # 状态管理
    status_manager = DownloadStatus(base_dir / "download_status.json")

    os.chdir(base_dir)
    print(f"工作目录: {base_dir}")
    print(f"文档目录: {docs_dir}")

    # 从 clone_list.yml 读取仓库配置
    clone_list_file = base_dir / "clone_list.yml"
    if not clone_list_file.exists():
        print(f"错误: 配置文件不存在: {clone_list_file}")
        return False

    try:
        with open(clone_list_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            repos = config.get("repositories", [])
    except Exception as e:
        print(f"错误: 无法读取配置文件: {e}")
        return False

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

        print(f"  本地状态: 存在={local_status['exists']}")
        last_commit = repo_status.get("last_commit")
        if last_commit:
            print(f"  上次提交: {last_commit[:8]}")

        # 获取远程最新提交
        remote_commit = get_remote_latest_commit(base_url, branch)
        if remote_commit:
            print(f"  远程提交: {remote_commit[:8]}")
        else:
            print(f"  ⚠ 无法获取远程提交信息")

        # 判断是否需要更新
        if args.force:
            update_reason = "强制更新"
        elif not local_status["exists"]:
            update_reason = "首次下载"
        else:
            # 从状态文件获取上次记录的commit，与远程commit比较
            last_commit = repo_status.get("last_commit")
            if remote_commit and remote_commit != last_commit:
                if last_commit:
                    update_reason = f"有更新 ({last_commit[:8]} -> {remote_commit[:8]})"
                else:
                    update_reason = "首次下载"
            else:
                print(f"  ✓ 已是最新，跳过")
                results["skipped"] += 1
                continue

        if args.check:
            print(f"  需要更新: {update_reason}")
            continue

        print(f"  需要更新: {update_reason}")

        try:
            # 删除旧目录（sparse-checkout 移动的目录没有 git 信息，无法增量更新）
            if local_status["exists"]:
                print(f"  删除旧目录...")
                import shutil
                shutil.rmtree(repo_dir)

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
