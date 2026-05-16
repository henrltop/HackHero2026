from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = r"C:\Users\Rachid\Documents\HACKAHERO\docs\vigilia_analise_legal.pdf"

AZUL_ESCURO = colors.HexColor("#1a3a5c")
AZUL_MEDIO  = colors.HexColor("#2563a8")
AZUL_CLARO  = colors.HexColor("#dbeafe")
CINZA_CLARO = colors.HexColor("#f1f5f9")
VERDE       = colors.HexColor("#166534")
VERDE_BG    = colors.HexColor("#dcfce7")
AMARELO_BG  = colors.HexColor("#fef9c3")
AMARELO     = colors.HexColor("#854d0e")
VERMELHO_BG = colors.HexColor("#fee2e2")
VERMELHO    = colors.HexColor("#991b1b")
BRANCO      = colors.white
PRETO       = colors.HexColor("#1e293b")

PAGE_W, PAGE_H = A4

def build_styles():
    s = getSampleStyleSheet()

    s.add(ParagraphStyle("Capa_Titulo",
        fontName="Helvetica-Bold", fontSize=28, leading=34,
        textColor=BRANCO, alignment=TA_CENTER, spaceAfter=10))

    s.add(ParagraphStyle("Capa_Sub",
        fontName="Helvetica", fontSize=13, leading=18,
        textColor=colors.HexColor("#bfdbfe"), alignment=TA_CENTER, spaceAfter=6))

    s.add(ParagraphStyle("Capa_Info",
        fontName="Helvetica", fontSize=10, leading=14,
        textColor=colors.HexColor("#93c5fd"), alignment=TA_CENTER))

    s.add(ParagraphStyle("Secao",
        fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=AZUL_ESCURO, spaceBefore=18, spaceAfter=8,
        borderPad=0))

    s.add(ParagraphStyle("SubSecao",
        fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=AZUL_MEDIO, spaceBefore=10, spaceAfter=4))

    s.add(ParagraphStyle("Corpo",
        fontName="Helvetica", fontSize=10, leading=15,
        textColor=PRETO, alignment=TA_JUSTIFY, spaceAfter=6))

    s.add(ParagraphStyle("CorpoNegrito",
        fontName="Helvetica-Bold", fontSize=10, leading=15,
        textColor=PRETO, spaceAfter=4))

    s.add(ParagraphStyle("Lei",
        fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
        textColor=AZUL_ESCURO, alignment=TA_JUSTIFY,
        leftIndent=10, rightIndent=10, spaceAfter=4))

    s.add(ParagraphStyle("Nota",
        fontName="Helvetica", fontSize=9, leading=13,
        textColor=colors.HexColor("#374151"), alignment=TA_JUSTIFY,
        leftIndent=10, rightIndent=10, spaceAfter=4))

    s.add(ParagraphStyle("Aviso",
        fontName="Helvetica-Bold", fontSize=9, leading=13,
        textColor=VERMELHO, alignment=TA_JUSTIFY,
        leftIndent=10, rightIndent=10, spaceAfter=4))

    s.add(ParagraphStyle("Checklist",
        fontName="Helvetica", fontSize=10, leading=16,
        textColor=PRETO, leftIndent=15, spaceAfter=2))

    s.add(ParagraphStyle("Rodape",
        fontName="Helvetica", fontSize=8, leading=10,
        textColor=colors.HexColor("#94a3b8"), alignment=TA_CENTER))

    return s

def caixa_lei(texto, styles, bg=AZUL_CLARO, border=AZUL_MEDIO):
    data = [[Paragraph(texto, styles["Lei"])]]
    t = Table(data, colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX",        (0,0), (-1,-1), 1, border),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [bg]),
    ]))
    return t

