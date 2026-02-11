# 创建langchain_ecosystem技能
使用 skill-creator 技能(不是MCP skill-seeker)，帮我创建以下技能：
name: langchain_ecosystem
description: LangChain、LangGraph、LangSmith的全面技术文档和API参考

## 工作目录
构建技能来源的文档目录：
docs/langchain
docs/langgraph
docs/langsmith

文档转换脚本：utils/mdx_to_md_converter.py

工作目录：tmp/
输出技能到目录：skills/langchain_ecosystem/

构建完成后，不需要打包 .zip 文件



# 从使用者的角度，优化langchain_ecosystem技能
使用 skill-creator 技能(不是MCP skill-seeker)，帮我继续完善目前已经创建好的：skills/output/langchain_ecosystem
但是以使用者的角度，在使用过程中，来调整技能的索引和描述。
使用者角度示例：
- LangChain、LangChain是如何配置供应商和模型的，最佳实践中配置的格式是怎样的？
- LangChain 都提供了哪些基础组件和工具、模块，让我在构建LangGraph multi-agent时，不必重复构建这些基础设施。
- 构建LangGraph的 State、Node 和 Edge，最佳实践是怎样的？共享哪些基础组件？多个智能体之间如何赋予角色、权限，如何互相传递消息？
- LangGraph中构建多个智能体的最佳实践
- LangGraph的打断、恢复、重试、超时、重试次数机制，最佳实践是怎样的？
- LangGraph的工具调用，传递消息的最佳实践是怎样的？
- LangSmith具体应该设置监控哪些指标？