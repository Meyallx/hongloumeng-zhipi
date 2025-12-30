#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红楼梦数据验证工具
检查JSONL文件的完整性和一致性
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set

class DataValidator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.errors = []
        self.warnings = []
        
    def validate_all(self):
        """执行所有验证"""
        print("🔍 开始验证数据...\n")
        
        self.validate_sentences()
        self.validate_annotations()
        self.validate_variants()
        self.validate_dictionary()
        
        self.print_report()
        
    def validate_sentences(self):
        """验证句子数据"""
        print("📝 验证句子数据...")
        
        sentence_ids = set()
        
        for version_dir in (self.data_dir / "versions").iterdir():
            if not version_dir.is_dir() or version_dir.name.endswith('.json'):
                continue
                
            for chapter_file in version_dir.glob("*.jsonl"):
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    line_num = 0
                    for line in f:
                        line_num += 1
                        try:
                            data = json.loads(line)
                            
                            # 检查必填字段
                            required = ['id', 'versionId', 'chapterId', 'chapterNumber', 
                                       'sentenceIndex', 'text', 'punctuation']
                            for field in required:
                                if field not in data:
                                    self.errors.append(
                                        f"❌ {chapter_file.name} 第{line_num}行缺少字段: {field}"
                                    )
                            
                            # 检查ID唯一性
                            if data['id'] in sentence_ids:
                                self.errors.append(
                                    f"❌ 重复的句子ID: {data['id']} in {chapter_file.name}"
                                )
                            sentence_ids.add(data['id'])
                            
                        except json.JSONDecodeError:
                            self.errors.append(f"❌ {chapter_file.name} 第{line_num}行JSON格式错误")
        
        print(f"   ✅ 验证了 {len(sentence_ids)} 个句子\n")
        
    def validate_annotations(self):
        """验证批注数据"""
        print("📌 验证批注数据...")
        
        annotation_file = self.data_dir / "annotations" / "zhipan.jsonl"
        if not annotation_file.exists():
            self.warnings.append(f"⚠️  批注文件不存在: {annotation_file}")
            return
            
        count = 0
        with open(annotation_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                    count += 1
                    
                    # 检查必填字段
                    required = ['id', 'type', 'subType', 'source', 'targetVersion', 
                               'targetChapter', 'content']
                    for field in required:
                        if field not in data:
                            self.errors.append(
                                f"❌ 批注文件第{line_num}行缺少字段: {field}"
                            )
                    
                except json.JSONDecodeError:
                    self.errors.append(f"❌ 批注文件第{line_num}行JSON格式错误")
        
        print(f"   ✅ 验证了 {count} 条批注\n")
        
    def validate_variants(self):
        """验证异文数据"""
        print("🔄 验证异文数据...")
        
        variant_file = self.data_dir / "variants" / "variants.jsonl"
        if not variant_file.exists():
            self.warnings.append(f"⚠️  异文文件不存在: {variant_file}")
            return
            
        count = 0
        with open(variant_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line)
                    count += 1
                    
                    # 检查variants数组
                    if 'variants' not in data:
                        self.errors.append(f"❌ 异文文件第{line_num}行缺少variants字段")
                    elif len(data['variants']) < 2:
                        self.warnings.append(f"⚠️  异文文件第{line_num}行variants少于2个版本")
                    
                except json.JSONDecodeError:
                    self.errors.append(f"❌ 异文文件第{line_num}行JSON格式错误")
        
        print(f"   ✅ 验证了 {count} 条异文\n")
        
    def validate_dictionary(self):
        """验证字典数据"""
        print("📚 验证字典数据...")
        
        dict_dir = self.data_dir / "dictionary"
        total = 0
        
        for dict_file in dict_dir.glob("*.jsonl"):
            count = 0
            with open(dict_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        count += 1
                        
                        # 检查必填字段
                        required = ['id', 'term', 'type', 'definition', 'explanation']
                        for field in required:
                            if field not in data:
                                self.errors.append(
                                    f"❌ {dict_file.name} 第{line_num}行缺少字段: {field}"
                                )
                        
                    except json.JSONDecodeError:
                        self.errors.append(f"❌ {dict_file.name} 第{line_num}行JSON格式错误")
            
            print(f"   ✅ {dict_file.name}: {count} 条")
            total += count
        
        print(f"   ✅ 总计 {total} 条字典数据\n")
        
    def print_report(self):
        """打印验证报告"""
        print("\n" + "="*60)
        print("📊 验证报告")
        print("="*60)
        
        if not self.errors and not self.warnings:
            print("✅ 所有数据验证通过！")
        else:
            if self.errors:
                print(f"\n❌ 发现 {len(self.errors)} 个错误：")
                for error in self.errors:
                    print(f"  {error}")
            
            if self.warnings:
                print(f"\n⚠️  发现 {len(self.warnings)} 个警告：")
                for warning in self.warnings:
                    print(f"  {warning}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    validator = DataValidator()
    validator.validate_all()
