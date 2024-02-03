import pandas as pd
import os
from typing import Tuple


# TODO: 为各函数增加抛出异常功能，若无法查询到相关信息，则抛出异常。

def get_formula(by, items) -> pd.DataFrame:
    """
        读取HerbiV_formula数据集，返回items中复方的信息。
        Read the HerbiV_formula dataset and return the information about the compound party in items.

        Args:
            by (str): 数据集中与items相匹配的列的列名。The column name of the column in the dataset that matches items.
            items (collections.abc.Iterable): 要查询的复方。

        Returns:
            formula: items中复方的信息。Information on compounding in items.

        Examples:
            >>> get_formula('HVPID', ['HVP1625'])# 获取HVPID为HVP1625的复方（小柴胡汤）的信息
                 HVPID  ... Source Document
            0  HVP1625  ...   shang han lun
            [1 rows x 6 columns]
    """

    # 读取HerbiV_formula数据集
    formula_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + r'/data/HerbiV_formula.csv')

    # 在数据集中获取items中复方的信息
    formula = formula_all.loc[formula_all[by].isin(items)].copy()

    # 重新设置索引
    formula.index = range(formula.shape[0])

    return formula


def get_formula_tcm_links(by, items) -> pd.DataFrame:
    """
        读取HerbiV_formula_tcm_links数据集，返回items中复方/中药的复方-中药连接信息。

        Args:
            by (str):数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的复方/中药。

        Returns:
            formula_tcm_links(pandas.DataFrame): items中复方/中药的复方-中药连接信息。

        Examples:
            >>> get_formula_tcm_links('HVPID', ['HVP1625'])# 获取HVPID为HVP1625的复方（小柴胡汤）的复方-中药连接信息
                 HVPID    HVMID
            0  HVP1625  HVM0367
            1  HVP1625  HVM0735
            2  HVP1625  HVM0766
            3  HVP1625  HVM1695
            4  HVP1625  HVM3203
            5  HVP1625  HVM4463
    """

    # 读取HerbiV_formula_tcm_links数据集
    formula_tcm_links_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +
                                        r'/data/HerbiV_formula_tcm_links.csv')

    # 在数据集中获取items中复方/中药的复方-中药连接信息
    formula_tcm_links = formula_tcm_links_all.loc[formula_tcm_links_all[by].isin(items)].copy()

    # 重新设置索引
    formula_tcm_links.index = range(formula_tcm_links.shape[0])

    return formula_tcm_links


def get_tcm(by, items) -> pd.DataFrame:
    """
        读取HerbiV_tcm数据集，返回items中中药的信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的中药。

        Returns:
            pandas.DataFrame: items中中药的信息。

        Examples:
            >>> get_tcm('cn_name', ['柴胡', '黄芩'])# 获取cn_name（中文名）为柴胡和黄芩的中药的信息（不建议使用中文名检索）
                 HVMID cn_name pinyin_name  ... TCM_ID_id SymMap_id TCMSP_id
            0  HVM0367      柴胡     CHAI HU  ...    3396.0      58.0     80.0
            1  HVM1695      黄芩   HUANG QIN  ...    6700.0     188.0    371.0
            [2 rows x 19 columns]
    """

    # 读取HerbiV_tcm数据集
    tcm_all = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + r'/data/HerbiV_tcm.csv')

    # 在数据集中获取items中中药的信息
    tcm = tcm_all.loc[tcm_all[by].isin(items)].copy()

    # 重新设置索引
    tcm.index = range(tcm.shape[0])

    return tcm


