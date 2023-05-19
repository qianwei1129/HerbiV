from . import get
from . import compute
from . import output


def from_tcm(tcm,
             score=900,
             out_for_cytoscape=True,
             re=True,
             path='result/'):
    r"""
    进行经典的正向网络药理学分析
    :param tcm: 任何可以使用in判断一个元素是否在其中的组合数据类型，拟分析的中药的中文名称
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出，默认为900
    :param out_for_cytoscape: 布尔类型，是否输出用于Cytoscape绘图的文件
    :param re: 布尔类型，是否返回原始分析结果（中药、化合物（中药成分）、蛋白质（靶点）及其连接信息）
    :param path: 字符串类型，存放结果的目录
    :return: tcm: pd.DataFrame类型，中药信息
    :return: tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :return: chem: pd.DataFrame类型，化合物（中药成分）信息
    :return: chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :return: proteins: pd.DataFrame类型，蛋白质（靶点）信息
    """
    tcm = get.get_tcm('cn_name', tcm)
    tcm_chem_links = get.get_tcm_chem_links('HVMID', tcm['HVMID'])
    chem = get.get_chemicals('HVCID', tcm_chem_links['HVCID'])
    chem_protein_links = get.get_chem_protein_links('HVCID', chem['HVCID'], score)
    proteins = get.get_proteins('Ensembl_ID', chem_protein_links['Ensembl_ID'])

    # 若化合物（中药成分）-蛋白质（靶点）连接使用了score过滤，则需要依照过滤结果修改chem、tcm_chem_links和tcm
    if score > 0:
        chem = chem.loc[chem.loc[:, 'HVCID'].isin(chem_protein_links['HVCID'])]
        tcm_chem_links = tcm_chem_links.loc[tcm_chem_links.loc[:, 'HVCID'].isin(chem['HVCID'])]
        tcm = tcm.loc[tcm.loc[:, 'HVMID'].isin(tcm_chem_links['HVMID'])]
        # 重新编号（chem和tcm在计算score时会重新编号，此处不再重新编号）
        tcm_chem_links.index = range(tcm_chem_links.shape[0])

    tcm, chem = compute.score(tcm, tcm_chem_links, chem, chem_protein_links)

    if out_for_cytoscape:
        output.out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, proteins, path)

    if re:
        return tcm, tcm_chem_links, chem, chem_protein_links, proteins


def from_proteins(proteins,
                  score=0,
                  random_state=None,
                  out_for_cytoscape=True,
                  re=True,
                  path='result/'):
    r"""
    进行逆向网络药理学分析
    :param proteins: 任何可以使用in判断一个元素是否在其中的组合数据类型，存储拟分析蛋白质（靶点）在STITCH中的Ensembl_ID
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出，默认为0
    :param random_state: int类型，指定随机数种子
    :param out_for_cytoscape: 布尔类型，是否输出用于Cytoscape绘图的文件
    :param re: 布尔类型，是否返回原始分析结果
    :param path: 字符串类型，存放结果的目录
    :return: tcm: pd.DataFrame类型，中药信息
    :return: tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :return: chem: pd.DataFrame类型，化合物（中药成分）信息
    :return: chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :return: protein: pd.DataFrame类型，蛋白质（靶点）信息
    """
    protein = get.get_proteins('Ensembl_ID', proteins)
    chem_protein_links = get.get_chem_protein_links('Ensembl_ID', protein['Ensembl_ID'], score)
    chem = get.get_chemicals('HVCID', chem_protein_links['HVCID'])
    tcm_chem_links = get.get_tcm_chem_links('HVCID', chem['HVCID'])
    tcm = get.get_tcm('HVMID', tcm_chem_links['HVMID'])
    formula_tcm_links = get.get_formula_tcm_links('HVMID', tcm['HVMID'])
    formula = get.get_formula('HVPID', formula_tcm_links['HVPID'])

    tcm, chem, formula = compute.score(tcm, tcm_chem_links, chem, chem_protein_links, formula, formula_tcm_links)
    tcms = compute.component(tcm.loc[tcm['Importance Score'] != 1.0], random_state)
    formulas = compute.component(formula.loc[formula['Importance Score'] != 1.0], random_state)

    if out_for_cytoscape:
        output.out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, protein, path)

    if re:
        return formula, tcm, tcm_chem_links, chem, chem_protein_links, protein, tcms, formulas


