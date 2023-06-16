# CKG_demo

本仓库为基于（代码）知识图谱的Python API误用检测场景下文本-代码一致性检测算法的初步实现Demo。其输入为某一项目提交（包括提交文本+原始代码+修改后代码），输出为一致性得分。该算法核心在于通过对格式自由的提交文本进行DSL关键词识别，提取API误用及变更知识点，与CKG进行相似度检测。注意：由于该方法依赖专家知识，局限性较高，因此通用的一致性匹配方法在HatPAM中进行了扩展：https://github.com/MirageLyu/HatPAM

## 核心文件说明


### 1.代码变更表示

try_sc2.py: 使用Gumtreediff工具，获取语法层细粒度代码变更

codeChange.py: 针对代码变更构建CKG

### 2.文本表示

redundant_dict.txt: 约束规则设计文件，自定义NER识别

compute_ck_score.py: 计算局部实体相似度，目前只使用到了文本相似度，可按需进行扩展

### 3.代码表示

此外，我们基于已有工作，在Python上进行了简单复现，可以针对单个代码文件（非变更）构建API调用相关CKG：


KG.py: 定义CKG类别。 具体如下：

There are five kinds of code entity types: class, property, method, parameter and variable; and five relation types in code knowledge graph: "inheritance"(between class and class), "has"(between class and property, class and method, method and parameter, method and variable), "instance_of" (between property and class, variable and class), "return_type" (between method and class) and "call" (between method and method).

ASTParser.py: 调用入口

ASTVisitor.py: 在AST遍历功能上重构+增加CKG知识提取逻辑

### 4.其他文件

其他文件，如extract_\*.py为一些中间数据的提取、预处理等。

