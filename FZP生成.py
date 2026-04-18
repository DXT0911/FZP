import math
from weasyprint import HTML

def generate_black_fzp_pdf(output_filename="fzp_template_black.pdf"):
    # 物理参数
    wavelength = 632.8e-6  # mm (632.8 nm)
    rings_list = [20, 40, 60, 80, 100]
    focal_lengths = [400, 600, 800]
    types = ['positive', 'negative']

    # 生成 30 个组合
    combinations = []
    for r in rings_list:
        for f in focal_lengths:
            for t in types:
                combinations.append({'n_max': r, 'f': f, 'type': t})

    def create_svg_fzp(params):
        n_max = params['n_max']
        f = params['f']
        is_pos = (params['type'] == 'positive')
        
        svg_elements = []
        # 从大到小绘制，叠层法
        for n in range(n_max, 0, -1):
            radius = math.sqrt(n * wavelength * f + (n * wavelength / 2)**2)
            
            # 正片 (+): n=1是白, n=2是黑... => 奇数白，偶数黑
            # 负片 (-): n=1是黑, n=2是白... => 奇数黑，偶数白
            if is_pos:
                color = "white" if n % 2 != 0 else "black"
            else:
                color = "black" if n % 2 != 0 else "white"
            
            svg_elements.append(f'<circle cx="20" cy="20" r="{radius}" fill="{color}" />')
            
        label = f"N{n_max} f{f} {'+' if is_pos else '-'}"
        
        return f"""
        <div class="cell">
            <svg viewBox="0 0 40 40" width="40mm" height="40mm">
                <rect x="0" y="0" width="40" height="40" fill="black" />
                {svg_content if 'svg_content' in locals() else "".join(svg_elements)}
            </svg>
            <div class="label">{label}</div>
        </div>
        """

    # 重构逻辑以匹配上面的 div
    html_cells = ""
    for p in combinations:
        html_cells += create_svg_fzp(p)

    html_content = f"""
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 15mm 5mm;
                background-color: black;
            }}
            body {{
                margin: 0;
                padding: 0;
                background-color: black;
                display: block;
            }}
            .grid {{
                width: 200mm;
                display: block;
                font-size: 0;
            }}
            .cell {{
                width: 40mm;
                height: 40mm;
                display: inline-block;
                position: relative;
                box-sizing: border-box;
                border: 0.1pt solid #333333; /* 暗灰色裁剪线 */
                vertical-align: top;
                background-color: black;
            }}
            .label {{
                position: absolute;
                bottom: 1.5mm;
                left: 0;
                width: 100%;
                text-align: center;
                font-size: 5pt;
                font-family: sans-serif;
                color: white; /* 白色文字 */
            }}
            svg {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <div class="grid">
            {html_cells}
        </div>
    </body>
    </html>
    """
    
    HTML(string=html_content).write_pdf(output_filename)
    return output_filename

generate_black_fzp_pdf()