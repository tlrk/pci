# 决策树建模
## 引入决策树
* 现有的情况，对应的数据并且每个数据有对应的结果，这些数据都是已经发生了的，我们需要利用这些数据对未来的某些数据做出预测，得出最终的结果
* 决策树可以直观地以图形的形式来表示最终数据的结果所经历的选择过程，以此事实我们可以做出参考和推断
* 对于一行数据有多个列，其实就是对应用户的每一个选择，是影响最终结果的一种因素，这些因素的选取是在开始的时候认为选择的，有一定的主观性，选择特征（影响因素）也是非常重要的经验
* col值对应于一行数据汇中某一列的序号，表示的意思是这列所代表的事件的判断条件
* value是为了使结果为true，必须匹配的值
* results保存的是针对于当前分支的结果，他是一个字典，除了叶子节点外，在其他节点上该值都为None

## 对树进行训练
* CART（classification and regression trees），即是分类回归树，构建决策树
* 需要一个函数，实现根据某一个变量因素，对数据集进行划分成两个集合，其中一个是满足了该变量提供的条件，另外一个集合不满足该条件
* 现在的问题是应该选择哪个因素来拆分
* 拆分得到的结果是两个集合，我们关注的是这两个集合中，对应最终的结果是否具有一致性，比如最终的结果都是付费用户，那么说明这次划分是一次非常好的划分

## 选择最合适的拆分方案
* 目标是选择一个合适的变量，使两个数据集合在混杂程度上尽可能的小，也就是对于我们所关注的结果，在两个数据集合中，尽可能的保持一致
* uniquecount函数，对集合中所有的结果进行技术，得到一个字典，用于后面的统计
* 有两种方法计算：基尼不纯度和熵

## 基尼不纯度
> 基尼不纯度指标[编辑]
在CART算法中, 基尼不纯度表示一个随机选中的样本在子集中被分错的可能性。基尼不纯度为这个样本被选中的概率乘以它被分错的概率。当一个节点中所有样本都是一个类时，基尼不纯度为零。
假设y的可能取值为{1, 2, ..., m},令fi是样本被赋予i的概率，则基尼指数可以通过如下计算：

![基尼不纯度计算公式](../image/snapSave/giniimpurity.png)


* 将来自集合中的某种结果随机应用于集合中某一数据项的预期误差率

```
# 随机放置的数据项出现于错误分类中的概率
def giniimpurity(rows):
	total = len(rows)
	counts = uniquecounts(rows)
	imp = 0
	for k1 in counts:
		p1 = float(counts[k1]) / total
		for k2 in counts:
			if (k1 == k2): continue
			p2 = float(counts[k2]) / total
			imp += p1 * p2
	return imp
```
* <mark>该函数利用集合中的每一项元素出现结果的次数，除以集合的总行数来计算对应的概率，然后将所有这些概率的值累加起来，得到某行数据被随机分配到错误结果的总概率</mark>
* 算法解释，第一层循环为某一项被选中的概率，下一个循环表示的是它被选错的概率
* 到底层循环结束的时候，我们是得到选中k1时，对应被选错的概率，现在要得到随机的一个被选错的概率，应该选中集合中其他的项，同样这样来计算，总共的和就是某一行数据被随机分配到错误结果的概率

## 熵
> 通常，一个信源发送出什么符号是不确定的，衡量它可以根据其出现的概率来度量。概率大，出现机会多，不确定性小；反之就大。
不确定性函数f是概率P的单调递降函数；两个独立符号所产生的不确定性应等于各自不确定性之和，即f（P1，P2）=f（P1）+f（P2），这称为可加性。同时满足这两个条件的函数f是对数函数，即  。
在信源中，考虑的不是某一单个符号发生的不确定性，而是要考虑这个信源所有可能发生情况的平均不确定性。若信源符号有n种取值：U1…Ui…Un，对应概率为：P1…Pi…Pn，且各种符号的出现彼此独立。这时，信源的平均不确定性应当为单个符号不确定性-logPi的统计平均值（E），可称为信息熵，即  ，式中对数一般取2为底，单位为比特。但是，也可以取其它对数底，采用其它相应的单位，它们间可用换底公式换算。
最简单的单符号信源仅取0和1两个元素，即二元信源，其概率为P和Q=1-P，该信源的熵即为如图1所示。
由图可见，离散信源的信息熵具有：①非负性，即收到一个信源符号所获得的信息量应为正值，H（U）≥0；②对称性，即对称于P=0．5（③确定性，H（1，0）=0，即P=0或P=1已是确定状态，所得信息量为零；④极值性，当P=0．5时，H（U）最大；而且H（U）是P的上凸函数。
对连续信源，仙农给出了形式上类似于离散信源的连续熵，
图1   二元信源的熵
图1 二元信源的熵
虽然连续熵HC（U）仍具有可加性，但不具有信息的非负性，已不同于离散信源。HC（U）不代表连续信源的信息量。连续信源取值无限，信息量是无限大，而HC（U）是一个有限的相对值，又称相对熵。但是，在取两熵的差值为互信息时，它仍具有非负性。这与力学中势能的定义相仿

![熵的函数图](../image/snapSave/entropy.png)

```
# 熵是遍历所有可能结果之后所得到的p(x)*log(p(x))之和
def entropy(rows):

	from math import log
	log2=lambda x:log(x)/log(2)
	results = uniquecounts(rows)

	# 此处开始计算熵值
	ent = 0.0
	for r in results.keys():
		p = float(results[r]) / len(rows)
		ent = ent - p * log2(p)
	return ent
```

## 决策树的减枝