def get_tcm_chem_links(by, items) -> pd.DataFrame:
    """
        读取HerbiV_tcm_chemical_links数据集，返回items中中药/化合物的中药-成分（化合物）连接信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的中药/化合物。

        Returns:
            pandas.DataFrame: items中中药/化合物的中药-成分连接信息。

        Examples:
            >>> get_tcm_chem_links('HVMID', ['HVM0367'])# 获取HVMID为HVM0367的中药（柴胡）的中药-成分连接信息
                   HVMID    HVCID
            0    HVM0367  HVC0284
            1    HVM0367  HVC3018
            2    HVM0367  HVC0396
            3    HVM0367  HVC1371
            4    HVM0367  HVC1045
            ..       ...      ...
            311  HVM0367  HVC2149
            312  HVM0367  HVC0465
            313  HVM0367  HVC0941
            314  HVM0367  HVC0936
            315  HVM0367  HVC1279
            [316 rows x 2 columns]
    """

    # 读取HerbiV_tcm_chemical_links数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    tcm_chem_links_all = pd.read_csv(current_directory + r'/data/HerbiV_tcm_chemical_links.csv')

    # 在数据集中获取items中中药/化合物的中药-成分连接信息
    tcm_chem_links = tcm_chem_links_all.loc[tcm_chem_links_all[by].isin(items)].copy()

    # 重新设置索引
    tcm_chem_links.index = range(tcm_chem_links.shape[0])

    return tcm_chem_links


def get_chemicals(by, items) -> pd.DataFrame:
    """
        读取HerbiV_chemicals数据集，返回items中化合物的信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的化合物。

        Returns:
            pandas.DataFrame: items中化合物的信息。

        Examples:
            >>> chaihu = get_tcm_chem_links('HVMID', ['HVM0367'])# 获取HVMID为HVM0367的中药（柴胡）的中药-成分连接信息
            >>> get_chemicals('HVCID', chaihu['HVCID'])# 获取柴胡的成分的信息
                   HVCID                                     Name  ...     STITCH_id     HERB_id
            0    HVC0034                                allantoin  ...  CIDm00000204  HBIN015193
            1    HVC0036                                  glucose  ...  CIDm00000206  HBIN001003
            2    HVC0046                             benzaldehyde  ...  CIDm00000240  HBIN017734
            3    HVC0071                                 coumarin  ...  CIDm00000323  HBIN021605
            4    HVC0073                            cuminaldehyde  ...  CIDm00000326  HBIN010591
            ..       ...                                      ...  ...           ...         ...
            253  HVC6045                        8-hydroxydaidzein  ...  CIDm05466139  HBIN012955
            254  HVC6054                                narcissin  ...  CIDm05481663  HBIN031161
            255  HVC6156  stigmasterol-3-O-beta-D-glucopyranoside  ...  CIDm06440962  HBIN015690
            256  HVC6183                           beta-gurjunene  ...  CIDm06450812  HBIN018138
            257  HVC6204                         geraniol acetate  ...  CIDm06850714  HBIN027529
            [258 rows x 8 columns]
    """

    # 读取HerbiV_chemical_protein_links数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_all = pd.read_csv(current_directory + r'/data/HerbiV_chemicals.csv')

    # 在数据集中获取items中化合物的信息
    chem = chem_all.loc[chem_all[by].isin(items)].drop_duplicates(subset=['HVCID'])

    # 重新设置索引
    chem.index = range(chem.shape[0])

    return chem


def get_chem_protein_links(by, items, score=900) -> pd.DataFrame:
    """
        读取HerbiV_chemicals数据集，返回items中化合物/蛋白的化合物-靶点（蛋白）连接的combined_score大于等于score的连接信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的化合物/蛋白。
            score (int): 仅combined_score大于等于score的记录会被筛选出，默认为900，最大为1000，最小为0。

        Returns:
            pandas.DataFrame: items中化合物/蛋白的化合物-靶点（蛋白）连接的combined_score大于等于score的连接信息。

        Examples:
            >>> # 获取Ensembl ID为ENSP00000335062的蛋白（PDCD1）的化合物-靶点连接信息
            >>> get_chem_protein_links('Ensembl_ID', ['ENSP00000335062'])
                 HVCID       Ensembl_ID  Combined_score
            0  HVC5134  ENSP00000335062           0.202
            1  HVC0159  ENSP00000335062           0.795
    """

    # 读取HerbiV_chemical_protein_links数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    chem_protein_links_all = pd.read_csv(current_directory + r'/data/HerbiV_chemical_protein_links.csv')

    # 在数据集中获取items中化合物/蛋白的化合物-靶点（蛋白）连接的combined_score大于等于score的连接信息
    chem_protein_links = chem_protein_links_all.loc[
        (chem_protein_links_all[by].isin(items)) &
        (chem_protein_links_all['Combined_score'] >= score)].copy()

    # 将Combined_score变换为0-1的浮点数
    chem_protein_links.loc[:, 'Combined_score'] = chem_protein_links.loc[:, 'Combined_score'].apply(
        lambda x: x / 1000)

    # 重新设置索引
    chem_protein_links.index = range(chem_protein_links.shape[0])

    return chem_protein_links


