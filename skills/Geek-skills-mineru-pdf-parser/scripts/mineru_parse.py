#!/usr/bin/env python3
"""
MinerU PDF Parser Script

将PDF文档解析为Markdown/JSON格式的封装脚本。
支持单文件解析、批量解析、多种输出格式。

用法:
    python mineru_parse.py input.pdf -o output/
    python mineru_parse.py ./pdfs/ -o output/ --batch
    python mineru_parse.py input.pdf -o output/ --backend vlm
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, List
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_mineru_installed() -> bool:
    """检查MinerU是否已安装"""
    try:
        import mineru
        return True
    except ImportError:
        return False


def install_mineru():
    """安装MinerU"""
    logger.info("Installing MinerU...")
    os.system("pip install uv && uv pip install -U 'mineru[all]'")
    logger.info("Downloading models...")
    os.system("mineru-models-download")


def parse_single_pdf(
    input_path: str,
    output_dir: str,
    backend: str = "hybrid",
    lang: Optional[str] = None,
    output_format: str = "all"
) -> dict:
    """
    解析单个PDF文件
    
    Args:
        input_path: PDF文件路径
        output_dir: 输出目录
        backend: 解析后端 (pipeline/vlm/hybrid)
        lang: OCR语言代码
        output_format: 输出格式 (markdown/json/all)
    
    Returns:
        解析结果信息字典
    """
    from mineru import MinerU
    
    logger.info(f"Parsing: {input_path}")
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 初始化MinerU
    mineru = MinerU(backend=backend)
    if lang:
        mineru.lang = lang
    
    # 解析PDF
    try:
        result = mineru.parse(input_path)
        
        # 保存结果
        pdf_name = Path(input_path).stem
        
        if output_format in ("markdown", "all"):
            md_path = Path(output_dir) / f"{pdf_name}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(result.to_markdown())
            logger.info(f"Saved Markdown: {md_path}")
        
        if output_format in ("json", "all"):
            json_path = Path(output_dir) / f"{pdf_name}_content_list.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result.to_json(), f, ensure_ascii=False, indent=2)
            logger.info(f"Saved JSON: {json_path}")
        
        # 保存图像
        images = result.get_images()
        if images:
            img_dir = Path(output_dir) / "images"
            img_dir.mkdir(exist_ok=True)
            for i, img in enumerate(images):
                img_path = img_dir / f"image_{i}.png"
                img.save(img_path)
            logger.info(f"Saved {len(images)} images")
        
        return {
            "status": "success",
            "input": input_path,
            "output_dir": output_dir,
            "pages": len(result.to_json().get("pages", [])),
            "images": len(images) if images else 0
        }
        
    except Exception as e:
        logger.error(f"Error parsing {input_path}: {e}")
        return {
            "status": "error",
            "input": input_path,
            "error": str(e)
        }


def parse_batch(
    input_dir: str,
    output_dir: str,
    backend: str = "hybrid",
    lang: Optional[str] = None,
    output_format: str = "all",
    workers: int = 4
) -> List[dict]:
    """
    批量解析PDF文件
    
    Args:
        input_dir: 包含PDF文件的目录
        output_dir: 输出目录
        backend: 解析后端
        lang: OCR语言代码
        output_format: 输出格式
        workers: 并发数
    
    Returns:
        所有解析结果列表
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    # 获取所有PDF文件
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    logger.info(f"Found {len(pdf_files)} PDF files")
    
    if not pdf_files:
        logger.warning("No PDF files found")
        return []
    
    results = []
    
    def process_one(pdf_path):
        pdf_output = Path(output_dir) / pdf_path.stem
        return parse_single_pdf(
            str(pdf_path),
            str(pdf_output),
            backend=backend,
            lang=lang,
            output_format=output_format
        )
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_one, pdf): pdf for pdf in pdf_files}
        
        for future in as_completed(futures):
            pdf = futures[future]
            try:
                result = future.result()
                results.append(result)
                if result["status"] == "success":
                    logger.info(f"Completed: {pdf.name}")
                else:
                    logger.error(f"Failed: {pdf.name}")
            except Exception as e:
                logger.error(f"Exception processing {pdf.name}: {e}")
                results.append({
                    "status": "error",
                    "input": str(pdf),
                    "error": str(e)
                })
    
    # 统计
    success = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - success
    logger.info(f"Batch complete: {success} success, {failed} failed")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="MinerU PDF Parser - Convert PDF to Markdown/JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.pdf -o output/
  %(prog)s ./pdfs/ -o output/ --batch
  %(prog)s paper.pdf -o output/ --backend vlm
  %(prog)s scanned.pdf -o output/ --lang ch
        """
    )
    
    parser.add_argument(
        "input",
        help="Input PDF file or directory (with --batch)"
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory"
    )
    parser.add_argument(
        "--backend",
        choices=["pipeline", "vlm", "hybrid"],
        default="hybrid",
        help="Parsing backend (default: hybrid)"
    )
    parser.add_argument(
        "--lang",
        help="OCR language code (e.g., ch, en, ja)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "all"],
        default="all",
        help="Output format (default: all)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Batch process all PDFs in directory"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of workers for batch processing (default: 4)"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install MinerU if not present"
    )
    
    args = parser.parse_args()
    
    # 检查安装
    if not check_mineru_installed():
        if args.install:
            install_mineru()
        else:
            logger.error("MinerU not installed. Run with --install or:")
            logger.error("  pip install uv && uv pip install -U 'mineru[all]'")
            sys.exit(1)
    
    # 执行解析
    if args.batch:
        if not Path(args.input).is_dir():
            logger.error("--batch requires a directory as input")
            sys.exit(1)
        results = parse_batch(
            args.input,
            args.output,
            backend=args.backend,
            lang=args.lang,
            output_format=args.format,
            workers=args.workers
        )
    else:
        if not Path(args.input).is_file():
            logger.error(f"Input file not found: {args.input}")
            sys.exit(1)
        result = parse_single_pdf(
            args.input,
            args.output,
            backend=args.backend,
            lang=args.lang,
            output_format=args.format
        )
        results = [result]
    
    # 输出摘要
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    for r in results:
        status = "✓" if r["status"] == "success" else "✗"
        print(f"{status} {r['input']}")
        if r["status"] == "error":
            print(f"  Error: {r['error']}")


if __name__ == "__main__":
    main()
