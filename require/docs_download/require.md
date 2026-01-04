帮我创建一个git目录 下载及更新 脚本。
使用 git sparse-checkout 更新我列出的仓库目录地址。
只需要指定的目录，不要拷贝整个仓库，不要含git历史记录。

只需要指定的目录：
例如，我要下载 https://github.com/langchain-ai/docs/tree/main/src/oss/langchain
那么，只需要将最终的 langchain 目录下载到 docs 目录下，上级的 docs/tree/main/src/oss/ 等目录不要。

需要更新的地址列表在 clone_list.yml。

--depth 1：确保只拉取最新的 commit，不含历史记录。
--no-checkout：克隆仓库结构，但先不检出任何文件。

今后每次运行该脚本，会自动下载我新加的地址对应的目录文件，更新已存在的目录文件。


备注：
在运行下载脚本前，可使用 proxy on 命令开启代理加速下载。
当前是在wsl中，可使用 export http_proxy="http://10.255.255.254:1087" && export https_proxy="http://10.255.255.254:1087" && echo "代理已开启: $http_proxy" 开启代理。