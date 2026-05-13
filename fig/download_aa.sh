#!/bin/bash

cd "/Users/limbo/Project/aa_learn/fig" || exit 1

# 格式：英文名:单字缩写:中文名
# 注意：天冬氨酸和谷氨酸的英文名中包含空格，已替换为 %20 用于 URL
data=(
"alanine:A:丙氨酸"
"arginine:R:精氨酸"
"asparagine:N:天冬酰胺"
"aspartic%20acid:D:天冬氨酸"
"cysteine:C:半胱氨酸"
"glutamine:Q:谷氨酰胺"
"glutamic%20acid:E:谷氨酸"
"glycine:G:甘氨酸"
"histidine:H:组氨酸"
"isoleucine:I:异亮氨酸"
"leucine:L:亮氨酸"
"lysine:K:赖氨酸"
"methionine:M:甲硫氨酸"
"phenylalanine:F:苯丙氨酸"
"proline:P:脯氨酸"
"serine:S:丝氨酸"
"threonine:T:苏氨酸"
"tryptophan:W:色氨酸"
"tyrosine:Y:酪氨酸"
"valine:V:缬氨酸"
)

for item in "${data[@]}"; do
    IFS=':' read -r en_name abbr zh_name <<< "$item"
    url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${en_name}/PNG"
    output="${abbr}.png"
    echo "正在下载 ${zh_name} (${abbr}) ..."
    curl -s -o "$output" "$url"
    if [ $? -eq 0 ] && [ -s "$output" ]; then
        echo "✓ 已保存为 ${output}"
    else
        echo "✗ 下载失败：${zh_name}"
        rm -f "$output"
    fi
    sleep 0.3
done

echo "完成！图片位于：/Users/limbo/Project/aa_learn/fig"