def caixa_nota(texto, styles, bg=CINZA_CLARO):
    data = [[Paragraph(texto, styles["Nota"])]]
    t = Table(data, colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX",        (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))
    return t

def caixa_aviso(texto, styles):
    data = [[Paragraph(texto, styles["Aviso"])]]
    t = Table(data, colWidths=[14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), VERMELHO_BG),
        ("BOX",        (0,0), (-1,-1), 1, VERMELHO),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))
    return t

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    txt = "Vigilia - Analise Juridica Preliminar  |  Nao substitui parecer juridico especializado  |  2026"
    canvas.drawCentredString(PAGE_W / 2, 1.2*cm, txt)
    canvas.setStrokeColor(colors.HexColor("#e2e8f0"))
    canvas.line(2*cm, 1.6*cm, PAGE_W - 2*cm, 1.6*cm)
    canvas.restoreState()

def capa(styles):
    elems = []

    # Fundo azul simulado via tabela
    titulo_data = [[
        Paragraph("Vigilia", styles["Capa_Titulo"]),
    ]]
    t_titulo = Table(titulo_data, colWidths=[14.5*cm])
    t_titulo.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL_ESCURO),
        ("TOPPADDING",    (0,0), (-1,-1), 40),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ]))
    elems.append(t_titulo)

    sub_data = [[
        Paragraph("Analise Juridica do App de Monitoramento Parental", styles["Capa_Sub"]),
    ]]
    t_sub = Table(sub_data, colWidths=[14.5*cm])
    t_sub.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL_ESCURO),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ]))
    elems.append(t_sub)

    leis_data = [[
        Paragraph("Lei 15.211/2025 (ECA Digital)  |  Decreto 12.880/2026  |  LGPD Lei 13.709/2018", styles["Capa_Info"]),
    ]]
    t_leis = Table(leis_data, colWidths=[14.5*cm])
    t_leis.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AZUL_ESCURO),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 40),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ]))
    elems.append(t_leis)
    elems.append(Spacer(1, 0.5*cm))

    aviso_data = [[
        Paragraph(
            "AVISO: Este documento e de carater informativo e preliminar. "
            "Nao substitui parecer juridico especializado. "
            "Consulte um advogado especializado em LGPD e ECA antes de publicar o aplicativo.",
            styles["Nota"]
        )
    ]]
    t_aviso = Table(aviso_data, colWidths=[14.5*cm])
    t_aviso.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), AMARELO_BG),
        ("BOX",           (0,0), (-1,-1), 1, AMARELO),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    elems.append(t_aviso)
    elems.append(PageBreak())
    return elems

