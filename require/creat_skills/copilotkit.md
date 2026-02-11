先探查 docs/copilotkit 目录

使用 skill-creator 技能(不是MCP skill-seeker)，帮我创建以下技能：
name: copilotkit
description: 根据目录下文件总结出技能描述


# 工作目录
构建技能来源的文档目录：docs/copilotkit
做好无关目录文件的排除。需要保留全部教程和示例代码文件供参考。

如果需要，这里有文档转换脚本：utils/mdx_to_md_converter.py

工作目录：tmp/
输出技能到目录：skills/copilotkit/

构建完成后，不需要打包 .zip 文件