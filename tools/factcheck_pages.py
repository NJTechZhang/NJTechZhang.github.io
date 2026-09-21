"""事实核查：把论文导读页中的数值与对应论文 PDF 全文比对，标记查无实据的数字。

用法：
    python tools/factcheck_pages.py

说明：
    - 会做全角数字、千分位逗号、空白归一化，因此 61,070.24 与 61070.24 视为相同
    - 页面中的数字若由公式计算得出（如 3n²=243）或经四舍五入，可能被判为「待核」，
      这类情况需人工确认（原文通常有对应的公式或更高精度数值）
    - 输出「待核」不代表错误，而是提示需要人工核对上下文
"""
import os
import re

import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "论文原文")
PAGES = os.path.join(ROOT, "papers")

# 导读页 -> 论文原文 PDF（新增论文时在此登记）
MAP = {
    "3dcity-net.html": "复杂城市动态图卷积网络三维场景语义分割法_张荣庭.pdf",
    "autonomous-learning-interactive-hyperspectral.html": "Autonomous_learning_interactive_features_hyperspectral_AppliedSciences2021.pdf",
    "background-suppression-diffusion-htd.html": "Background Suppression by Multivariate Gaussian Denoising Diffusion Model for Hyperspectral Target Detection.pdf",
    "context-enhanced-scale-contrastive.html": "Context-Enhanced_and_Scale-Contrastive_Learning_for_Remote_Sensing_Imagery_Understanding.pdf",
    "generalized-buffering-algorithm.html": "Generalized_Buffering_Algorithm.pdf",
    "geoinformatics-ai2-integration.html": "测绘地理信息与人工智能2.0融合发展的方向_张广运.pdf",
    "grid-graph-point-cloud-registration.html": "Grid graph-based large-scale point clouds registration.pdf",
    "local-global-fused-feature-mesh-segmentation.html": "Optimizing_LocalGlobal_Fused_Feature_Space_With_Category-Center-Aware_Supervised_Contrastive_Learning_for_Urban_3-D_Mesh_Segmentation.pdf",
    "manifold-learning-co-location-decision-tree.html": "Manifold Learning Co-Location Decision Tree for Remotely Sensed Imagery Classification.pdf",
    "mesh-based-dgcnn.html": "Mesh-Based_DGCNN_Semantic_Segmentation_of_Text.pdf",
    "meshnet-sp.html": "MeshNet-SP_ A Semantic Urban 3D Mesh Segmentat.pdf",
    "mfsm-net.html": "MFSM-Net_Multimodal Feature Extraction for Semantic Segmentation of Urban-Scale Textured 3D Meshes.pdf",
    "on-board-ortho-rectification-fpga.html": "On-Board Ortho-Rectification for Images Based on An FPGA.pdf",
    "remote-sensing-course-teaching-ai.html": "新一代AI下的遥感专业课程教学方式变革探索_张广运.pdf",
    "rpc-orthorectification-fpga.html": "sensors-18-02511.pdf",
    "scrm-net.html": "SCRM-Net_Self-Supervised Deep Clustering Feature Representation for Urban 3D Mesh Semantic Segmentation.pdf",
    "spatial-consistency-point-cloud-registration.html": "基于空间一致性的同平台点云配准方法_张广运.pdf",
    "spectral-transformer-aod.html": "Spectral transformer with physics-informed regularization fof high-resolution Landsat-8 AOD retrieval.pdf",
    "supernerf.html": "Published-SuperNeRF_High-Precision_3-D_Reconst.pdf",
    "urban-mesh-interpretation-survey.html": "复杂城市场景三维网格模型智能解译技术综述.pdf",
    # radanet / mdanet 无全文 PDF，其导读依据公开摘要，不参与核查
}

NUM = re.compile(r"(?<![A-Za-z0-9.])(\d+(?:\.\d+)?\s*%|\d+\.\d+|\d{3,6})(?![A-Za-z0-9])")
_cache = {}


def norm(s):
    s = s.translate(str.maketrans("０１２３４５６７８９．", "0123456789."))
    return re.sub(r"[\s\u00a0,，]", "", s)


def pdf_norm(fname):
    if fname not in _cache:
        doc = pymupdf.open(os.path.join(SRC, fname))
        t = "\n".join(doc[i].get_text() for i in range(doc.page_count))
        doc.close()
        _cache[fname] = norm(t)
    return _cache[fname]


def pdf_floats(src):
    """枚举原文中所有可能的浮点候选值。

    表格区域的文本抽取常把相邻数值连成一串（如 '1.3684' '83.1978' 被抽成
    '1.368483.1978'），因此需要枚举数字串的所有子串作为候选。
    """
    out = set()
    for m in re.finditer(r"\d[\d.]{1,60}\d", src):
        run = m.group(0)
        for i in range(len(run)):
            if not run[i].isdigit():
                continue
            for j in range(i + 3, min(len(run), i + 14) + 1):
                sub = run[i:j]
                if sub.count(".") == 1 and not sub.endswith("."):
                    try:
                        out.add(float(sub))
                    except ValueError:
                        pass
    return out


def main():
    pending = 0
    for slug, pdf in sorted(MAP.items()):
        page_path = os.path.join(PAGES, slug)
        pdf_path = os.path.join(SRC, pdf)
        if not os.path.exists(page_path):
            print(f"[跳过] {slug}（导读页不存在）")
            continue
        if not os.path.exists(pdf_path):
            print(f"[跳过] {slug}（原文 PDF 不存在）")
            continue

        raw = open(page_path, encoding="utf-8").read()
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
        flat = norm(re.sub(r"<[^>]+>", " ", body))
        src = pdf_norm(pdf)
        src_floats = pdf_floats(src)

        miss = []
        for m in NUM.finditer(flat):
            n = m.group(1)
            core = norm(n).replace("%", "")
            ctx_all = flat[max(0, m.start() - 34):m.end() + 22]
            # 1) 精确匹配
            if core in src or core.rstrip("0").rstrip(".") in src:
                continue
            # 2) 四舍五入匹配：原文更高精度数值按页面位数取整后相等
            if "." in core:
                decimals = len(core.split(".")[1])
                val = float(core)
                if any(round(f, decimals) == val for f in src_floats):
                    continue
            # 3) 期刊引用信息（年, 卷(期): 起页–止页）中的编号，非实验数据，跳过
            win = flat[max(0, m.start() - 40):m.end() + 12]
            if re.search(r"(?:19|20)\d\d\d*\(\d+\)[:：]\d+", win):
                continue
            if re.search(r"20\d\d.{0,4}$", flat[max(0, m.start() - 12):m.start()]):
                continue
            if re.search(r"\)[:：]?$", flat[max(0, m.start() - 6):m.start()]) and len(core) <= 5:
                continue
            miss.append((n, ctx_all))

        pending += len(miss)
        print(f"{'OK ' if not miss else '?? '}{slug:<52} 待核 {len(miss)}")
        for n, ctx in miss:
            print(f"     [{n}] …{ctx}…")

    print(f"\n合计待人工核对：{pending}（原文中经公式计算得出的数值会出现在此处，需人工确认）")


if __name__ == "__main__":
    main()
