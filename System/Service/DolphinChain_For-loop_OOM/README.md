### 关于DolphinChain

DolphinChain 是由玄猫安全实验室维护的区块链应用靶机，旨在教授区块链应用程序安全课程。您可以使用 DolphinChain 进行安装和练习。

DolphinChain 基于 tendermint v0.31.2 (WARNING: ALPHA SOFTWARE) 开发，是当时的 tendermint 最新版本。

在这个版本里(v1.0.0)，我们在DolphinChain设置了10多个缺陷。任何白帽子与区块链开发者都可以尝试挖掘漏洞。DolphinChain目的在于帮助安全人员提高技能，同时帮助区块链开发者更好地了解保护区块链应用程序的过程。

### 漏洞简介

恶意的 BlockchainInfo 请求可能会导致无限循环，最终导致内存耗尽导致崩溃。

### 漏洞版本

version < 0.22.6

### 漏洞分析

文件：rpc/core/blocks.go

```
func BlockchainInfo(ctx *rpctypes.Context, minHeight, maxHeight int64) (*ctypes.ResultBlockchainInfo, error) {
if minHeight == 0 {
minHeight = 1
}
if maxHeight == 0 {
maxHeight = blockStore.Height()
} else {
maxHeight = cmn.MinInt64(blockStore.Height(), maxHeight)
}
// maximum 20 block metas
const limit int64 = 20
minHeight = cmn.MaxInt64(minHeight, maxHeight-limit)
logger.Debug("BlockchainInfoHandler", "maxHeight", maxHeight, "minHeight", minHeight)
if minHeight > maxHeight {
return nil, fmt.Errorf("min height %d can't be greater than max height %d", minHeight, maxHeight)
}
blockMetas := []*types.BlockMeta{}
for height := maxHeight; height >= minHeight; height-- { // for-loop
blockMeta := blockStore.LoadBlockMeta(height)
blockMetas = append(blockMetas, blockMeta)
}
return &ctypes.ResultBlockchainInfo{blockStore.Height(), blockMetas}, nil
}
```

注意到maxHeight = cmn.MinInt64(blockStore.Height(), maxHeight)，其中 MinInt64 为从两个参数选择较小的，所以我们使用负值的 maxHeight。

注意循环语句 for height := maxHeight; height >= minHeight; height– {}，代码中的 for-loop 会可以无限次循环执行。当达到循环次数 9223372036854775807 (max int64) ，还能继续进行。每次无法查找块时，它会向 blockMetas 向量追加一个nil。最终，这将增长到足以耗尽服务器上的内存。

### 漏洞修复

增加 filterMinMax 对输入的参数值进行检查处理。