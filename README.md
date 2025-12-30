# hongloumeng-zhipi
《红楼梦》异文对照与脂批嵌入
# 红楼梦多版本对照与批注数据库
 
## 项目简介
 
本项目旨在建立一个结构化的《红楼梦》多版本对照和批注数据库，支持：
 
- 📖 **多版本文本对照**：程甲本、脂砚斋本等
- 📝 **脂批整理**：甲戌本、庚辰本、己卯本等脂砚斋批语
- 🔍 **异文标注**：记录不同版本的文字差异
- 📚 **字典注释**：词语解释、典故、文化背景
 
## 数据结构
 
所有数据采用JSONL格式（每行一个JSON对象），便于：
- 版本控制（Git友好）
- 逐行处理
- 增量更新
- 多人协作
 
### 文件说明
data/
├── versions/ # 文本数据（按句存储）
├── annotations/ # 批注数据
├── dictionary/ # 字典数据
└── variants/ # 异文记录


*.txt
Plaintext

详细字段定义请参考：[docs/字段定义.md](docs/字段定义.md)
## 数据示例
当前包含第1回的完整示例数据：
- ✅ 程甲本：20句
- ✅ 脂砚斋本：20句
- ✅ 脂批：10条
- ✅ 异文：12条
- ✅ 词语：15个
- ✅ 典故：8个
- ✅ 文化背景：5个
## 使用方法
### 查看数据
```bash
# 查看第1回第1句（程甲本）
head -n 1 data/versions/version_001/chapter_001.jsonl | jq
# 查看所有脂批
cat data/annotations/zhipan.jsonl | jq
# 查看异文
cat data/variants/variants.jsonl | jq