def from_tcm_protein(tcm,
                     proteins,
                     score=0,
                     out_for_cytoscape=True,
                     re=True,
                     path='result/'):
    r"""
    进行经典的正向网络药理学分析，并根据给定的靶点筛选结果
    :param tcm: 任何可以使用in判断一个元素是否在其中的组合数据类型，拟分析的中药的中文名称
    :param proteins: 任何可以使用in判断一个元素是否在其中的组合数据类型，拟分析蛋白质（靶点）在STITCH中的Ensembl_ID
    :param score: int类型，仅combined_score大于等于score的记录会被筛选出
    :param out_for_cytoscape: 布尔类型，是否输出用于Cytoscape绘图的文件
    :param re: 布尔类型，是否返回原始分析结果
    :param path: 字符串类型，存放结果的目录
    :return: tcm: pd.DataFrame类型，中药信息
    :return: tcm_chem_links: pd.DataFrame类型，中药-化合物（中药成分）连接信息
    :return: chem: pd.DataFrame类型，化合物（中药成分）信息
    :return: chem_protein_links: pd.DataFrame类型，化合物（中药成分）-蛋白质（靶点）连接信息
    :return: protein: pd.DataFrame类型，蛋白质（靶点）信息
    """
    # 检索中药和蛋白质（靶点）
    tcm = get.get_tcm('cn_name', tcm)
    proteins = get.get_proteins('Ensembl_ID', proteins)

    # 根据中药和蛋白质（靶点）获取中药-化合物（中药成分）连接和化合物（中药成分）-蛋白质（靶点）连接
    tcm_chem_links = get.get_tcm_chem_links('HVMID', tcm['HVMID'])
    chem_protein_links = get.get_chem_protein_links('Ensembl_ID', proteins['Ensembl_ID'], score)

    # 获取中药-化合物（中药成分）连接和化合物（中药成分）-蛋白质（靶点）连接中化合物（中药成分）的交集
    chem_from_tcm_chem_links = get.get_chemicals('HVCID', tcm_chem_links['HVCID'])
    chem_from_chem_protein_links = get.get_chemicals('HVCID', chem_protein_links['HVCID'])
    chem = chem_from_tcm_chem_links.loc[chem_from_tcm_chem_links['HVCID'].isin(chem_from_chem_protein_links['HVCID'])]

    # 根据化合物（中药成分）的交集过滤中药-化合物（中药成分）连接和化合物（中药成分）-蛋白质（靶点）连接以及中药和蛋白质（靶点）
    tcm_chem_links = tcm_chem_links.loc[tcm_chem_links.loc[:, 'HVCID'].isin(chem['HVCID'])]
    tcm = tcm.loc[tcm.loc[:, 'HVMID'].isin(tcm_chem_links['HVMID'])]
    chem_protein_links = chem_protein_links.loc[chem_protein_links.loc[:, 'HVCID'].isin(chem['HVCID'])]
    proteins = proteins.loc[proteins.loc[:, 'Ensembl_ID'].isin(chem_protein_links['Ensembl_ID'])]

    # 重新编号（chem和tcm在计算score时会重新编号，此处不再重新编号）
    tcm_chem_links.index = range(tcm_chem_links.shape[0])
    chem_protein_links.index = range(chem_protein_links.shape[0])
    proteins.index = range(proteins.shape[0])

    tcm, chem = compute.score(tcm, tcm_chem_links, chem, chem_protein_links)

    if out_for_cytoscape:
        output.out_for_cyto(tcm, tcm_chem_links, chem, chem_protein_links, proteins, path)

    if re:
        return tcm, tcm_chem_links, chem, chem_protein_links, proteins


if __name__ == '__main__':
    tcm_ft, tcm_chem_links_ft, chem_ft, chem_protein_links_ft, protein_ft = from_tcm(['柴胡', '黄芩'])
    tcm_fg, tcm_chem_links_fg, chem_fg, chem_protein_links_fg, protein_fg, tcms, formulas = from_proteins(
        ['ENSP00000381588', 'ENSP00000252519'])
    tcm_ftp, tcm_chem_links_ftp, chem_ftp, chem_protein_links_ftp, protein_ftp = from_tcm_protein(['柴胡', '黄芩'],
                                                                                                  ['ENSP00000381588',
                                                                                                   'ENSP00000252519'])