def secao_permite(styles):
    elems = []
    elems.append(Paragraph("1. O que a lei PERMITE", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    elems.append(Paragraph("Lei 15.211/2025, Art. 2, II — Define e legaliza o Vigilia", styles["SubSecao"]))
    elems.append(Paragraph(
        "A lei cria uma categoria juridica especifica para o que o Vigilia faz — "
        "capturar imagens para monitoramento parental e explicita que isso e legal:",
        styles["Corpo"]))
    elems.append(caixa_lei(
        '"produto ou servico de monitoramento infantil: produto ou servico de tecnologia da informacao '
        'destinado ao acompanhamento, por pais ou responsaveis legais, das acoes executadas por criancas '
        'e adolescentes em ambientes digitais, a partir do <b>registro ou da transmissao de imagens</b>, '
        'de sons, de informacoes de localizacao, de atividade ou de outros dados"',
        styles))
    elems.append(caixa_nota(
        "Conclusao: o Vigilia se enquadra exatamente nessa definicao. "
        "Capturar imagens para monitoramento parental e <b>explicitamente previsto e legalizado</b> pela lei.",
        styles, bg=VERDE_BG))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Lei 15.211/2025, Art. 3, paragrafo unico — Direito e dever dos pais", styles["SubSecao"]))
    elems.append(caixa_lei(
        '"A crianca e o adolescente tem o direito de ser educados, orientados e acompanhados por seus '
        'pais ou responsaveis legais quanto ao uso da internet e a sua experiencia digital, e a estes '
        'incumbe o exercicio do <b>cuidado ativo e continuo, por meio da utilizacao de ferramentas de '
        'supervisao parental</b> adequadas a idade e ao estagio de desenvolvimento da crianca e do adolescente."',
        styles))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("Lei 15.211/2025, Arts. 17 e 18 — Obrigacoes dos fornecedores", styles["SubSecao"]))
    elems.append(Paragraph(
        "Fornecedores de apps <b>devem</b> disponibilizar ferramentas de supervisao parental. "
        "Essas ferramentas devem permitir que os pais:",
        styles["Corpo"]))
    items = [
        "I — visualizar, configurar e gerenciar as opcoes de conta e privacidade da crianca ou do adolescente;",
        "II — restringir compras e transacoes financeiras;",
        "III — identificar os perfis de adultos com os quais a crianca ou o adolescente se comunica;",
        "IV — acessar metricas consolidadas do tempo total de uso do produto ou servico.",
    ]
    for item in items:
        elems.append(Paragraph(f"• {item}", styles["Corpo"]))
    elems.append(Spacer(1, 0.3*cm))
    return elems

def secao_exige(styles):
    elems = []
    elems.append(Paragraph("2. O que a lei EXIGE (condicoes obrigatorias)", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    elems.append(Paragraph("Lei 15.211/2025, Art. 19 — O artigo mais importante para o Vigilia", styles["SubSecao"]))
    elems.append(caixa_lei(
        '<b>Art. 19 caput:</b> "Os produtos ou servicos de monitoramento infantil deverao conter '
        'mecanismos e solucoes de tecnologia da informacao e comunicacao vigentes para garantir a '
        '<b>inviolabilidade das imagens, dos sons e das outras informacoes captadas, armazenadas e '
        'transmitidas aos pais ou responsaveis legais</b>."',
        styles))
    elems.append(caixa_nota(
        "PONTO-CHAVE: a lei protege imagens 'transmitidas AOS PAIS'. "
        "O Vigilia <b>nunca transmite imagem aos pais</b> — transmite apenas texto. "
        "A arquitetura supera o requisito minimo legal.",
        styles, bg=VERDE_BG))
    elems.append(Spacer(1, 0.2*cm))

    elems.append(caixa_lei(
        '<b>Art. 19, §1:</b> "Os produtos ou servicos deverao conter mecanismos que informem as '
        'criancas e os adolescentes, em linguagem apropriada, acerca da realizacao do monitoramento."',
        styles))
    elems.append(caixa_nota(
        "Vigilia: icone discreto na status bar + tela de ciencia no setup com linguagem simples. "
        "Recomendado: guardar log de que o menor visualizou a tela de ciencia.",
        styles))
    elems.append(Spacer(1, 0.2*cm))

    elems.append(caixa_lei(
        '<b>Art. 19, §2:</b> "O desenvolvimento e o uso de mecanismos de monitoramento infantil '
        'deverao ser orientados pelo melhor interesse da crianca e do adolescente e pelo pleno '
        'desenvolvimento de suas capacidades."',
        styles))
    elems.append(Spacer(1, 0.3*cm))

    elems.append(Paragraph("LGPD Lei 13.709/2018 — Dados de criancas", styles["SubSecao"]))
    elems.append(caixa_lei(
        '<b>Art. 14:</b> O tratamento de dados pessoais de criancas deve ser realizado com o '
        'consentimento especifico e em destaque dado por pelo menos um dos pais ou pelo responsavel legal.',
        styles))
    elems.append(caixa_lei(
        '<b>Art. 6, III — Minimizacao:</b> Realizacao do tratamento com dados pertinentes, '
        'proporcionais e nao excessivos em relacao as finalidades do tratamento de dados.',
        styles))
    elems.append(caixa_nota(
        "Vigilia: monitoramento apenas dos apps selecionados pelos pais (lista configurada no setup). "
        "Nao monitora todos os apps — apenas os da lista. Isso cumpre o principio de minimizacao.",
        styles))
    elems.append(Spacer(1, 0.3*cm))
    return elems

def secao_vigilancia(styles):
    elems = []
    elems.append(Paragraph("3. A 'Vigilancia Massiva' — onde esta e o que significa", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    elems.append(Paragraph(
        "A proibicao de vigilancia massiva existe na lei, mas esta nos artigos sobre "
        "regulamentacao pelo governo — nao sobre apps privados diretamente.",
        styles["Corpo"]))

    elems.append(caixa_lei(
        '<b>Art. 34, §1:</b> "A regulamentacao nao podera, em nenhuma hipotese, autorizar ou '
        'resultar na implantacao de mecanismos de vigilancia massiva, generica ou indiscriminada, '
        'vedadas praticas contra os direitos fundamentais a liberdade de expressao, a privacidade, '
        'a protecao integral e ao tratamento diferenciado dos dados pessoais de criancas e de '
        'adolescentes, nos termos da Constituicao Federal e das Leis nos 8.069/1990 (ECA) e '
        '13.709/2018 (LGPD)."',
        styles))

    elems.append(caixa_lei(
        '<b>Art. 37, paragrafo unico:</b> "A regulamentacao nao podera, em nenhuma hipotese, '
        'impor, autorizar ou resultar na implantacao de mecanismos de vigilancia massiva, generica '
        'ou indiscriminada, vedadas as praticas que comprometam os direitos fundamentais a liberdade '
        'de expressao, a privacidade, a protecao integral e ao tratamento diferenciado dos dados '
        'pessoais de criancas e de adolescentes."',
        styles))

    elems.append(caixa_aviso(
        "ESCLARECIMENTO: Esses artigos sao dirigidos ao Poder Executivo ao regulamentar a lei "
        "(ANPD e governo), nao diretamente a apps privados. "
        "O argumento juridico correto para o Vigilia e: Art. 19 (imagens nunca chegam aos pais) "
        "+ LGPD Art. 6 III (monitoramento apenas de apps da lista escolhida pelos pais).",
        styles))
    elems.append(Spacer(1, 0.3*cm))
    return elems

def secao_eliminacao(styles):
    elems = []
    elems.append(Paragraph("4. Principio de Eliminacao Imediata — Decreto 12.880/2026", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    elems.append(caixa_lei(
        '<b>Decreto 12.880/2026, Art. 24, §3:</b> "O tratamento de dados decorrente da coleta de '
        'documentos devera limitar-se ao dado relativo a idade ou a confirmacao da faixa etaria, '
        '<b>vedado o armazenamento, a retencao ou qualquer forma de conservacao da imagem</b>, '
        'da copia do documento ou da informacao, que devera ser <b>eliminada de modo imediato e '
        'irreversivel</b> apos a captura da informacao necessaria, nos termos da Lei no 13.709/2018 (LGPD)."',
        styles))

    elems.append(caixa_nota(
        "Contexto: esse artigo trata de verificacao de idade de usuarios. "
        "Mas o principio de eliminacao imediata e irreversivel da imagem apos uso "
        "<b>reforça juridicamente a arquitetura do Vigilia</b>, que destroi a imagem do servidor "
        "imediatamente apos a analise pela IA — sem armazenamento, sem retencao.",
        styles))
    elems.append(Spacer(1, 0.3*cm))
    return elems

def secao_zonas(styles):
    elems = []
    elems.append(Paragraph("5. Zonas Cinzentas", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    zonas = [
        (
            "Imagem trafega pela API Mistral (terceiro)",
            "LGPD Art. 26 — transferencia de dados a operador terceiro. "
            "Mesmo que a imagem seja destruida no servidor do Vigilia, ela passa pela "
            "infraestrutura da Mistral AI antes de ser destruida.",
            "Usar Mistral (empresa europeia que declara nao treinar com dados de API) + "
            "documentar DPA (Data Processing Agreement) com a Mistral. "
            "Solucao definitiva: modelo de IA local (Fase 2 do projeto)."
        ),
        (
            "'Ciencia do menor' ainda e vaga",
            "O Art. 19 §1 exige informar a crianca em linguagem apropriada, mas nenhum "
            "tribunal brasileiro definiu o minimo suficiente para cumprir essa exigencia.",
            "Tela de ciencia no setup com linguagem simples + guardar log com timestamp "
            "de que o menor visualizou a tela."
        ),
        (
            "Adolescentes 12-18 tem capacidade relativa (Codigo Civil)",
            "Um adolescente de 15 anos pode argumentar que seu consentimento importa. "
            "Sem jurisprudencia especifica no Brasil ainda para apps de monitoramento parental.",
            "Termos de Uso com linguagem especifica por faixa etaria + assinatura do "
            "responsavel legal identificado por CPF."
        ),
        (
            "Responsabilidade civil do desenvolvedor",
            "Se o app falhar em detectar um risco e a crianca sofrer dano, os pais "
            "podem acionar o desenvolvedor por falha na prestacao do servico.",
            "Disclaimer claro nos Termos de Uso: o app e ferramenta de apoio parental, "
            "nao uma garantia de seguranca. Nao substitui supervisao ativa dos responsaveis."
        ),
    ]

    for i, (titulo, risco, mitigacao) in enumerate(zonas, 1):
        elems.append(KeepTogether([
            Paragraph(f"Zona {i}: {titulo}", styles["SubSecao"]),
            caixa_nota(f"<b>Risco:</b> {risco}", styles, bg=AMARELO_BG),
            Spacer(1, 0.1*cm),
            caixa_nota(f"<b>Mitigacao:</b> {mitigacao}", styles, bg=VERDE_BG),
            Spacer(1, 0.3*cm),
        ]))
    return elems

def secao_tabela(styles):
    elems = []
    elems.append(Paragraph("6. Arquitetura Vigilia vs. Requisitos Legais", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    header_style = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9,
                                   textColor=BRANCO, alignment=TA_CENTER)
    cell_style   = ParagraphStyle("td", fontName="Helvetica", fontSize=9,
                                   textColor=PRETO, leading=13)
    status_ok    = ParagraphStyle("ok",  fontName="Helvetica-Bold", fontSize=9,
                                   textColor=VERDE, alignment=TA_CENTER)
    status_warn  = ParagraphStyle("warn", fontName="Helvetica-Bold", fontSize=9,
                                   textColor=AMARELO, alignment=TA_CENTER)

    data = [
        [
            Paragraph("Decisao Tecnica", header_style),
            Paragraph("Lei", header_style),
            Paragraph("Artigo", header_style),
            Paragraph("Status", header_style),
        ],
        [
            Paragraph("Captura apenas apps da lista dos pais", cell_style),
            Paragraph("LGPD", cell_style),
            Paragraph("Art. 6 III — Minimizacao", cell_style),
            Paragraph("OK Conforme", status_ok),
        ],
        [
            Paragraph("Imagem destruida imediatamente no servidor", cell_style),
            Paragraph("Lei 15.211 + Decreto", cell_style),
            Paragraph("Art. 19 + Decreto Art. 24 §3", cell_style),
            Paragraph("OK Supera o exigido", status_ok),
        ],
        [
            Paragraph("Imagem NUNCA transmitida aos pais", cell_style),
            Paragraph("Lei 15.211", cell_style),
            Paragraph("Art. 19 caput", cell_style),
            Paragraph("OK Supera o exigido", status_ok),
        ],
        [
            Paragraph("Icone na status bar", cell_style),
            Paragraph("Lei 15.211", cell_style),
            Paragraph("Art. 19 §1", cell_style),
            Paragraph("OK Conforme", status_ok),
        ],
        [
            Paragraph("Tela de ciencia no setup", cell_style),
            Paragraph("Lei 15.211", cell_style),
            Paragraph("Art. 19 §1", cell_style),
            Paragraph("OK Conforme", status_ok),
        ],
        [
            Paragraph("Consentimento do responsavel no setup", cell_style),
            Paragraph("LGPD", cell_style),
            Paragraph("Art. 14", cell_style),
            Paragraph("OK Conforme", status_ok),
        ],
        [
            Paragraph("Imagem passa pela API Mistral", cell_style),
            Paragraph("LGPD", cell_style),
            Paragraph("Art. 26 (operador terceiro)", cell_style),
            Paragraph("!! Requer DPA", status_warn),
        ],
    ]

    col_widths = [5.5*cm, 2.5*cm, 4*cm, 2.5*cm]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [BRANCO, CINZA_CLARO]),
        ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND",    (0,7), (-1,7), AMARELO_BG),
    ]))
    elems.append(t)
    elems.append(Spacer(1, 0.3*cm))
    return elems

def secao_checklist(styles):
    elems = []
    elems.append(Paragraph("7. Checklist Obrigatorio antes de Lançar", styles["Secao"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=AZUL_ESCURO, spaceAfter=10))

    items = [
        ("Advogado LGPD/ECA",
         "Termos de Uso + Politica de Privacidade especificos para monitoramento de menores."),
        ("RIPD — Relatorio de Impacto a Protecao de Dados",
         "Exigido pelo ECA Digital Art. 16 §unico. Deve ser elaborado por DPO e compartilhado "
         "com a autoridade competente (ANPD) sob requisicao."),
        ("Tela de ciencia com log de visualizacao",
         "Guardar timestamp de que o menor visualizou a tela de ciencia no setup. "
         "Cumpre Art. 19 §1 da Lei 15.211/2025."),
        ("DPA documentado com Mistral AI",
         "LGPD Art. 26 — contrato de processamento de dados com o operador terceiro. "
         "Mistral AI declara nao treinar com dados de API."),
        ("Disclaimer de limitacoes",
         "Nos Termos de Uso: 'o app e ferramenta de apoio parental, nao uma garantia de seguranca'. "
         "Limita responsabilidade civil do desenvolvedor."),
        ("Endpoint de exclusao total de dados",
         "LGPD Art. 18 — o titular tem direito de apagar todos os seus dados. "
         "Implementar DELETE /api/account/ antes de lançar."),
    ]

    for i, (titulo, desc) in enumerate(items, 1):
        elems.append(KeepTogether([
            caixa_nota(
                f"<b>{i}. {titulo}</b><br/>{desc}",
                styles,
                bg=CINZA_CLARO
            ),
            Spacer(1, 0.15*cm),
        ]))

    elems.append(Spacer(1, 0.5*cm))
    elems.append(caixa_aviso(
        "LEMBRETE FINAL: Esta analise e preliminar e foi elaborada com base nos textos oficiais "
        "das leis. Nao substitui parecer juridico especializado. "
        "Consulte um advogado especializado em LGPD e direito digital antes de publicar o aplicativo.",
        styles))
    return elems

def main():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="Vigilia - Analise Juridica",
        author="Vigilia Team",
        subject="Analise ECA Digital, LGPD e Decreto 12.880/2026",
    )

    styles = build_styles()
    story = []

    story += capa(styles)
    story += secao_permite(styles)
    story += secao_exige(styles)
    story += secao_vigilancia(styles)
    story += secao_eliminacao(styles)
    story += secao_zonas(styles)
    story.append(PageBreak())
    story += secao_tabela(styles)
    story += secao_checklist(styles)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF gerado: {OUTPUT}")

if __name__ == "__main__":
    main()