def get_proteins(by, items) -> pd.DataFrame:
    """
        读取HerbiV_proteins数据集，返回items中蛋白的信息。

        Args:
            by (str): 数据集中与items相匹配的列的列名。
            items (collections.abc.Iterable): 要查询的蛋白。

        Returns:
            pandas.DataFrame: items中蛋白的信息。

        Examples:
            >>> get_proteins('protein_name', ['PDCD1 PD1'])# 获取gene_name（基因名）为PDCD1 PD1的蛋白的信息（不建议使用名称检索）
                    Ensembl_ID  ...  gene_name
            0  ENSP00000335062  ...  PDCD1 PD1
    """

    # 读取HerbiV_proteins数据集
    current_directory = os.path.dirname(os.path.abspath(__file__))
    proteins_all = pd.read_csv(current_directory + r'/data/HerbiV_proteins.csv')

    # 在数据集中获取items中蛋白的信息
    proteins = proteins_all.loc[proteins_all[by].isin(items)].drop_duplicates(subset=['Ensembl_ID'])

    # 重置索引
    proteins.index = range(proteins.shape[0])

    return proteins


def get_tcm_and_formula(tcm_and_formula) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
        获取tcm_or_formula中元素对应（及连接）的中药、复方及其连接信息。

        Args:
            tcm_and_formula (collections.abc.Iterable): 要查询的中药或复方的ID

        Returns:
            - formula：tcm_or_formula中的（或中药对应的）复方的信息。
            - tcm：tcm_or_formula中的（或复方对应的）中药的信息。
            - formula_tcm_links：tcm_or_formula中的复方或中药的复方-中药连接信息。

    """

    if tcm_and_formula[0][2] == 'P':  # 判断输入是否为复方的HVPID
        formula = get_formula('HVPID', tcm_and_formula)  # 获取该复方的信息
        formula_tcm_links = get_formula_tcm_links('HVPID', formula['HVPID'])
        tcm = get_tcm('HVMID', formula_tcm_links['HVMID'])
    else:
        formula = None
        formula_tcm_links = None
        tcm = get_tcm('HVMID', tcm_and_formula)
    return formula, tcm, formula_tcm_links


if __name__ == '__main__':
    formula_info = get_formula('HVPID', ['HVP1625'])
    formula_tcm_links_info = get_formula_tcm_links('HVPID', formula_info['HVPID'])
    tcm_info = get_tcm('HVMID', formula_tcm_links_info['HVMID'])
    tcm_chem_links_info = get_tcm_chem_links('HVMID', tcm_info['HVMID'])
    chem_info = get_chemicals('HVCID', tcm_chem_links_info['HVCID'])
    chem_protein_links_info = get_chem_protein_links('HVCID', chem_info['HVCID'])
    protein_info = get_proteins('Ensembl_ID', chem_protein_links_info['Ensembl_ID'])
    formula_info1, tcm_info1, formula_tcm_links_info1 = get_tcm_and_formula(['HVP1625'])
    formula_info2, tcm_info2, formula_tcm_links_info2 = get_tcm_and_formula(['HVM0367', 'HVM1695'])
