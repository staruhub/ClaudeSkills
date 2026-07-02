# Page Brief 模板（Step 5，每页一份）

字段定义与密度规则见 `../references/page-schema.md`。

```jsonc
{
  "page_no": 3,
  "page_type": "problem",
  "title": "客服响应超 4 小时，30% 用户流失在等待中",
  "key_message": "响应速度是当前留存的最大瓶颈",
  "visual_structure": "big-number",
  "content_blocks": [
    {"kind": "number", "content": "4.2h 平均首次响应"},
    {"kind": "bullets", "content": "等待中流失 30%；差评 68% 提及'慢'；人力已到上限"},
    {"kind": "chart", "content": "折线：响应时长 vs 流失率，近 6 个月"}
  ],
  "image_need": "chart",
  "speaker_notes": "先让数字说话，停顿两秒再翻页。强调这不是服务态度问题，是结构问题。"
}
```

自查：key_message 写不出一句话 → 这页不该存在；content_blocks > 5 → 拆页。
