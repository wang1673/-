# 原750任务补充指标与域外试听示例记录

原750音频与三指标不变；补算FAD、KAD及用户授权的论文基线参照ASB/AMB。详细[实验记录](records/EXPERIMENT_RECORD.md)、[精确汇总](records/summary.json)、[独立数值校验](records/independent-validation.json)、[七指标CSV](records/all-metrics.csv)。

FAD=0.779795870：原缓存CLAP特征协议，固定fadtk距离函数；KAD=0.003024635155：原已声明的k=(dot/512+1)^3无偏MMD²约定，作者完整核参数未公开，不能直接比较论文尺度。ASB=0.861230564、AMB=0.930290454是七种发表基线均值的参照近似值，没有补跑基线。原kadtk默认Gaussian核与Polyphonia论文的多项式描述不同，诊断值单列，未混用。

记录保留默认BLAS分解错误及Haswell内核修复、独立torch CUDA float64验证；没有升级软件或修改旧750。原实验剪裁与数据重建限制继续保留。猫叫转狗叫是域外探索示例，不计入750音乐指标；生成结果及失败/重跑记录见机器记录。本目录只上传文本，不上传音频和模型。
