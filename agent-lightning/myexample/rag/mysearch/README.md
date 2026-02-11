# 搜索接口文档
# 文献搜索

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /search/home/keywords:
    post:
      summary: 文献搜索
      deprecated: false
      description: ''
      tags:
        - 文献搜索2.0
      parameters:
        - name: token
          in: header
          description: 请用自己的环境变量
          example: '{{token}}'
          schema:
            type: string
            default: '{{token}}'
        - name: X-API-Version
          in: header
          description: ''
          example: '5003007'
          schema:
            type: string
            default: '5003007'
        - name: Authorization
          in: header
          description: 请用自己的环境变量
          example: '{{Authorization}}'
          schema:
            type: string
            default: '{{Authorization}}'
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                keywords:
                  description: 查询内容
                  type: string
                category:
                  description: category = 3 为综合搜索，不区分临床和指南
                  type: integer
                field:
                  description: 定向搜索
                  type: string
                sort:
                  description: 排序默认相关性， docIf、docPublishTime、citedBy
                  type: string
                filter:
                  description: >-
                    过滤条件，@@AND$$doc_mesh_terms$$Female@@AND$$doc_mesh_terms$$Infant
                  type: string
                pageNum:
                  type: integer
                pageSize:
                  type: integer
                nearMonth:
                  description: 最近几个月
                  type: integer
                docPublishTypes:
                  type: array
                  items:
                    type: string
                  description: 指定文档类型 Systematic Review  / Meta-Analysis
                diseaseTagsQuery:
                  type: array
                  items:
                    type: string
                  description: 疾病id
                type:
                  description: 带查询历史加入这个参数，如高级搜索，其他不带这个参数。高搜历史传doc
                  type: string
              required:
                - category
                - pageNum
                - pageSize
              x-apifox-orders:
                - keywords
                - category
                - field
                - sort
                - filter
                - pageNum
                - pageSize
                - nearMonth
                - docPublishTypes
                - diseaseTagsQuery
                - type
            example: "{\r\n    \"keywords\": \"\", //查询内容\r\n    \"category\": 3, //category = 3 为综合搜索，不区分临床和指南\r\n    \"field\": \"\", //定向搜索\r\n    \"sort\": \"\", //排序默认相关性， docIf、docPublishTime、citedBy\r\n    \"filter\": \"\", //过滤条件，@@AND$$doc_mesh_terms$$Female@@AND$$doc_mesh_terms$$Infant\r\n    \"pageNum\": 1,\r\n    \"pageSize\": 10\r\n    //,\"type\":\"doc\" //带查询历史加入这个参数，如高级搜索，其他不带这个参数\r\n    ,\r\n    \"nearMonth\": 200 //最近几个月\r\n    ,\r\n    \"docPublishTypes\": [\r\n        \"Meta-Analysis\",\r\n        \"Systematic Review\"\r\n    ] // 指定文档类型 Systematic Review  / Meta-Analysis\r\n    ,\r\n    \"diseaseTagsQuery\": [\r\n        \"267\"\r\n    ] // 疾病id\r\n}"
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      records:
                        type: array
                        items:
                          type: object
                          properties:
                            country:
                              type: string
                            modifiedTime:
                              type: string
                            docTags:
                              type: string
                            zkyArea:
                              type: string
                            year:
                              type: string
                            docLastAddr:
                              type: string
                            docDoi:
                              type: string
                            docTitle:
                              type: string
                            qiniuUrl:
                              type: string
                            highLightDocAbstract:
                              type: string
                            diseaseTags:
                              type: string
                            highLightDocTitle:
                              type: string
                            docAddrQuery:
                              type: array
                              items:
                                type: string
                            pages:
                              type: string
                            province:
                              type: string
                            createdTime:
                              type: string
                            aiOverview:
                              type: string
                            id:
                              type: string
                            docAuthor:
                              type: string
                            docAddr:
                              type: string
                            issue:
                              type: string
                            pptUrl:
                              type: string
                            docFirstAddr:
                              type: string
                            textStatus:
                              type: string
                            docPublishTypeQuery:
                              type: array
                              items:
                                type: string
                            qiniuUrlZh:
                              type: string
                            docKeywords:
                              type: string
                            diseaseTagsQuery:
                              type: array
                              items:
                                type: string
                            volume:
                              type: string
                            docAbstract:
                              type: string
                            pageIdx:
                              type: string
                            sourcesCode:
                              type: string
                            status:
                              type: string
                            illnessQuery:
                              type: array
                              items:
                                type: string
                            docIf:
                              type: string
                            docSimpleJournal:
                              type: string
                            highLightDocAuthor:
                              type: string
                            docMeshTermsQuery:
                              type: array
                              items:
                                type: object
                                properties:
                                  path:
                                    type: string
                                  is_subheading_star:
                                    type: boolean
                                  origin_string:
                                    type: string
                                  term:
                                    type: string
                                  is_star:
                                    type: boolean
                                  subheading:
                                    type: string
                                required:
                                  - path
                                  - is_subheading_star
                                  - origin_string
                                  - term
                                  - is_star
                                  - subheading
                                x-apifox-orders:
                                  - path
                                  - is_subheading_star
                                  - origin_string
                                  - term
                                  - is_star
                                  - subheading
                            journalId:
                              type: string
                            docPublishTime:
                              type: string
                            ztTags:
                              type: string
                            docSourceJournal:
                              type: string
                            docFirstAuthor:
                              type: string
                            videoUrl:
                              type: string
                            docMeshTerms:
                              type: string
                            pptEnUrl:
                              type: string
                            illness:
                              type: string
                            highLightDocKeywords:
                              type: string
                            citedBy:
                              type: string
                            queryScore:
                              type: integer
                            docInfo:
                              type: string
                            pmid:
                              type: string
                            docTitleZh:
                              type: string
                            docAuthorNested:
                              type: array
                              items:
                                type: object
                                properties:
                                  name:
                                    type: string
                                required:
                                  - name
                                x-apifox-orders:
                                  - name
                            meshTags:
                              type: string
                            docLastAuthor:
                              type: string
                            organization:
                              type: string
                            category:
                              type: string
                            xkTags:
                              type: string
                            docPublishType:
                              type: string
                            docKeywordsQuery:
                              type: string
                            docTagsQuery:
                              type: array
                              items:
                                type: string
                            docAbstractZh:
                              type: string
                          required:
                            - country
                            - modifiedTime
                            - docTags
                            - zkyArea
                            - year
                            - docLastAddr
                            - docDoi
                            - docTitle
                            - qiniuUrl
                            - highLightDocAbstract
                            - diseaseTags
                            - highLightDocTitle
                            - docAddrQuery
                            - pages
                            - province
                            - createdTime
                            - aiOverview
                            - id
                            - docAuthor
                            - docAddr
                            - issue
                            - pptUrl
                            - docFirstAddr
                            - textStatus
                            - docPublishTypeQuery
                            - qiniuUrlZh
                            - docKeywords
                            - diseaseTagsQuery
                            - volume
                            - docAbstract
                            - pageIdx
                            - sourcesCode
                            - status
                            - illnessQuery
                            - docIf
                            - docSimpleJournal
                            - highLightDocAuthor
                            - docMeshTermsQuery
                            - journalId
                            - docPublishTime
                            - ztTags
                            - docSourceJournal
                            - docFirstAuthor
                            - videoUrl
                            - docMeshTerms
                            - pptEnUrl
                            - illness
                            - highLightDocKeywords
                            - citedBy
                            - queryScore
                            - docInfo
                            - pmid
                            - docTitleZh
                            - docAuthorNested
                            - meshTags
                            - docLastAuthor
                            - organization
                            - category
                            - xkTags
                            - docPublishType
                            - docKeywordsQuery
                            - docTagsQuery
                            - docAbstractZh
                          x-apifox-orders:
                            - country
                            - modifiedTime
                            - docTags
                            - zkyArea
                            - year
                            - docLastAddr
                            - docDoi
                            - docTitle
                            - qiniuUrl
                            - highLightDocAbstract
                            - diseaseTags
                            - highLightDocTitle
                            - docAddrQuery
                            - pages
                            - province
                            - createdTime
                            - aiOverview
                            - id
                            - docAuthor
                            - docAddr
                            - issue
                            - pptUrl
                            - docFirstAddr
                            - textStatus
                            - docPublishTypeQuery
                            - qiniuUrlZh
                            - docKeywords
                            - diseaseTagsQuery
                            - volume
                            - docAbstract
                            - pageIdx
                            - sourcesCode
                            - status
                            - illnessQuery
                            - docIf
                            - docSimpleJournal
                            - highLightDocAuthor
                            - docMeshTermsQuery
                            - journalId
                            - docPublishTime
                            - ztTags
                            - docSourceJournal
                            - docFirstAuthor
                            - videoUrl
                            - docMeshTerms
                            - pptEnUrl
                            - illness
                            - highLightDocKeywords
                            - citedBy
                            - queryScore
                            - docInfo
                            - pmid
                            - docTitleZh
                            - docAuthorNested
                            - meshTags
                            - docLastAuthor
                            - organization
                            - category
                            - xkTags
                            - docPublishType
                            - docKeywordsQuery
                            - docTagsQuery
                            - docAbstractZh
                      total:
                        type: integer
                      size:
                        type: integer
                      current:
                        type: integer
                      pages:
                        type: integer
                    required:
                      - records
                      - total
                      - size
                      - current
                      - pages
                    x-apifox-orders:
                      - records
                      - total
                      - size
                      - current
                      - pages
                required:
                  - code
                  - msg
                  - data
                x-apifox-orders:
                  - code
                  - msg
                  - data
              example:
                code: 0
                msg: success
                data:
                  records:
                    - country: ''
                      modifiedTime: '2025-08-26T14:13:44Z'
                      docTags: ''
                      zkyArea: 医学 3区
                      year: ''
                      docLastAddr: ' Department of Gastroenterological and Pediatric Surgery, Faculty of Medicine, Oita University, 1-1 Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan.'
                      docDoi: 10.1007/s00268-021-06071-x
                      docTitle: >-
                        How Should We Treat Pancreatic Metastases from Renal
                        Cell Carcinoma? A Meta-Analysis
                      qiniuUrl: >-
                        https://doc3.infox-med.com/33768307_59a7c4b5d60e4880bb19b5c0e412e976.pdf
                      highLightDocAbstract: >-
                        Background: The treatment strategy for pancreatic
                        metastasis (PM) from renal cell carcinoma (RCC) is
                        unclear due to its rarity. The aim of this study was to
                        reveal the role of surgery for PM from RCC. 

                        Methods: A systematic literature search was conducted
                        using PubMed and the Cochrane Library. The effectiveness
                        of surgery for PM was evaluated based on the primary
                        outcome of overall survival (OS), which was investigated
                        in relation to surgical procedures and metastatic sites
                        via subgroup analyses. 

                        Results: There was no significant difference in the rate
                        of 2-year OS between the surgery and control group (OR
                        0.43, 95% CI 0.14-1.26, P = 0.12). However, the rate of
                        5-year OS was significantly higher in the surgery group
                        than the control group (OR = 0.41, 95% CI 0.18-0.93, P =
                        0.03). The rates of the complications and OS were not
                        significantly different between radical and conservative
                        pancreatectomies. The rate of 5-year OS of the patients
                        with PM was higher than that with other metastases (OR
                        0.38, 95% CI 0.20-0.74, P = 0.004). Conclusion: Surgical
                        resection for PM from RCC is associated with good
                        prognosis. Limited surgery may be a useful option
                        depending on the location of the lesion.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        How Should We Treat Pancreatic Metastases from Renal
                        Cell Carcinoma? A Meta-Analysis
                      docAddrQuery:
                        - >-
                          Department of Gastroenterological and Pediatric
                          Surgery, Faculty of Medicine, Oita University, 1-1
                          Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan.
                          teij03@oita-u.ac.jp.
                        - >-
                          Department of Gastroenterological and Pediatric
                          Surgery, Faculty of Medicine, Oita University, 1-1
                          Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan.
                        - >-
                          Department of Urology, Faculty of Medicine, Oita
                          University, 1-1 Hasama-machi, Yufu , Oita, 879-5593,
                          Japan.
                      pages: '0'
                      province: ''
                      createdTime: '2021-04-29T18:51:14Z'
                      aiOverview: ''
                      id: '21450574'
                      docAuthor: >-
                        Teijiro Hirashita,Yukio Iwashita,Yuichi Endo,Atsuro
                        Fujinaga,Toshitaka Shin,Hiromitsu Mimata,Masafumi
                        Inomata
                      docAddr: ' Department of Gastroenterological and Pediatric Surgery, Faculty of Medicine, Oita University, 1-1 Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan. teij03@oita-u.ac.jp.;; Department of Gastroenterological and Pediatric Surgery, Faculty of Medicine, Oita University, 1-1 Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan.;; Department of Urology, Faculty of Medicine, Oita University, 1-1 Hasama-machi, Yufu , Oita, 879-5593, Japan.'
                      issue: ''
                      pptUrl: ''
                      docFirstAddr: ' Department of Gastroenterological and Pediatric Surgery, Faculty of Medicine, Oita University, 1-1 Idaigaoka, Hasama-machi, Yufu, Oita, 879-5593, Japan. teij03@oita-u.ac.jp.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Meta-Analysis
                      qiniuUrlZh: ''
                      docKeywords: ''
                      diseaseTagsQuery:
                        - '267'
                      volume: ''
                      docAbstract: >-
                        Background: The treatment strategy for pancreatic
                        metastasis (PM) from renal cell carcinoma (RCC) is
                        unclear due to its rarity. The aim of this study was to
                        reveal the role of surgery for PM from RCC. 

                        Methods: A systematic literature search was conducted
                        using PubMed and the Cochrane Library. The effectiveness
                        of surgery for PM was evaluated based on the primary
                        outcome of overall survival (OS), which was investigated
                        in relation to surgical procedures and metastatic sites
                        via subgroup analyses. 

                        Results: There was no significant difference in the rate
                        of 2-year OS between the surgery and control group (OR
                        0.43, 95% CI 0.14-1.26, P = 0.12). However, the rate of
                        5-year OS was significantly higher in the surgery group
                        than the control group (OR = 0.41, 95% CI 0.18-0.93, P =
                        0.03). The rates of the complications and OS were not
                        significantly different between radical and conservative
                        pancreatectomies. The rate of 5-year OS of the patients
                        with PM was higher than that with other metastases (OR
                        0.38, 95% CI 0.20-0.74, P = 0.004). Conclusion: Surgical
                        resection for PM from RCC is associated with good
                        prognosis. Limited surgery may be a useful option
                        depending on the location of the lesion.
                      pageIdx: ''
                      sourcesCode: PMID33768307
                      status: '2'
                      illnessQuery:
                        - 肿瘤::肾癌
                        - 肿瘤::胰腺癌
                      docIf: '2.500'
                      docSimpleJournal: ''
                      highLightDocAuthor: >-
                        Teijiro Hirashita, Yukio Iwashita, Yuichi Endo, Atsuro
                        Fujinaga, Toshitaka Shin, Hiromitsu Mimata, Masafumi
                        Inomata
                      docMeshTermsQuery:
                        - path: C12.950.983.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C04.557.470.200.025.390
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C04.588.945.947.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C12.200.758.820.750.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C12.200.777.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C12.050.351.968.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: C12.050.351.937.820.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / surgery
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: surgery
                        - path: B01.050.150.900.649.313.988.400.112.400.400
                          is_subheading_star: false
                          origin_string: Humans
                          term: Humans
                          is_star: false
                          subheading: ''
                        - path: C12.900.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.950.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.950.983.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C04.588.945.947.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.200.758.820.750
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.200.777.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.050.351.937.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C12.050.351.968.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / surgery
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: E04.210.752
                          is_subheading_star: false
                          origin_string: Pancreatectomy
                          term: Pancreatectomy
                          is_star: false
                          subheading: ''
                        - path: C06.689.667
                          is_subheading_star: false
                          origin_string: Pancreatic Neoplasms* / surgery
                          term: Pancreatic Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C04.588.274.761
                          is_subheading_star: false
                          origin_string: Pancreatic Neoplasms* / surgery
                          term: Pancreatic Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: C04.588.322.475
                          is_subheading_star: false
                          origin_string: Pancreatic Neoplasms* / surgery
                          term: Pancreatic Neoplasms
                          is_star: true
                          subheading: surgery
                        - path: E01.789
                          is_subheading_star: false
                          origin_string: Prognosis
                          term: Prognosis
                          is_star: false
                          subheading: ''
                        - path: N01.224.935.698.826
                          is_subheading_star: false
                          origin_string: Survival Rate
                          term: Survival Rate
                          is_star: false
                          subheading: ''
                        - path: E05.318.308.985.550.900
                          is_subheading_star: false
                          origin_string: Survival Rate
                          term: Survival Rate
                          is_star: false
                          subheading: ''
                        - path: N06.850.505.400.975.550.900
                          is_subheading_star: false
                          origin_string: Survival Rate
                          term: Survival Rate
                          is_star: false
                          subheading: ''
                        - path: N06.850.520.308.985.550.900
                          is_subheading_star: false
                          origin_string: Survival Rate
                          term: Survival Rate
                          is_star: false
                          subheading: ''
                      journalId: '2668'
                      docPublishTime: '2021-07-01T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: World journal of surgery
                      docFirstAuthor: Teijiro Hirashita
                      videoUrl: ''
                      docMeshTerms: >-
                        Carcinoma, Renal Cell* / surgery $$ Humans $$ Kidney
                        Neoplasms* / surgery $$ Pancreatectomy $$ Pancreatic
                        Neoplasms* / surgery $$ Prognosis $$ Survival Rate
                      pptEnUrl: ''
                      illness: 肿瘤::肾癌 $$肿瘤::胰腺癌
                      highLightDocKeywords: ''
                      citedBy: '2'
                      queryScore: 4
                      docInfo: ''
                      pmid: '33768307'
                      docTitleZh: ''
                      docAuthorNested:
                        - name: Teijiro Hirashita
                        - name: Yukio Iwashita
                        - name: Yuichi Endo
                        - name: Atsuro Fujinaga
                        - name: Toshitaka Shin
                        - name: Hiromitsu Mimata
                        - name: Masafumi Inomata
                      meshTags: ''
                      docLastAuthor: Masafumi Inomata
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Meta-Analysis
                    - country: ''
                      modifiedTime: '2025-08-26T14:15:01Z'
                      docTags: >-
                        First-line$Immune-based combinations$Immunotherapy$Renal
                        cell carcinoma$Tyrosine kinase inhibitors
                      zkyArea: 医学 1区
                      docKeywordsQuery: >-
                        First-line, Immune-based combinations, Immunotherapy,
                        Renal cell carcinoma, Tyrosine kinase inhibitors.
                      year: ''
                      docLastAddr: ' Oncology Unit, Macerata Hospital, Macerata, Italy.'
                      docDoi: 10.1016/j.ejca.2021.06.015
                      docTitle: >-
                        Immune-based combinations for the treatment of
                        metastatic renal cell carcinoma: a meta-analysis of
                        randomised clinical trials
                      qiniuUrl: >-
                        https://doc3.infox-med.com/34265504_3d5896bff8ac4630b3564ba8a8425d73.pdf
                      highLightDocAbstract: >-
                        Background: Recent years have witnessed the advent of
                        novel treatment options for metastatic renal cell
                        carcinoma (mRCC), including combination therapies with
                        immune checkpoint inhibitors. Herein, we conducted an
                        up-to-date and comprehensive meta-analysis including
                        recently published data of phase III clinical trials
                        evaluating immune-based combinations in mRCC. 

                        Methods: We retrieved all the relevant trials published
                        from 15th June 2008 to 24th February 2021, evaluating
                        immune-based combinations in treatment-naïve mRCC
                        through PubMed/MEDLINE, Cochrane library, and EMBASE;
                        additionally, proceedings of the main international
                        oncological meetings were also searched for relevant
                        abstracts. Outcomes of interest included overall
                        survival (OS), progression-free survival (PFS), complete
                        response (CR) rate, and overall response rate (ORR).
                        Hazard ratios (HRs) and their 95% confidence intervals
                        (CIs) for OS and PFS, and odds ratios (ORs) and 95% CIs
                        for CR rate and ORR, were extracted. 

                        Results: Overall, 6 phase III studies involving 5175
                        treatment-naïve mRCC patients were available for the
                        meta-analysis (immune-based combinations, n = 2576;
                        sunitinib, n = 2597). According to our results, the use
                        of immune-based combinations decreased the risk of death
                        by 26% (HR 0.74, 95% CI 0.67-0.81, P &lt; 0.001);
                        similarly, a PFS benefit was observed (HR 0.68, 95% CI
                        0.54-0.85, P = 0.001). In addition, immune-based
                        combinations showed better CR rate and ORR, with ORs of
                        3.04 (95% CI 2.31-3.99, P = 0.001) and 2.53 (95% CI
                        1.77-3.62, P &lt; 0.03), respectively. 

                        Conclusions: The results of our meta-analysis confirm
                        the clinical benefit provided by immunotherapy
                        combinations, with CR rate more than tripled in mRCCs
                        receiving immune-based combinations. Further studies in
                        real-world setting are warranted to validate the
                        findings of our meta-analysis, the most updated to
                        systematically evaluate immune-based combinations in
                        mRCC.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Immune-based combinations for the treatment of
                        metastatic renal cell carcinoma: a meta-analysis of
                        randomised clinical trials
                      docTagsQuery:
                        - First-line
                        - Immune-based combinations
                        - Immunotherapy
                        - Renal cell carcinoma
                        - Tyrosine kinase inhibitors
                      docAddrQuery:
                        - >-
                          Medical Oncology, IRCCS Azienda
                          Ospedaliero-Universitaria di Bologna, Bologna, Italy.
                          Electronic address: francesco.massari@aosp.bo.it.
                        - >-
                          Medical Oncology, IRCCS Azienda
                          Ospedaliero-Universitaria di Bologna, Bologna, Italy.
                        - Oncology Unit, Macerata Hospital, Macerata, Italy.
                      pages: '0'
                      province: ''
                      createdTime: '2021-07-23T18:25:14Z'
                      aiOverview: ''
                      id: '21892823'
                      docAuthor: >-
                        Francesco Massari,Alessandro Rizzo,Veronica
                        Mollica,Matteo Rosellini,Andrea Marchetti,Andrea
                        Ardizzoni,Matteo Santoni
                      docAddr: ' Medical Oncology, IRCCS Azienda Ospedaliero-Universitaria di Bologna, Bologna, Italy. Electronic address: francesco.massari@aosp.bo.it.;; Medical Oncology, IRCCS Azienda Ospedaliero-Universitaria di Bologna, Bologna, Italy.;; Oncology Unit, Macerata Hospital, Macerata, Italy.'
                      issue: ''
                      pptUrl: ''
                      docFirstAddr: ' Medical Oncology, IRCCS Azienda Ospedaliero-Universitaria di Bologna, Bologna, Italy. Electronic address: francesco.massari@aosp.bo.it.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Meta-Analysis
                      qiniuUrlZh: ''
                      docKeywords: >-
                        First-line, Immune-based combinations, Immunotherapy,
                        Renal cell carcinoma, Tyrosine kinase inhibitors.
                      diseaseTagsQuery:
                        - '267'
                      volume: ''
                      docAbstract: >-
                        Background: Recent years have witnessed the advent of
                        novel treatment options for metastatic renal cell
                        carcinoma (mRCC), including combination therapies with
                        immune checkpoint inhibitors. Herein, we conducted an
                        up-to-date and comprehensive meta-analysis including
                        recently published data of phase III clinical trials
                        evaluating immune-based combinations in mRCC. 

                        Methods: We retrieved all the relevant trials published
                        from 15th June 2008 to 24th February 2021, evaluating
                        immune-based combinations in treatment-naïve mRCC
                        through PubMed/MEDLINE, Cochrane library, and EMBASE;
                        additionally, proceedings of the main international
                        oncological meetings were also searched for relevant
                        abstracts. Outcomes of interest included overall
                        survival (OS), progression-free survival (PFS), complete
                        response (CR) rate, and overall response rate (ORR).
                        Hazard ratios (HRs) and their 95% confidence intervals
                        (CIs) for OS and PFS, and odds ratios (ORs) and 95% CIs
                        for CR rate and ORR, were extracted. 

                        Results: Overall, 6 phase III studies involving 5175
                        treatment-naïve mRCC patients were available for the
                        meta-analysis (immune-based combinations, n = 2576;
                        sunitinib, n = 2597). According to our results, the use
                        of immune-based combinations decreased the risk of death
                        by 26% (HR 0.74, 95% CI 0.67-0.81, P &lt; 0.001);
                        similarly, a PFS benefit was observed (HR 0.68, 95% CI
                        0.54-0.85, P = 0.001). In addition, immune-based
                        combinations showed better CR rate and ORR, with ORs of
                        3.04 (95% CI 2.31-3.99, P = 0.001) and 2.53 (95% CI
                        1.77-3.62, P &lt; 0.03), respectively. 

                        Conclusions: The results of our meta-analysis confirm
                        the clinical benefit provided by immunotherapy
                        combinations, with CR rate more than tripled in mRCCs
                        receiving immune-based combinations. Further studies in
                        real-world setting are warranted to validate the
                        findings of our meta-analysis, the most updated to
                        systematically evaluate immune-based combinations in
                        mRCC.
                      pageIdx: ''
                      sourcesCode: PMID34265504
                      status: '2'
                      illnessQuery:
                        - 肿瘤::肾癌
                      docIf: '7.100'
                      docSimpleJournal: ''
                      highLightDocAuthor: >-
                        Francesco Massari, Alessandro Rizzo, Veronica Mollica,
                        Matteo Rosellini, Andrea Marchetti, Andrea Ardizzoni,
                        Matteo Santoni
                      docMeshTermsQuery:
                        - path: E02.183.750.500
                          is_subheading_star: true
                          origin_string: >-
                            Antineoplastic Combined Chemotherapy Protocols /
                            therapeutic use*
                          term: Antineoplastic Combined Chemotherapy Protocols
                          is_star: false
                          subheading: therapeutic use
                        - path: C12.950.983.535.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C04.557.470.200.025.390
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C04.588.945.947.535.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C12.200.758.820.750.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C12.200.777.419.473.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535.160
                          is_subheading_star: true
                          origin_string: Carcinoma, Renal Cell / drug therapy*
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: drug therapy
                        - path: C12.950.983.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C04.557.470.200.025.390
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C04.588.945.947.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C12.200.758.820.750.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C12.200.777.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C12.050.351.968.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: C12.050.351.937.820.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell / mortality
                          term: Carcinoma, Renal Cell
                          is_star: false
                          subheading: mortality
                        - path: B01.050.150.900.649.313.988.400.112.400.400
                          is_subheading_star: false
                          origin_string: Humans
                          term: Humans
                          is_star: false
                          subheading: ''
                        - path: D27.505.519.507
                          is_subheading_star: false
                          origin_string: Immune Checkpoint Inhibitors / therapeutic use
                          term: Immune Checkpoint Inhibitors
                          is_star: false
                          subheading: therapeutic use
                        - path: D27.505.954.248.384.500
                          is_subheading_star: false
                          origin_string: Immune Checkpoint Inhibitors / therapeutic use
                          term: Immune Checkpoint Inhibitors
                          is_star: false
                          subheading: therapeutic use
                        - path: C12.900.820.535
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.950.419.473
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.950.983.535
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C04.588.945.947.535
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.200.758.820.750
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.200.777.419.473
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473
                          is_subheading_star: true
                          origin_string: Kidney Neoplasms / drug therapy*
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: drug therapy
                        - path: C12.900.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.950.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.950.983.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C04.588.945.947.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.200.758.820.750
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.200.777.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.050.351.937.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: C12.050.351.968.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms / mortality
                          term: Kidney Neoplasms
                          is_star: false
                          subheading: mortality
                        - path: E05.318.372.250.250.365.500
                          is_subheading_star: false
                          origin_string: Randomized Controlled Trials as Topic
                          term: Randomized Controlled Trials as Topic
                          is_star: false
                          subheading: ''
                        - path: N06.850.520.450.250.250.365.500
                          is_subheading_star: false
                          origin_string: Randomized Controlled Trials as Topic
                          term: Randomized Controlled Trials as Topic
                          is_star: false
                          subheading: ''
                        - path: N05.715.360.330.250.250.365.500
                          is_subheading_star: false
                          origin_string: Randomized Controlled Trials as Topic
                          term: Randomized Controlled Trials as Topic
                          is_star: false
                          subheading: ''
                      journalId: '3455'
                      docPublishTime: '2021-09-01T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: 'European journal of cancer (Oxford, England : 1990)'
                      docFirstAuthor: Francesco Massari
                      videoUrl: ''
                      docMeshTerms: >-
                        Antineoplastic Combined Chemotherapy Protocols /
                        therapeutic use* $$ Carcinoma, Renal Cell / drug
                        therapy* $$ Carcinoma, Renal Cell / mortality $$ Humans
                        $$ Immune Checkpoint Inhibitors / therapeutic use $$
                        Kidney Neoplasms / drug therapy* $$ Kidney Neoplasms /
                        mortality $$ Randomized Controlled Trials as Topic
                      pptEnUrl: ''
                      illness: 肿瘤::肾癌
                      highLightDocKeywords: ''
                      citedBy: '6'
                      queryScore: 4
                      docInfo: ''
                      pmid: '34265504'
                      docTitleZh: 基于免疫的联合治疗在治疗转移性肾细胞癌中的效果：随机临床试验的meta分析
                      docAuthorNested:
                        - name: Francesco Massari
                        - name: Alessandro Rizzo
                        - name: Veronica Mollica
                        - name: Matteo Rosellini
                        - name: Andrea Marchetti
                        - name: Andrea Ardizzoni
                        - name: Matteo Santoni
                      meshTags: ''
                      docLastAuthor: Matteo Santoni
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Meta-Analysis
                    - country: ''
                      modifiedTime: '2025-08-26T15:46:18Z'
                      docTags: >-
                        meta-analysis$metabolic syndrome$obesity$renal cell
                        cancer$risk factor
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        meta-analysis, metabolic syndrome, obesity, renal cell
                        cancer, risk factor.
                      year: ''
                      docLastAddr: ' The First School of Clinical Medicine, Zhejiang Chinese Medical University, Hangzhou, China.$$ Education Department, The First Affiliated Hospital of Zhejiang Chinese Medical University (Zhejiang Provincial Hospital of Traditional Chinese Medicine), Hangzhou, China.'
                      docDoi: 10.3389/fonc.2022.928619
                      docTitle: >-
                        Association Between Metabolic Syndrome and Risk of Renal
                        Cell Cancer: A Meta-Analysis
                      qiniuUrl: >-
                        https://doc3.infox-med.com/35832547_67d3b7349a004af1b8f6f35a64c64b61.pdf
                      highLightDocAbstract: >-
                        Background: Metabolic syndrome (MetS) has been related
                        to increased risks of a variety of cancers. However, the
                        association between MetS and the risk of renal cell
                        cancer (RCC) remains not fully determined. This
                        meta-analysis was conducted to investigate whether MetS
                        is independently associated with the risk of RCC in
                        adults. 

                        Methods: Relevant observational studies were obtained by
                        searching PubMed, Embase, Cochrane's Library, and Web of
                        Science databases. Study characteristics and outcome
                        data were extracted independently by two authors. The
                        random-effect model was used for meta-analysis
                        considering the possible influence of between-study
                        heterogeneity. Predefined subgroup analyses were used to
                        evaluate the possible influences of study
                        characteristics on the outcome. 

                        Results: Eight studies involving 10,601,006 participants
                        contributed to the meta-analysis. Results showed that
                        MetS was independently associated with a higher risk of
                        RCC in adult population (risk ratio [RR]: 1.62, 95%
                        confidence interval [CI]: 1.41 to 1.87, p&lt;0.001; I2 =
                        85%). Subgroup analyses showed consistent association in
                        men (RR: 1.52, 95% CI: 1.23 to 1.89, p&lt;0.001) and in
                        women (RR: 1.71, 95% CI: 1.28 to 2.27, p&lt;0.001), in
                        Asians (RR: 1.51, 95% CI: 1.25 to 1.83, p&lt;0.001) and
                        in Caucasians (RR: 1.76, 95% CI: 1.46 to 2.12,
                        p&lt;0.001), and in community derived (RR: 1.56, 95% CI:
                        1.34 to 1.82, p&lt;0.001) and non-community derived
                        population (RR: 1.87, 95% CI: 1.71 to 2.04, p&lt;0.001).
                        Differences in study design or quality score also did
                        not significantly affect the association (p for subgroup
                        difference both &gt;0.05). 

                        Conclusions: MetS may be independently associated with
                        RCC in adult population.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Association Between Metabolic Syndrome and Risk of Renal
                        Cell Cancer: A Meta-Analysis
                      docTagsQuery:
                        - meta-analysis
                        - metabolic syndrome
                        - obesity
                        - renal cell cancer
                        - risk factor
                      docAddrQuery:
                        - >-
                          The First School of Clinical Medicine, Zhejiang
                          Chinese Medical University, Hangzhou, China.
                        - >-
                          Department of Oncology, Affiliated Hangzhou First
                          People's Hospital, Zhejiang University School of
                          Medicine, Hangzhou, China.
                        - >-
                          Department of Oncology, The Fourth School of Clinical
                          Medicine, Zhejiang Chinese Medical University,
                          Hangzhou, China.
                        - >-
                          Oncology Department, The Second Affiliated Hospital of
                          Zhejiang Chinese Medical University (Xinhua Hospital
                          of Zhejiang Province), Hangzhou, China.
                        - >-
                          Department of Medical Oncology, The First Affiliated
                          Hospital of Zhejiang Chinese Medical University
                          (Zhejiang Provincial Hospital of Traditional Chinese
                          Medicine), Hangzhou, China.
                        - >-
                          Education Department, The First Affiliated Hospital of
                          Zhejiang Chinese Medical University (Zhejiang
                          Provincial Hospital of Traditional Chinese Medicine),
                          Hangzhou, China.
                      pages: '0'
                      province: ''
                      createdTime: '2022-07-15T17:30:34Z'
                      aiOverview: ''
                      id: '36097948'
                      docAuthor: >-
                        Wurong Du,Kaibo Guo,Huimin Jin,Leitao Sun,Shanming
                        Ruan,Qiaoling Song
                      docAddr: ' The First School of Clinical Medicine, Zhejiang Chinese Medical University, Hangzhou, China.;; Department of Oncology, Affiliated Hangzhou First People''s Hospital, Zhejiang University School of Medicine, Hangzhou, China.;; Department of Oncology, The Fourth School of Clinical Medicine, Zhejiang Chinese Medical University, Hangzhou, China.;; Oncology Department, The Second Affiliated Hospital of Zhejiang Chinese Medical University (Xinhua Hospital of Zhejiang Province), Hangzhou, China.;; Department of Medical Oncology, The First Affiliated Hospital of Zhejiang Chinese Medical University (Zhejiang Provincial Hospital of Traditional Chinese Medicine), Hangzhou, China.;; Education Department, The First Affiliated Hospital of Zhejiang Chinese Medical University (Zhejiang Provincial Hospital of Traditional Chinese Medicine), Hangzhou, China.'
                      issue: ''
                      pptUrl: ''
                      docFirstAddr: ' The First School of Clinical Medicine, Zhejiang Chinese Medical University, Hangzhou, China.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        meta-analysis, metabolic syndrome, obesity, renal cell
                        cancer, risk factor.
                      diseaseTagsQuery:
                        - '267'
                      volume: ''
                      docAbstract: >-
                        Background: Metabolic syndrome (MetS) has been related
                        to increased risks of a variety of cancers. However, the
                        association between MetS and the risk of renal cell
                        cancer (RCC) remains not fully determined. This
                        meta-analysis was conducted to investigate whether MetS
                        is independently associated with the risk of RCC in
                        adults. 

                        Methods: Relevant observational studies were obtained by
                        searching PubMed, Embase, Cochrane's Library, and Web of
                        Science databases. Study characteristics and outcome
                        data were extracted independently by two authors. The
                        random-effect model was used for meta-analysis
                        considering the possible influence of between-study
                        heterogeneity. Predefined subgroup analyses were used to
                        evaluate the possible influences of study
                        characteristics on the outcome. 

                        Results: Eight studies involving 10,601,006 participants
                        contributed to the meta-analysis. Results showed that
                        MetS was independently associated with a higher risk of
                        RCC in adult population (risk ratio [RR]: 1.62, 95%
                        confidence interval [CI]: 1.41 to 1.87, p&lt;0.001; I2 =
                        85%). Subgroup analyses showed consistent association in
                        men (RR: 1.52, 95% CI: 1.23 to 1.89, p&lt;0.001) and in
                        women (RR: 1.71, 95% CI: 1.28 to 2.27, p&lt;0.001), in
                        Asians (RR: 1.51, 95% CI: 1.25 to 1.83, p&lt;0.001) and
                        in Caucasians (RR: 1.76, 95% CI: 1.46 to 2.12,
                        p&lt;0.001), and in community derived (RR: 1.56, 95% CI:
                        1.34 to 1.82, p&lt;0.001) and non-community derived
                        population (RR: 1.87, 95% CI: 1.71 to 2.04, p&lt;0.001).
                        Differences in study design or quality score also did
                        not significantly affect the association (p for subgroup
                        difference both &gt;0.05). 

                        Conclusions: MetS may be independently associated with
                        RCC in adult population.
                      pageIdx: ''
                      sourcesCode: PMID35832547
                      status: '1'
                      docIf: '3.300'
                      docSimpleJournal: ''
                      highLightDocAuthor: >-
                        Wurong Du, Kaibo Guo, Huimin Jin, Leitao Sun, Shanming
                        Ruan, Qiaoling Song
                      journalId: '6126'
                      docPublishTime: '2022-06-27T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in oncology
                      docAbstractZh: >-
                        背景:代谢综合征(MetS)与多种癌症的风险增加有关。然而，MetS与肾细胞癌(RCC)风险之间的关系仍未完全确定。这项荟萃分析的目的是调查MetS是否与成人RCC风险独立相关。

                        方法:检索PubMed、Embase、Cochrane's Library和Web of
                        Science数据库，获取相关观察性研究。研究特征和结果数据由两位作者独立提取。考虑到研究间异质性的可能影响，采用随机效应模型进行meta分析。采用预先定义的亚组分析来评估研究特征对结果的可能影响。

                        结果:8项研究涉及10,601,006名参与者参与了meta分析。结果显示，在成人人群中，MetS与较高的RCC风险独立相关(风险比[RR]:
                        1.62, 95%置信区间[CI]: 1.41 ~ 1.87, p&lt;0.001;I2 =
                        85%)。亚组分析显示，男性(RR: 1.52, 95% CI: 1.23 ~ 1.89,
                        p&lt;0.001)和女性(RR: 1.71, 95% CI: 1.28 ~ 2.27,
                        p&lt;0.001)、亚洲人(RR: 1.51, 95% CI: 1.25 ~ 1.83,
                        p&lt;0.001)、白种人(RR: 1.76, 95% CI: 1.46 ~ 2.12,
                        p&lt;0.001)、社区衍生人群(RR: 1.56, 95% CI: 1.34 ~ 1.82,
                        p&lt;0.001)和非社区衍生人群(RR: 1.87, 95% CI: 1.71 ~ 2.04,
                        p&lt;0.001)具有一致的相关性。研究设计或质量评分的差异也不显著影响相关性(p为亚组差异&gt;0.05)。

                        结论:在成人人群中，MetS可能与RCC独立相关。
                      docFirstAuthor: Wurong Du
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: ''
                      pmid: '35832547'
                      docTitleZh: 代谢综合征与肾细胞癌风险的相关性:一项meta分析
                      docAuthorNested:
                        - name: Wurong Du
                        - name: Kaibo Guo
                        - name: Huimin Jin
                        - name: Leitao Sun
                        - name: Shanming Ruan
                        - name: Qiaoling Song
                      meshTags: ''
                      docLastAuthor: Qiaoling Song
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T15:41:23Z'
                      docTags: >-
                        VEGF targeted therapy$combination
                        therapy$efficacy$immune checkpoint inhibitors
                        (ICI)$renal cell carcinoma (RCC)$safety
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        VEGF targeted therapy; combination therapy; efficacy;
                        immune checkpoint inhibitors (ICI); renal cell carcinoma
                        (RCC); safety.
                      year: '2021'
                      docLastAddr: ' Department of Oncology, Beijing Chaoyang Hospital, Capital Medical University, Beijing, China.'
                      docDoi: 10.3389/fonc.2021.739263
                      docTitle: >-
                        Balancing the Risk-Benefit Ratio of Immune Checkpoint
                        Inhibitor and Anti-VEGF Combination Therapy in Renal
                        Cell Carcinoma: A Systematic Review and Meta-Analysis
                      qiniuUrl: >-
                        https://doc3.infox-med.com/34722290_182e734add824eb7a829609c2e2e67f4.pdf
                      highLightDocAbstract: >-
                        Background: Although immune checkpoint inhibitors (ICIs)
                        combined with vascular endothelial growth factor
                        receptor (VEGFR)-targeted therapy and sunitinib
                        monotherapy have been widely applied to metastatic renal
                        cell carcinoma (mRCC), effectiveness and safety data are
                        still lacking. To optimize clinical decision-making, we
                        conducted a systematic review and meta-analysis of
                        published randomized clinical trials to characterize the
                        efficacy and the risk of adverse events (AEs) in
                        patients treated with ICIs plus anti-VEGF therapy.
                        Materials and methods: We used PubMed, EMBASE, and the
                        Cochrane Library to retrieve randomized controlled
                        trials (RCTs) published before March 27, 2021. The
                        efficacy outcomes were progression-free survival (PFS),
                        overall survival (OS), and objective response rate
                        (ORR). The pooled risk ratio (RR) and 95% confidence
                        intervals (CI) of AEs were calculated in the safety
                        analysis. 

                        Results: Six RCTs involving 4,227 patients were
                        identified after a systematic search. For OS, ICI and
                        anti-VEGF combination therapy decreased mortality
                        approximately 30% in the intention-to-treat population
                        (ITT) (hazard ratio (HR) = 0.70, 95% CI: 0.57-0.87), but
                        there was no statistical difference in patients
                        evaluated as "favorable" by the International Metastatic
                        Renal-Cell Carcinoma Database Consortium (IMDC) criteria
                        compared with monotherapy (HR = 0.90, 95% CI: 0.55-1.46,
                        p = 0.66). In terms of PFS, the progression risk for all
                        participants declined 35% (HR = 0.65, 95% CI: 0.50-0.83)
                        and patients evaluated as "poor" by IMDC benefited
                        further (HR = 0.46, 95% CI: 0.36-0.58). No evident
                        divergence was found in age and sex subgroups. The RRs
                        of all-grade hypertension, arthralgia, rash,
                        proteinuria, high-grade (grades 3-5) arthralgia, and
                        proteinuria developed after combination therapy were
                        increased compared with sunitinib. The risk of
                        high-grade hypertension and rash showed no statistical
                        difference. However, the risk of hand-foot skin reaction
                        (HFSR), stomatitis, and dysgeusia decreased in
                        combination therapy groups. 

                        Conclusions: Compared with sunitinib, OS, PFS, and ORR
                        were significantly improved in patients receiving ICI
                        and anti-VEGF combination therapy at the expense of
                        increased specific AEs. More attention should be paid to
                        individualized application of these combination
                        therapies to achieve the best benefit-risk ratio in the
                        clinic. Systematic review registration:
                        [https://inplasy.com/] INPLASY: 202130104.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Balancing the Risk-Benefit Ratio of Immune Checkpoint
                        Inhibitor and Anti-VEGF Combination Therapy in Renal
                        Cell Carcinoma: A Systematic Review and Meta-Analysis
                      docTagsQuery:
                        - VEGF targeted therapy
                        - combination therapy
                        - efficacy
                        - immune checkpoint inhibitors (ICI)
                        - renal cell carcinoma (RCC)
                        - safety
                      docAddrQuery:
                        - >-
                          Beijing Chaoyang Hospital, Capital Medical University,
                          Beijing, China.
                        - >-
                          Department of Oncology, Beijing Chaoyang Hospital,
                          Capital Medical University, Beijing, China.
                      pages: '0'
                      province: ''
                      createdTime: '2021-11-02T17:54:20Z'
                      aiOverview: ''
                      id: '34917526'
                      docAuthor: >-
                        Li Tao,Huiyun Zhang,Guangyu An,Haoning Lan,Yaoqi Xu,Yang
                        Ge,Jiannan Yao
                      docAddr: >-
                        Beijing Chaoyang Hospital, Capital Medical University,
                        Beijing, China.;;Department of Oncology, Beijing
                        Chaoyang Hospital, Capital Medical University, Beijing,
                        China.
                      issue: N/A
                      pptUrl: ''
                      docFirstAddr: ' Beijing Chaoyang Hospital, Capital Medical University, Beijing, China.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        VEGF targeted therapy; combination therapy; efficacy;
                        immune checkpoint inhibitors (ICI); renal cell carcinoma
                        (RCC); safety.
                      diseaseTagsQuery:
                        - '267'
                      volume: '11'
                      docAbstract: >-
                        Background: Although immune checkpoint inhibitors (ICIs)
                        combined with vascular endothelial growth factor
                        receptor (VEGFR)-targeted therapy and sunitinib
                        monotherapy have been widely applied to metastatic renal
                        cell carcinoma (mRCC), effectiveness and safety data are
                        still lacking. To optimize clinical decision-making, we
                        conducted a systematic review and meta-analysis of
                        published randomized clinical trials to characterize the
                        efficacy and the risk of adverse events (AEs) in
                        patients treated with ICIs plus anti-VEGF therapy.
                        Materials and methods: We used PubMed, EMBASE, and the
                        Cochrane Library to retrieve randomized controlled
                        trials (RCTs) published before March 27, 2021. The
                        efficacy outcomes were progression-free survival (PFS),
                        overall survival (OS), and objective response rate
                        (ORR). The pooled risk ratio (RR) and 95% confidence
                        intervals (CI) of AEs were calculated in the safety
                        analysis. 

                        Results: Six RCTs involving 4,227 patients were
                        identified after a systematic search. For OS, ICI and
                        anti-VEGF combination therapy decreased mortality
                        approximately 30% in the intention-to-treat population
                        (ITT) (hazard ratio (HR) = 0.70, 95% CI: 0.57-0.87), but
                        there was no statistical difference in patients
                        evaluated as "favorable" by the International Metastatic
                        Renal-Cell Carcinoma Database Consortium (IMDC) criteria
                        compared with monotherapy (HR = 0.90, 95% CI: 0.55-1.46,
                        p = 0.66). In terms of PFS, the progression risk for all
                        participants declined 35% (HR = 0.65, 95% CI: 0.50-0.83)
                        and patients evaluated as "poor" by IMDC benefited
                        further (HR = 0.46, 95% CI: 0.36-0.58). No evident
                        divergence was found in age and sex subgroups. The RRs
                        of all-grade hypertension, arthralgia, rash,
                        proteinuria, high-grade (grades 3-5) arthralgia, and
                        proteinuria developed after combination therapy were
                        increased compared with sunitinib. The risk of
                        high-grade hypertension and rash showed no statistical
                        difference. However, the risk of hand-foot skin reaction
                        (HFSR), stomatitis, and dysgeusia decreased in
                        combination therapy groups. 

                        Conclusions: Compared with sunitinib, OS, PFS, and ORR
                        were significantly improved in patients receiving ICI
                        and anti-VEGF combination therapy at the expense of
                        increased specific AEs. More attention should be paid to
                        individualized application of these combination
                        therapies to achieve the best benefit-risk ratio in the
                        clinic. Systematic review registration:
                        [https://inplasy.com/] INPLASY: 202130104.
                      pageIdx: '739263.'
                      sourcesCode: PMID34722290
                      status: '2'
                      docIf: '3.300'
                      docSimpleJournal: Front Oncol
                      highLightDocAuthor: >-
                        Li Tao, Huiyun Zhang, Guangyu An, Haoning Lan, Yaoqi Xu,
                        Yang Ge, Jiannan Yao
                      journalId: '6126'
                      docPublishTime: '2021-10-14T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in oncology
                      docAbstractZh: >-
                        背景：尽管免疫检查点抑制剂（ICIs）联合血管内皮生长因子受体（VEGFR）靶向治疗和舒尼替尼单药治疗已广泛应用于转移性肾细胞癌（mRCC），但有效性和安全性数据仍然缺乏。为了优化临床决策，我们对已发表的随机临床试验进行了系统回顾和荟萃分析，以表征接受ICIs
                        +抗vegf治疗的患者的疗效和不良事件（ae）风险。材料和方法：我们使用PubMed、EMBASE和Cochrane图书馆检索在2021年3月27日之前发表的随机对照试验（RCTs）。疗效指标为无进展生存期（PFS）、总生存期（OS）和客观缓解率（ORR）。在安全性分析中计算ae的合并风险比（RR）和95%置信区间（CI）。

                        结果：经过系统检索，确定了6项随机对照试验，涉及4,227例患者。对于OS，
                        ICI和抗vegf联合治疗在意向治疗人群（ITT）中降低了约30%的死亡率（风险比(HR) = 0.70,
                        95% CI:
                        0.57-0.87），但在国际转移性肾细胞癌数据库联盟（IMDC）标准中评估为“有利”的患者与单药治疗相比没有统计学差异（HR
                        = 0.90, 95% CI: 0.55-1.46, p =
                        0.66）。在PFS方面，所有参与者的进展风险下降了35% (HR = 0.65, 95% CI:
                        0.50-0.83)， IMDC评估为“差”的患者进一步受益（HR = 0.46, 95% CI:
                        0.36-0.58）。在年龄和性别亚组中没有发现明显的差异。与舒尼替尼相比，联合治疗后出现的所有级别高血压、关节痛、皮疹、蛋白尿、高级别（3-5级）关节痛和蛋白尿的rrr均有所增加。发生高级别高血压和皮疹的风险无统计学差异。然而，联合治疗组手足皮肤反应（HFSR）、口炎和吞咽困难的风险降低。

                        结论：与舒尼替尼相比，接受ICI和抗vegf联合治疗的患者的OS、PFS和ORR显著改善，但代价是特异性ae增加。应注意个体化应用这些联合疗法，以达到最佳的临床获益-风险比。系统评审注册：[https://inplasy.com/]
                        INPLASY: 202130104]。
                      docFirstAuthor: Li Tao
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '6'
                      queryScore: 4
                      docInfo: >-
                        2021 Oct 14:11:739263. doi: 10.3389/fonc.2021.739263.
                        eCollection 2021.
                      pmid: '34722290'
                      docTitleZh: 平衡免疫检查点抑制剂和抗vegf联合治疗肾细胞癌的风险-收益比：一项系统综述和荟萃分析
                      docAuthorNested:
                        - name: Li Tao
                        - name: Huiyun Zhang
                        - name: Guangyu An
                        - name: Haoning Lan
                        - name: Yaoqi Xu
                        - name: Yang Ge
                        - name: Jiannan Yao
                      meshTags: ''
                      docLastAuthor: Jiannan Yao
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T16:01:13Z'
                      docTags: ''
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        diagnosis, exosomal microRNAs, meta-analysis, miRNA,
                        renal cell carcinoma.
                      year: '2024'
                      docDoi: 10.3389/fonc.2024.1441429
                      docTitle: >-
                        Meta-analysis of the diagnostic value of exosomal
                        microRNAs in renal cell carcinoma
                      qiniuUrl: >-
                        https://doc3.infox-med.com/39558958_bfeeb0f891414113b7cb544092c786eb.pdf
                      highLightDocAbstract: >-
                        Aim: This meta-analysis aims to evaluate the potential
                        of exosomal microRNAs(Exo-miRs) as diagnostic biomarkers
                        for renal cell carcinoma(RCC). 

                        Methods: Clinical studies reporting the use of Exo-miRs
                        in the diagnosis of RCC were retrieved from PubMed, Web
                        of Science, Cochrane Library, Embase, China National
                        Knowledge Infrastructure (CNKI), Wanfang, VIP, and
                        Chinese Biomedical Literature Database (SinoMed). After
                        relevant data were screened and extracted, the quality
                        of the included studies was assessed using the QUADAS-2
                        tool. The Meta-disc (version 1.4) software was used to
                        analyze the heterogeneity of threshold/non-threshold
                        effects in the included studies. The Stata MP (version
                        16.0) software was used to calculate sensitivity(Sen),
                        specificity(Spe), positive likelihood ratio(+LR),
                        negative likelihood ratio(-LR), area under the
                        curve(AUC), diagnostic odds ratio(DOR), and publication
                        bias. 

                        Results: A total of 11 studies were included in this
                        meta-analysis. Spearman correlation coefficient was
                        0.319 (P = 0.075; &gt;0.05), indicating no threshold
                        effects. The pooled Sen, Spe, +LR, -LR, DOR, and AUC
                        were 0.73 (95% CI, 0.68-0.78), 0.81 (95% CI, 0.76-0.85),
                        3.80 (95% CI, 3.02-4.77), 0.33 (95% CI, 0.28-0.40),
                        11.48 (95% CI, 8.27-15.95), and 0.84 (95% CI,
                        0.80-0.87), respectively. No publication bias was
                        detected among the included studies. Conclusion: The
                        expression of Exo-miRs plays an important role in the
                        diagnosis of RCC. However, owing to the limited number
                        of included studies and heterogeneity among them,
                        further clinical research is necessary to verify the
                        findings of this meta-analysis. Systematic review
                        registration: https://www.crd.york.ac.uk/PROSPERO,
                        identifier CRD42023445956.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Meta-analysis of the diagnostic value of exosomal
                        microRNAs in renal cell carcinoma
                      docAddrQuery:
                        - >-
                          Department of Nephrology, the Eighth Clinical Medical
                          School of Guangzhou University of Chinese Medicine,
                          Foshan, China.
                        - >-
                          Department of Nephrology, Foshan Hospital of
                          Traditional Chinese Medicine, Foshan, China.
                        - >-
                          Department of Cardiovascular, the First Clinical
                          Medical College of Henan University of Chinese
                          Medicine, Zhengzhou, China.
                        - >-
                          Department of Oncology, Shenzhen Bao'an Authentic TCM
                          Therapy Hospital, Shenzhen, China.
                      pages: '16'
                      province: ''
                      createdTime: '2024-11-20T08:19:28Z'
                      aiOverview: ''
                      id: '40082685'
                      docAuthor: Qingru Li,Jing Tian,Cuiqing Chen,Hong Liu,Binyi Li
                      docAddr: ' Department of Nephrology, the Eighth Clinical Medical School of Guangzhou University of Chinese Medicine, Foshan, China.;; Department of Nephrology, Foshan Hospital of Traditional Chinese Medicine, Foshan, China.;; Department of Cardiovascular, the First Clinical Medical College of Henan University of Chinese Medicine, Zhengzhou, China.;; Department of Oncology, Shenzhen Bao''an Authentic TCM Therapy Hospital, Shenzhen, China.'
                      issue: N/A
                      pptUrl: ''
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        diagnosis, exosomal microRNAs, meta-analysis, miRNA,
                        renal cell carcinoma.
                      diseaseTagsQuery:
                        - '267'
                      volume: '14'
                      docAbstract: >-
                        Aim: This meta-analysis aims to evaluate the potential
                        of exosomal microRNAs(Exo-miRs) as diagnostic biomarkers
                        for renal cell carcinoma(RCC). 

                        Methods: Clinical studies reporting the use of Exo-miRs
                        in the diagnosis of RCC were retrieved from PubMed, Web
                        of Science, Cochrane Library, Embase, China National
                        Knowledge Infrastructure (CNKI), Wanfang, VIP, and
                        Chinese Biomedical Literature Database (SinoMed). After
                        relevant data were screened and extracted, the quality
                        of the included studies was assessed using the QUADAS-2
                        tool. The Meta-disc (version 1.4) software was used to
                        analyze the heterogeneity of threshold/non-threshold
                        effects in the included studies. The Stata MP (version
                        16.0) software was used to calculate sensitivity(Sen),
                        specificity(Spe), positive likelihood ratio(+LR),
                        negative likelihood ratio(-LR), area under the
                        curve(AUC), diagnostic odds ratio(DOR), and publication
                        bias. 

                        Results: A total of 11 studies were included in this
                        meta-analysis. Spearman correlation coefficient was
                        0.319 (P = 0.075; &gt;0.05), indicating no threshold
                        effects. The pooled Sen, Spe, +LR, -LR, DOR, and AUC
                        were 0.73 (95% CI, 0.68-0.78), 0.81 (95% CI, 0.76-0.85),
                        3.80 (95% CI, 3.02-4.77), 0.33 (95% CI, 0.28-0.40),
                        11.48 (95% CI, 8.27-15.95), and 0.84 (95% CI,
                        0.80-0.87), respectively. No publication bias was
                        detected among the included studies. Conclusion: The
                        expression of Exo-miRs plays an important role in the
                        diagnosis of RCC. However, owing to the limited number
                        of included studies and heterogeneity among them,
                        further clinical research is necessary to verify the
                        findings of this meta-analysis. Systematic review
                        registration: https://www.crd.york.ac.uk/PROSPERO,
                        identifier CRD42023445956.
                      pageIdx: '1441429.'
                      sourcesCode: PMID39558958
                      status: '1'
                      docIf: '3.300'
                      docSimpleJournal: ''
                      highLightDocAuthor: Qingru Li, Jing Tian, Cuiqing Chen, Hong Liu, Binyi Li
                      journalId: '6126'
                      docPublishTime: '2024-10-28T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in oncology
                      docAbstractZh: >-
                        目的：本meta分析旨在评估外泌体microRNAs（Exo-miRs）作为肾细胞癌（RCC）诊断生物标志物的潜力。方法：通过PubMed、Web
                        of Science、Cochrane
                        Library、Embase、中国国家知识基础设施（CNKI）、万方、VIP以及中国生物医学文献数据库（SinoMed）检索报道在外泌体microRNAs（Exo-miRs）诊断RCC中应用的临床研究。在提取相关数据并进行筛选后，使用QUADAS-2工具评估纳入研究的质量。采用Meta-disc（版本1.4）软件分析纳入研究中阈值/非阈值效应的异质性。
                        使用Stata
                        MP（版本16.0）软件计算了敏感性（Sen）、特异性（Spe）、阳性似然比（+LR）、阴性似然比（-LR）、曲线下面积（AUC）、诊断优势比（DOR）以及出版偏倚。结果：本meta分析共纳入11项研究。Spearman相关系数为0.319（P=0.075；>0.05），表明无阈值效应。汇总的Sen、Spe、+LR、-LR、DOR和AUC分别为0.73（95%
                        CI，0.68-0.78）、0.81（95% CI，0.76-0.85）、3.80（95%
                        CI，3.02-4.77）、0.33（95% CI，0.28-0.40）、11.48（95%
                        CI，8.27-15.95）和0.84（95%
                        CI，0.80-0.87）。纳入的研究中未发现出版偏倚。结论：Exo-miRs的表达在肾细胞癌（RCC）的诊断中起着重要作用。
                        然而，由于纳入的研究数量有限且它们之间存在异质性，因此需要进一步的临床研究来验证本元分析的发现。系统评价注册：https://www.crd.york.ac.uk/PROSPERO，标识符CRD42023445956。
                      docFirstAuthor: Qingru Li
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: >-
                        2024 Oct 28:14:1441429.doi:
                        10.3389/fonc.2024.1441429.eCollection 2024.
                      pmid: '39558958'
                      docTitleZh: ''
                      docAuthorNested:
                        - name: Qingru Li
                        - name: Jing Tian
                        - name: Cuiqing Chen
                        - name: Hong Liu
                        - name: Binyi Li
                      docLastAuthor: Binyi Li
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T15:57:46Z'
                      docTags: ''
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        adverse events; cabozantinib; immune checkpoint
                        inhibitors; renal cell carcinoma; tyrosine kinase
                        inhibitors.
                      year: '2024'
                      docDoi: 10.3389/fphar.2024.1322473
                      docTitle: >-
                        Cabozantinib in combination with immune checkpoint
                        inhibitors for renal cell carcinoma: a systematic review
                        and meta-analysis
                      qiniuUrl: >-
                        https://doc3.infox-med.com/38694912_c6964e9ab21a4a8db1e57553fa03fe6c.pdf
                      highLightDocAbstract: >-
                        Context: Cabozantinib combined with immune checkpoint
                        inhibitors (ICIs) has brought a new therapeutic effect
                        for the medical treatment of renal cell carcinoma (RCC).
                        Objectives: We performed a meta-analysis of randomized
                        controlled trials and single-arm trials to evaluate the
                        efficacy and safety of cabozantinib plus ICIs in RCC. 

                        Methods: We extracted data from PubMed, Cochrane,
                        Medline and Embase databases, and rated literature
                        quality through Cochrane risk of bias tool and MINORS.
                        RevMan5.3 software was used to analyze the results of
                        randomized controlled trials and single-arm trials. 

                        Results: A total of 7 studies were included. Treatment
                        with cabozantinib plus ICIs improved PFS [HR 0.75,
                        (95%CI: 0.52, 1.08), p = 0.12] and the OS [HR 0.80,
                        (95%CI: 0.60, 1.07), p = 0.13] in randomized controlled
                        trials. Meanwhile, the result of the ORR in randomized
                        controlled trials was [risk ratio (RR) 1.37, (95%CI:
                        1.21, 1.54), p < 0.00001] and in single-arm trials was
                        [risk difference (RD) 0.49, (95%CI: 0.26, 0.71), p <
                        0.0001]. Conclusion: Cabozantinib plus ICIs prolonged
                        the PFS and OS, and improved ORR in patients with RCC.
                        Our recommendation is to use cabozantinib plus ICIs to
                        treat advanced RCC, and to continuous monitor and manage
                        the drug-related adverse events. Systematic review
                        registration: identifier CRD42023455878.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Cabozantinib in combination with immune checkpoint
                        inhibitors for renal cell carcinoma: a systematic review
                        and meta-analysis
                      docAddrQuery:
                        - >-
                          Department of Oncology, Hangzhou Hospital of
                          Traditional Chinese Medicine Affiliated to Zhejiang
                          Chinese Medical University, Hangzhou, China.
                        - Tongde Hospital of Zhejiang Province, Hangzhou, China.
                        - Zhejiang Chinese Medical University, Hangzhou, China.
                        - >-
                          Department of Traditional Chinese Medicine, Ruijin
                          Hospital, Shanghai Jiao Tong University, School of
                          Medicine, Shanghai, China.
                        - >-
                          Department of Oncology, The First Affiliated Hospital
                          of Zhejiang Chinese Medical University, Hangzhou,
                          China.
                      pages: '15'
                      province: ''
                      createdTime: '2024-05-03T08:23:17Z'
                      aiOverview: ''
                      id: '39052889'
                      docAuthor: >-
                        Jingyang Su,Jialin Zhang,Yuqian Wu,Cui Ni,Yueyue
                        Ding,Zelin Cai,Ming Xu,Mingyang Lai,Jue Wang,Shengyou
                        Lin,Jinhua Lu
                      docAddr: >-
                        Department of Oncology, Hangzhou Hospital of Traditional
                        Chinese Medicine Affiliated to Zhejiang Chinese Medical
                        University, Hangzhou, China.;;Tongde Hospital of
                        Zhejiang Province, Hangzhou, China.;;Zhejiang Chinese
                        Medical University, Hangzhou, China.;;Department of
                        Traditional Chinese Medicine, Ruijin Hospital, Shanghai
                        Jiao Tong University, School of Medicine, Shanghai,
                        China.;;Department of Oncology, The First Affiliated
                        Hospital of Zhejiang Chinese Medical University,
                        Hangzhou, China.
                      issue: N/A
                      pptUrl: ''
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        adverse events; cabozantinib; immune checkpoint
                        inhibitors; renal cell carcinoma; tyrosine kinase
                        inhibitors.
                      diseaseTagsQuery:
                        - '267'
                      volume: '15'
                      docAbstract: >-
                        Context: Cabozantinib combined with immune checkpoint
                        inhibitors (ICIs) has brought a new therapeutic effect
                        for the medical treatment of renal cell carcinoma (RCC).
                        Objectives: We performed a meta-analysis of randomized
                        controlled trials and single-arm trials to evaluate the
                        efficacy and safety of cabozantinib plus ICIs in RCC. 

                        Methods: We extracted data from PubMed, Cochrane,
                        Medline and Embase databases, and rated literature
                        quality through Cochrane risk of bias tool and MINORS.
                        RevMan5.3 software was used to analyze the results of
                        randomized controlled trials and single-arm trials. 

                        Results: A total of 7 studies were included. Treatment
                        with cabozantinib plus ICIs improved PFS [HR 0.75,
                        (95%CI: 0.52, 1.08), p = 0.12] and the OS [HR 0.80,
                        (95%CI: 0.60, 1.07), p = 0.13] in randomized controlled
                        trials. Meanwhile, the result of the ORR in randomized
                        controlled trials was [risk ratio (RR) 1.37, (95%CI:
                        1.21, 1.54), p < 0.00001] and in single-arm trials was
                        [risk difference (RD) 0.49, (95%CI: 0.26, 0.71), p <
                        0.0001]. Conclusion: Cabozantinib plus ICIs prolonged
                        the PFS and OS, and improved ORR in patients with RCC.
                        Our recommendation is to use cabozantinib plus ICIs to
                        treat advanced RCC, and to continuous monitor and manage
                        the drug-related adverse events. Systematic review
                        registration: identifier CRD42023455878.
                      pageIdx: '1322473.'
                      sourcesCode: PMID38694912
                      status: '2'
                      docIf: '4.800'
                      docSimpleJournal: Front Pharmacol
                      highLightDocAuthor: >-
                        Jingyang Su, Jialin Zhang, Yuqian Wu, Cui Ni, Yueyue
                        Ding, Zelin Cai, Ming Xu, Mingyang Lai, Jue Wang,
                        Shengyou Lin, Jinhua Lu
                      journalId: '6128'
                      docPublishTime: '2024-04-17T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in pharmacology
                      docAbstractZh: >-
                        背景:卡博赞替尼联合免疫检查点抑制剂(ICIs)为肾细胞癌(RCC)的医学治疗带来了新的治疗效果。目的:我们对随机对照试验和单臂试验进行了荟萃分析，以评估卡博赞替尼加ICIs治疗RCC的疗效和安全性。

                        方法:从PubMed、Cochrane、Medline和Embase数据库中提取数据，通过Cochrane偏倚风险工具和未成年人对文献质量进行评分。采用RevMan5.3软件对随机对照试验和单臂试验结果进行分析。

                        结果:共纳入7项研究。在随机对照试验中，卡博赞替尼联合ICIs治疗可改善PFS [HR 0.75，
                        (95%CI: 0.52, 1.08)， p = 0.12]和OS [HR 0.80， (95%CI:
                        0.60, 1.07)， p = 0.13]。同时，随机对照试验的ORR结果为[风险比(RR) 1.37，
                        (95%CI: 1.21, 1.54)， p &lt;0.00001]，单臂试验[风险差异(RD) 0.49，
                        (95%CI: 0.26, 0.71)， p
                        &lt;0.0001]。结论:卡博赞替尼联合ICIs可延长RCC患者的PFS和OS，改善ORR。我们建议使用卡博赞替尼加ICIs治疗晚期RCC，并持续监测和管理药物相关不良事件。系统评价注册:标识符CRD42023455878。
                      docFirstAuthor: ''
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: >-
                        2024 Apr 17:15:1322473. doi: 10.3389/fphar.2024.1322473.
                        eCollection 2024.
                      pmid: '38694912'
                      docTitleZh: 卡博赞替尼联合免疫检查点抑制剂治疗肾细胞癌:系统回顾和荟萃分析
                      docAuthorNested:
                        - name: Jingyang Su
                        - name: Jialin Zhang
                        - name: Yuqian Wu
                        - name: Cui Ni
                        - name: Yueyue Ding
                        - name: Zelin Cai
                        - name: Ming Xu
                        - name: Mingyang Lai
                        - name: Jue Wang
                        - name: Shengyou Lin
                        - name: Jinhua Lu
                      meshTags: ''
                      docLastAuthor: ''
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T15:57:46Z'
                      docTags: ''
                      zkyArea: 医学 4区
                      year: '2024'
                      docDoi: 10.1097/FTD.0000000000001206
                      docTitle: >-
                        Therapeutic Drug Monitoring of Pazopanib in Renal Cell
                        Carcinoma and Soft Tissue Sarcoma: A Systematic Review
                      qiniuUrl: >-
                        https://doc3.infox-med.com/38723115_cb31a063ed5b4148931c0e9782f00fca.pdf
                      highLightDocAbstract: >-
                        Background: Pazopanib, an anti-angiogenic multitarget
                        tyrosine kinase inhibitor, has been approved for the
                        treatment of metastatic renal cell carcinoma and soft
                        tissue sarcoma. However, its recommended dose does not
                        always produce consistent outcomes, with some patients
                        experiencing adverse effects or toxicity. This
                        variability is due to differences in the systemic
                        exposure to pazopanib. This review aimed to establish
                        whether sufficient evidence exists for the routine or
                        selective therapeutic drug monitoring of pazopanib in
                        adult patients with approved indications. 

                        Methods: A systematic search of the PubMed and Web of
                        Science databases using search terms related to
                        pazopanib and therapeutic drug monitoring yielded 186
                        and 275 articles, respectively. Ten articles associated
                        with treatment outcomes or toxicity due to drug exposure
                        were selected for review. 

                        Results: The included studies were evaluated to
                        determine the significance of the relationship between
                        drug exposure/Ctrough and treatment outcomes and between
                        drug exposure and toxicity. A relationship between
                        exposure and treatment outcomes was observed in 5
                        studies, whereas the trend was nonsignificant in 4
                        studies. A relationship between exposure and toxicity
                        was observed in 6 studies, whereas 2 studies did not
                        find a significant relationship; significance was not
                        reported in 3 studies. 

                        Conclusions: Sufficient evidence supports the
                        therapeutic drug monitoring of pazopanib in adult
                        patients to improve its efficacy and/or safety in the
                        approved indications.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Therapeutic Drug Monitoring of Pazopanib in Renal Cell
                        Carcinoma and Soft Tissue Sarcoma: A Systematic Review
                      docAddrQuery:
                        - >-
                          Department of Clinical Pharmacy, University Hospital
                          Ostrava, Ostrava, Czech Republic.
                        - >-
                          Department of Biochemistry, Faculty of Science,
                          Masaryk University, Brno, Czech Republic.
                        - >-
                          Department of Biochemistry, Faculty of Medicine,
                          Masaryk University, Brno, Czech Republic.
                        - >-
                          Department of Pharmacology, Faculty of Medicine,
                          Masaryk University, Brno, Czech Republic.
                        - >-
                          Masaryk Memorial Cancer Institute, Brno, Czech
                          Republic; and.
                        - >-
                          Department of Pharmacology and Toxicology, Faculty of
                          Pharmacy, Masaryk University, Brno, Czech Republic.
                      pages: '11'
                      province: ''
                      createdTime: '2024-05-10T08:27:56Z'
                      aiOverview: ''
                      id: '39084137'
                      docAuthor: >-
                        Miroslav Turjap,Marta Pelcová,Jana Gregorová,Pavel
                        Šmak,Hiroko Martin,Jan Štingl,Ondřej Peš,Jan Juřica
                      docAddr: >-
                        Department of Clinical Pharmacy, University Hospital
                        Ostrava, Ostrava, Czech Republic.;;Department of
                        Biochemistry, Faculty of Science, Masaryk University,
                        Brno, Czech Republic.;;Department of Biochemistry,
                        Faculty of Medicine, Masaryk University, Brno, Czech
                        Republic.;;Department of Pharmacology, Faculty of
                        Medicine, Masaryk University, Brno, Czech
                        Republic.;;Masaryk Memorial Cancer Institute, Brno,
                        Czech Republic; and.;;Department of Pharmacology and
                        Toxicology, Faculty of Pharmacy, Masaryk University,
                        Brno, Czech Republic.
                      issue: '3'
                      pptUrl: ''
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: ''
                      diseaseTagsQuery:
                        - '267'
                      volume: '46'
                      docAbstract: >-
                        Background: Pazopanib, an anti-angiogenic multitarget
                        tyrosine kinase inhibitor, has been approved for the
                        treatment of metastatic renal cell carcinoma and soft
                        tissue sarcoma. However, its recommended dose does not
                        always produce consistent outcomes, with some patients
                        experiencing adverse effects or toxicity. This
                        variability is due to differences in the systemic
                        exposure to pazopanib. This review aimed to establish
                        whether sufficient evidence exists for the routine or
                        selective therapeutic drug monitoring of pazopanib in
                        adult patients with approved indications. 

                        Methods: A systematic search of the PubMed and Web of
                        Science databases using search terms related to
                        pazopanib and therapeutic drug monitoring yielded 186
                        and 275 articles, respectively. Ten articles associated
                        with treatment outcomes or toxicity due to drug exposure
                        were selected for review. 

                        Results: The included studies were evaluated to
                        determine the significance of the relationship between
                        drug exposure/Ctrough and treatment outcomes and between
                        drug exposure and toxicity. A relationship between
                        exposure and treatment outcomes was observed in 5
                        studies, whereas the trend was nonsignificant in 4
                        studies. A relationship between exposure and toxicity
                        was observed in 6 studies, whereas 2 studies did not
                        find a significant relationship; significance was not
                        reported in 3 studies. 

                        Conclusions: Sufficient evidence supports the
                        therapeutic drug monitoring of pazopanib in adult
                        patients to improve its efficacy and/or safety in the
                        approved indications.
                      pageIdx: 321-331.
                      sourcesCode: PMID38723115
                      status: '2'
                      illnessQuery:
                        - 肿瘤::肾癌
                      docIf: '2.400'
                      docSimpleJournal: Ther Drug Monit
                      highLightDocAuthor: >-
                        Miroslav Turjap, Marta Pelcová, Jana Gregorová, Pavel
                        Šmak, Hiroko Martin, Jan Štingl, Ondřej Peš, Jan Juřica
                      docMeshTermsQuery:
                        - path: D27.505.954.248.025
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / pharmacokinetics
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D27.505.696.377.077.099
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / pharmacokinetics
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D27.505.696.377.450.100
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / pharmacokinetics
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D27.505.954.248.025
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / therapeutic use
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: D27.505.696.377.077.099
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / therapeutic use
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: D27.505.696.377.450.100
                          is_subheading_star: false
                          origin_string: Angiogenesis Inhibitors* / therapeutic use
                          term: Angiogenesis Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: C12.950.983.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C04.557.470.200.025.390
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C04.588.945.947.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.758.820.750.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.777.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: E01.370.520.200
                          is_subheading_star: false
                          origin_string: Drug Monitoring* / methods
                          term: Drug Monitoring
                          is_star: true
                          subheading: methods
                        - path: B01.050.150.900.649.313.988.400.112.400.400
                          is_subheading_star: false
                          origin_string: Humans
                          term: Humans
                          is_star: false
                          subheading: ''
                        - path: D03.633.100.449
                          is_subheading_star: false
                          origin_string: Indazoles* / therapeutic use
                          term: Indazoles
                          is_star: true
                          subheading: therapeutic use
                        - path: D03.383.129.539.487
                          is_subheading_star: false
                          origin_string: Indazoles* / therapeutic use
                          term: Indazoles
                          is_star: true
                          subheading: therapeutic use
                        - path: C12.900.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.950.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.950.983.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C04.588.945.947.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.758.820.750
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.777.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: D03.383.742
                          is_subheading_star: false
                          origin_string: Pyrimidines* / pharmacokinetics
                          term: Pyrimidines
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D03.383.742
                          is_subheading_star: false
                          origin_string: Pyrimidines* / therapeutic use
                          term: Pyrimidines
                          is_star: true
                          subheading: therapeutic use
                        - path: C04.557.450.795
                          is_subheading_star: false
                          origin_string: Sarcoma* / drug therapy
                          term: Sarcoma
                          is_star: true
                          subheading: drug therapy
                        - path: D02.065.884
                          is_subheading_star: false
                          origin_string: Sulfonamides* / pharmacokinetics
                          term: Sulfonamides
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D02.886.590.700
                          is_subheading_star: false
                          origin_string: Sulfonamides* / pharmacokinetics
                          term: Sulfonamides
                          is_star: true
                          subheading: pharmacokinetics
                        - path: D02.065.884
                          is_subheading_star: false
                          origin_string: Sulfonamides* / therapeutic use
                          term: Sulfonamides
                          is_star: true
                          subheading: therapeutic use
                        - path: D02.886.590.700
                          is_subheading_star: false
                          origin_string: Sulfonamides* / therapeutic use
                          term: Sulfonamides
                          is_star: true
                          subheading: therapeutic use
                      journalId: '2301'
                      docPublishTime: '2024-06-01T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Therapeutic drug monitoring
                      docAbstractZh: >-
                        背景:Pazopanib是一种抗血管生成的多靶点酪氨酸激酶抑制剂，已被批准用于转移性肾细胞癌和软组织肉瘤的治疗。然而，其推荐剂量并不总是产生一致的结果，一些患者会出现不良反应或毒性。这种可变性是由于帕唑帕尼系统暴露的差异。本综述旨在确定是否有足够的证据证明在有批准适应症的成年患者中常规或选择性地监测帕唑帕尼的治疗药物。

                        方法:系统检索PubMed和Web of
                        Science数据库，使用与pazopanib和治疗药物监测相关的搜索词，分别获得186篇和275篇。选择10篇与治疗结果或药物暴露毒性相关的文章进行综述。

                        结果:对纳入的研究进行评估，以确定药物暴露/穿透与治疗结果之间以及药物暴露与毒性之间的关系的重要性。在5项研究中观察到暴露与治疗结果之间的关系，而在4项研究中这种趋势不显著。6项研究观察到接触与毒性之间的关系，而2项研究没有发现显著的关系;3项研究未报道显著性。

                        结论:有足够的证据支持在成人患者中监测帕唑帕尼的治疗药物，以提高其在批准适应症中的疗效和/或安全性。
                      docFirstAuthor: ''
                      videoUrl: ''
                      docMeshTerms: >-
                        Angiogenesis Inhibitors* / pharmacokinetics $$
                        Angiogenesis Inhibitors* / therapeutic use $$ Carcinoma,
                        Renal Cell* / drug therapy $$ Drug Monitoring* / methods
                        $$ Humans $$ Indazoles* / therapeutic use $$ Kidney
                        Neoplasms* / drug therapy $$ Pyrimidines* /
                        pharmacokinetics $$ Pyrimidines* / therapeutic use $$
                        Sarcoma* / drug therapy $$ Sulfonamides* /
                        pharmacokinetics $$ Sulfonamides* / therapeutic use
                      pptEnUrl: ''
                      illness: 肿瘤::肾癌
                      highLightDocKeywords: ''
                      citedBy: '1'
                      queryScore: 4
                      docInfo: >-
                        2024 Jun 1;46(3):321-331. doi:
                        10.1097/FTD.0000000000001206. Epub 2024 Apr 30.
                      pmid: '38723115'
                      docTitleZh: 帕唑帕尼治疗肾细胞癌和软组织肉瘤的药物监测:系统综述
                      docAuthorNested:
                        - name: Miroslav Turjap
                        - name: Marta Pelcová
                        - name: Jana Gregorová
                        - name: Pavel Šmak
                        - name: Hiroko Martin
                        - name: Jan Štingl
                        - name: Ondřej Peš
                        - name: Jan Juřica
                      meshTags: ''
                      docLastAuthor: ''
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T15:51:47Z'
                      docTags: ''
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        meta-analyses; partial nephrectomy; radiofrequency
                        ablation; renal cell carcinoma; treatment.
                      year: '2023'
                      docLastAddr: ' Department of Urological Surgery, Cancer Hospital of China Medical University/Liaoning Cancer Hospital & Institute, Shenyang, Liaoning, China.'
                      docDoi: 10.3389/fonc.2023.1105877
                      docTitle: >-
                        Meta analysis of clinical prognosis of radiofrequency
                        ablation versus partial nephrectomy in the treatment of
                        early renal cell carcinoma
                      qiniuUrl: >-
                        https://doc3.infox-med.com/37182152_e9009c3a0179491ba3d09c19c481bc4e.pdf
                      highLightDocAbstract: >-
                        Objective: To systematically review the differences
                        between radiofrequency ablation and partial nephrectomy
                        in patients with early-stage renal cell carcinoma, and
                        to provide evidence-based medical evidence for the
                        choice of surgery for patients with early-stage renal
                        cell carcinoma. 

                        Methods: According to the search strategy recommended by
                        the Cochrane Collaboration, Chinese databases such as
                        CNKI, VIP Chinese Science and Technology Periodicals
                        Database (VIP), and Wanfang Full-text Database were
                        searched with Chinese search terms. And PubMed and
                        MEDLINE as databases for English literature retrieval.
                        Retrieve the relevant literature on renal cell carcinoma
                        surgical methods published before May 2022, and further
                        screen radiofrequency ablation and partial nephrectomy
                        in patients with renal cell carcinoma The relevant
                        literature on the application is analyzed. RevMan5.3
                        software was used for heterogeneity test and combined
                        statistical analysis, sensitivity analysis, and subgroup
                        analysis. Analysis, and draw forest plot, using Stata
                        software Begger quantitative assessment of publication
                        bias. 

                        Results: A total of 11 articles were involved, including
                        2958 patients. According to the Jadad scale, 2 articles
                        were of low quality, and the remaining 9 articles were
                        of high quality. Results of this study demonstrates the
                        advantages of radiofrequency ablation in early-stage
                        renal cell carcinoma. The results of this meta-analysis
                        showed that compared with partial nephrectomy, there was
                        significant difference in the 5-year overall survival
                        rate between radiofrequency ablation and partial
                        nephrectomy and there was a statistically significant
                        difference between the two surgical methods in the
                        5-year relapse free survival rate of early renal cell
                        carcinoma. Conclusion: 1. Compared with partial
                        nephrectomy, the 5-year relapse-free survival rate, the
                        5-year cancer specific survival rate and the overall
                        5-year survival rate were higher in the radiofrequency
                        ablation group. 2. Compared with partial nephrectomy,
                        there was no significant difference in the postoperative
                        local tumor recurrence rate of radiofrequency ablation.
                        3. Compared with partial resection, radiofrequency
                        ablation is more beneficial to patients with renal cell
                        carcinoma.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Meta analysis of clinical prognosis of radiofrequency
                        ablation versus partial nephrectomy in the treatment of
                        early renal cell carcinoma
                      docAddrQuery:
                        - >-
                          Department of Urological Surgery, Cancer Hospital of
                          China Medical University/Liaoning Cancer Hospital &
                          Institute, Shenyang, Liaoning, China.
                      pages: '0'
                      province: ''
                      createdTime: '2023-05-15T08:47:10Z'
                      aiOverview: ''
                      id: '37483122'
                      docAuthor: Hongchen Qu,Kai Wang,Bin Hu
                      docAddr: >-
                        Department of Urological Surgery, Cancer Hospital of
                        China Medical University/Liaoning Cancer Hospital &
                        Institute, Shenyang, Liaoning, China.
                      issue: N/A
                      pptUrl: ''
                      docFirstAddr: ' Department of Urological Surgery, Cancer Hospital of China Medical University/Liaoning Cancer Hospital & Institute, Shenyang, Liaoning, China.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        meta-analyses; partial nephrectomy; radiofrequency
                        ablation; renal cell carcinoma; treatment.
                      diseaseTagsQuery:
                        - '267'
                      volume: '13'
                      docAbstract: >-
                        Objective: To systematically review the differences
                        between radiofrequency ablation and partial nephrectomy
                        in patients with early-stage renal cell carcinoma, and
                        to provide evidence-based medical evidence for the
                        choice of surgery for patients with early-stage renal
                        cell carcinoma. 

                        Methods: According to the search strategy recommended by
                        the Cochrane Collaboration, Chinese databases such as
                        CNKI, VIP Chinese Science and Technology Periodicals
                        Database (VIP), and Wanfang Full-text Database were
                        searched with Chinese search terms. And PubMed and
                        MEDLINE as databases for English literature retrieval.
                        Retrieve the relevant literature on renal cell carcinoma
                        surgical methods published before May 2022, and further
                        screen radiofrequency ablation and partial nephrectomy
                        in patients with renal cell carcinoma The relevant
                        literature on the application is analyzed. RevMan5.3
                        software was used for heterogeneity test and combined
                        statistical analysis, sensitivity analysis, and subgroup
                        analysis. Analysis, and draw forest plot, using Stata
                        software Begger quantitative assessment of publication
                        bias. 

                        Results: A total of 11 articles were involved, including
                        2958 patients. According to the Jadad scale, 2 articles
                        were of low quality, and the remaining 9 articles were
                        of high quality. Results of this study demonstrates the
                        advantages of radiofrequency ablation in early-stage
                        renal cell carcinoma. The results of this meta-analysis
                        showed that compared with partial nephrectomy, there was
                        significant difference in the 5-year overall survival
                        rate between radiofrequency ablation and partial
                        nephrectomy and there was a statistically significant
                        difference between the two surgical methods in the
                        5-year relapse free survival rate of early renal cell
                        carcinoma. Conclusion: 1. Compared with partial
                        nephrectomy, the 5-year relapse-free survival rate, the
                        5-year cancer specific survival rate and the overall
                        5-year survival rate were higher in the radiofrequency
                        ablation group. 2. Compared with partial nephrectomy,
                        there was no significant difference in the postoperative
                        local tumor recurrence rate of radiofrequency ablation.
                        3. Compared with partial resection, radiofrequency
                        ablation is more beneficial to patients with renal cell
                        carcinoma.
                      pageIdx: '1105877.'
                      sourcesCode: PMID37182152
                      status: '2'
                      docIf: '3.300'
                      docSimpleJournal: Front Oncol
                      highLightDocAuthor: Hongchen Qu, Kai Wang, Bin Hu
                      journalId: '6126'
                      docPublishTime: '2023-04-25T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in oncology
                      docFirstAuthor: Hongchen Qu
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: >-
                        2023 Apr 25:13:1105877. doi: 10.3389/fonc.2023.1105877.
                        eCollection 2023.
                      pmid: '37182152'
                      docTitleZh: ''
                      docAuthorNested:
                        - name: Hongchen Qu
                        - name: Kai Wang
                        - name: Bin Hu
                      meshTags: ''
                      docLastAuthor: Bin Hu
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                    - country: ''
                      modifiedTime: '2025-08-26T14:13:44Z'
                      docTags: >-
                        renal cell carcinoma$overall
                        survival$statin$meta-analysis
                      zkyArea: 医学 4区
                      docKeywordsQuery: >-
                        renal cell carcinoma, overall survival, statin,
                        meta-analysis.
                      year: ''
                      docLastAddr: ' Department of Urology, The First Affiliated Hospital of Dalian Medical University, Dalian, China. wuguang0613@hotmail.com.'
                      docDoi: 10.25011/cim.v43i4.34908
                      docTitle: >-
                        Statin use and the overall survival of renal cell
                        carcinoma: A meta-analysis
                      qiniuUrl: >-
                        https://doc3.infox-med.com/33370521_67bc1619f7c4438ca4d96dfcd6d1ae77.pdf
                      highLightDocAbstract: >-
                        Purpose: Statins are commonly prescribed drugs that
                        reduce cholesterol levels and the risk of cardiovascular
                        and cerebrovascular events. Clinical studies have shown
                        that statins also possess cancer-preventive properties.
                        Two studies have reported that statins also possess
                        cancer-preventive properties; however, whether statins
                        improve the prognosis of patients with renal cell
                        carcinoma is still unclear. In this study, we used
                        meta-analysis to evaluate the association between statin
                        use and overall survival risk in patients with renal
                        cell carcinoma. 

                        Methods: Published studies on statin-treated renal cell
                        carcinoma were retrieved from PubMed, Embase, The
                        Cochrane Library, China National Knowledge
                        Infrastructure and Wanfang databases from inception to
                        July 2019. The relevant data were extracted and a
                        meta-analysis was performed using Cochrane Review
                        Manager (RevMan 5.3) software. 

                        Results: Data from five studies, which reported on 5,299
                        patients, were analysed. The application of statins
                        showed no effects on the overall survival of patients
                        with renal cell carcinoma compared with the control
                        group (OR = 1.07, 95% CI:0.77 to 1.49, P = 0.68). 

                        Conclusions: The findings of this meta-analysis suggest
                        that statin application does not affect the overall
                        survival of patients with renal cell carcinoma.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Statin use and the overall survival of renal cell
                        carcinoma: A meta-analysis
                      docTagsQuery:
                        - renal cell carcinoma
                        - overall survival
                        - statin
                        - meta-analysis
                      docAddrQuery:
                        - >-
                          Department of Anesthesiology, The First Affiliated
                          Hospital of Dalian Medical University, Dalian, China.
                        - >-
                          Department of Rehabilitation, Liguang Rehabilitation
                          Hospital of Dalian Development Zone, Dalian, China.
                        - >-
                          Department of Neurobiology, Harbin Medical University,
                          Harbin, China.
                        - >-
                          Anesthesiology Department, Dalian Medical of
                          University, Dalian, China.
                        - >-
                          Department of Urology, The First Affiliated Hospital
                          of Dalian Medical University, Dalian, China.
                          wuguang0613@hotmail.com.
                      pages: '0'
                      province: ''
                      createdTime: '2021-04-30T13:16:15Z'
                      aiOverview: ''
                      id: '21506069'
                      docAuthor: >-
                        Ping Wu,Tingting Xiang,Jing Wang,Run Lv,Yimeng
                        Zhuang,Guangzhen Wu
                      docAddr: ' Department of Anesthesiology, The First Affiliated Hospital of Dalian Medical University, Dalian, China.;; Department of Rehabilitation, Liguang Rehabilitation Hospital of Dalian Development Zone, Dalian, China.;; Department of Neurobiology, Harbin Medical University, Harbin, China.;; Anesthesiology Department, Dalian Medical of University, Dalian, China.;; Department of Urology, The First Affiliated Hospital of Dalian Medical University, Dalian, China. wuguang0613@hotmail.com.'
                      issue: ''
                      pptUrl: ''
                      docFirstAddr: ' Department of Anesthesiology, The First Affiliated Hospital of Dalian Medical University, Dalian, China.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Meta-Analysis
                      qiniuUrlZh: ''
                      docKeywords: >-
                        renal cell carcinoma, overall survival, statin,
                        meta-analysis.
                      diseaseTagsQuery:
                        - '267'
                      volume: ''
                      docAbstract: >-
                        Purpose: Statins are commonly prescribed drugs that
                        reduce cholesterol levels and the risk of cardiovascular
                        and cerebrovascular events. Clinical studies have shown
                        that statins also possess cancer-preventive properties.
                        Two studies have reported that statins also possess
                        cancer-preventive properties; however, whether statins
                        improve the prognosis of patients with renal cell
                        carcinoma is still unclear. In this study, we used
                        meta-analysis to evaluate the association between statin
                        use and overall survival risk in patients with renal
                        cell carcinoma. 

                        Methods: Published studies on statin-treated renal cell
                        carcinoma were retrieved from PubMed, Embase, The
                        Cochrane Library, China National Knowledge
                        Infrastructure and Wanfang databases from inception to
                        July 2019. The relevant data were extracted and a
                        meta-analysis was performed using Cochrane Review
                        Manager (RevMan 5.3) software. 

                        Results: Data from five studies, which reported on 5,299
                        patients, were analysed. The application of statins
                        showed no effects on the overall survival of patients
                        with renal cell carcinoma compared with the control
                        group (OR = 1.07, 95% CI:0.77 to 1.49, P = 0.68). 

                        Conclusions: The findings of this meta-analysis suggest
                        that statin application does not affect the overall
                        survival of patients with renal cell carcinoma.
                      pageIdx: ''
                      sourcesCode: PMID33370521
                      status: '2'
                      illnessQuery:
                        - 肿瘤::肾癌
                      docIf: '0.800'
                      docSimpleJournal: ''
                      highLightDocAuthor: >-
                        Ping Wu, Tingting Xiang, Jing Wang, Run Lv, Yimeng
                        Zhuang, Guangzhen Wu
                      docMeshTermsQuery:
                        - path: C12.950.983.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C04.557.470.200.025.390
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C04.588.945.947.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.758.820.750.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.777.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535.160
                          is_subheading_star: false
                          origin_string: Carcinoma, Renal Cell* / drug therapy
                          term: Carcinoma, Renal Cell
                          is_star: true
                          subheading: drug therapy
                        - path: Z01.252.474.164
                          is_subheading_star: false
                          origin_string: China
                          term: China
                          is_star: false
                          subheading: ''
                        - path: B01.050.150.900.649.313.988.400.112.400.400
                          is_subheading_star: false
                          origin_string: Humans
                          term: Humans
                          is_star: false
                          subheading: ''
                        - path: D27.505.519.389.370
                          is_subheading_star: false
                          origin_string: >-
                            Hydroxymethylglutaryl-CoA Reductase Inhibitors* /
                            therapeutic use
                          term: Hydroxymethylglutaryl-CoA Reductase Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: D27.505.519.186.071.202.370
                          is_subheading_star: false
                          origin_string: >-
                            Hydroxymethylglutaryl-CoA Reductase Inhibitors* /
                            therapeutic use
                          term: Hydroxymethylglutaryl-CoA Reductase Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: D27.505.954.557.500.202.370
                          is_subheading_star: false
                          origin_string: >-
                            Hydroxymethylglutaryl-CoA Reductase Inhibitors* /
                            therapeutic use
                          term: Hydroxymethylglutaryl-CoA Reductase Inhibitors
                          is_star: true
                          subheading: therapeutic use
                        - path: C12.900.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.950.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.950.983.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C04.588.945.947.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.758.820.750
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.200.777.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.937.820.535
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: C12.050.351.968.419.473
                          is_subheading_star: false
                          origin_string: Kidney Neoplasms* / drug therapy
                          term: Kidney Neoplasms
                          is_star: true
                          subheading: drug therapy
                        - path: E01.789
                          is_subheading_star: false
                          origin_string: Prognosis
                          term: Prognosis
                          is_star: false
                          subheading: ''
                      journalId: '3651'
                      docPublishTime: '2020-12-27T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: >-
                        Clinical and investigative medicine. Medecine clinique
                        et experimentale
                      docFirstAuthor: Ping Wu
                      videoUrl: ''
                      docMeshTerms: >-
                        Carcinoma, Renal Cell* / drug therapy $$ China $$ Humans
                        $$ Hydroxymethylglutaryl-CoA Reductase Inhibitors* /
                        therapeutic use $$ Kidney Neoplasms* / drug therapy $$
                        Prognosis
                      pptEnUrl: ''
                      illness: 肿瘤::肾癌
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: ''
                      pmid: '33370521'
                      docTitleZh: 他汀类药物使用与肾细胞癌的总生存率：一项meta分析
                      docAuthorNested:
                        - name: Ping Wu
                        - name: Tingting Xiang
                        - name: Jing Wang
                        - name: Run Lv
                        - name: Yimeng Zhuang
                        - name: Guangzhen Wu
                      meshTags: ''
                      docLastAuthor: Guangzhen Wu
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Meta-Analysis
                    - country: ''
                      modifiedTime: '2025-08-26T15:40:35Z'
                      docTags: >-
                        meta-analysis$partial nephrectomy$renal cell
                        carcinoma$suture$sutureless
                      zkyArea: 医学 3区
                      docKeywordsQuery: >-
                        meta-analysis, partial nephrectomy, renal cell
                        carcinoma, suture, sutureless.
                      year: ''
                      docLastAddr: ' Department of Urology, Affiliated Hospital of Guizhou Medical University, Guiyang, China.$$ Institute of Medical Science of Guizhou Medical University, Guiyang, China.'
                      docDoi: 10.3389/fonc.2021.713645
                      docTitle: >-
                        Comparison of Sutureless Versus Suture Partial
                        Nephrectomy for Clinical T1 Renal Cell Carcinoma: A
                        Meta-Analysis of Retrospective Studies
                      qiniuUrl: >-
                        https://doc3.infox-med.com/34540681_1f44580b3d074e92a9b5d182a29061a7.pdf
                      highLightDocAbstract: >-
                        Background: Partial nephrectomy (PN) is the recommended
                        treatment for T1 renal cell carcinoma (RCC). Compared
                        with suture PN, sutureless PN reduces the difficulty and
                        time of operation, but the safety and feasibility have
                        been controversial. This meta-analysis was conducted to
                        compare the function and perioperative outcomes of
                        suture and sutureless PN for T1 RCC. 

                        Methods: Systematic literature review was performed up
                        to April 2021 using multiple databases to identify
                        eligible comparative studies. According to the Preferred
                        Reporting Items for Systematic Reviews and Meta-analysis
                        (PRISMA) criteria, identification and selection of the
                        studies were conducted. Meta-analysis was performed for
                        studies comparing suture to sutureless PN for both T1a
                        and T1b RCC. In addition, subgroup analysis was
                        performed on operation time, warm ischemia time,
                        estimated blood loss, and postoperative complications.
                        Sensitivity analysis was used in analysis with high
                        heterogeneity (operation time and estimated blood
                        loss). 

                        Results: Eight retrospective studies were included with
                        a total of 1,156 patients; of the 1,156 patients, 499
                        received sutureless PN and 707 received suture PN. The
                        results showed that sutureless PN had shorter operative
                        time (I2 = 0%, P &lt; 0.001), warm ischemia time (I2 =
                        97.5%, P &lt; 0.001), and lower clamping rate (I2 =
                        85.8%, P = 0.003), but estimated blood loss (I2 = 76.6%,
                        P = 0.064) had no difference. In the comparison of
                        perioperative outcomes, there was no significant
                        difference in postoperative complications (I2 = 0%, P =
                        0.999), positive surgical margins (I2 = 0%, P = 0.356),
                        postoperative estimated glomerular filtration rat (eGFR)
                        (I2 = 0%, P = 0.656), and tumor recurrence (I2 = 0%, P =
                        0.531). 

                        Conclusions: In T1a RCC with low RENAL score, sutureless
                        PN is a feasible choice, whereas it should not be
                        overestimated in T1b RCC.
                      diseaseTags: '267'
                      highLightDocTitle: >-
                        Comparison of Sutureless Versus Suture Partial
                        Nephrectomy for Clinical T1 Renal Cell Carcinoma: A
                        Meta-Analysis of Retrospective Studies
                      docTagsQuery:
                        - meta-analysis
                        - partial nephrectomy
                        - renal cell carcinoma
                        - suture
                        - sutureless
                      docAddrQuery:
                        - >-
                          Department of Urology, Affiliated Hospital of Guizhou
                          Medical University, Guiyang, China.
                        - >-
                          Institute of Medical Science of Guizhou Medical
                          University, Guiyang, China.
                      pages: '0'
                      province: ''
                      createdTime: '2021-09-22T17:40:16Z'
                      aiOverview: ''
                      id: '34751270'
                      docAuthor: >-
                        Wenjun Zhang,Bangwei Che,Shenghan Xu,Yi Mu,Jun He,Kaifa
                        Tang
                      docAddr: ' Department of Urology, Affiliated Hospital of Guizhou Medical University, Guiyang, China.;; Institute of Medical Science of Guizhou Medical University, Guiyang, China.'
                      issue: ''
                      pptUrl: ''
                      docFirstAddr: ' Department of Urology, Affiliated Hospital of Guizhou Medical University, Guiyang, China.'
                      textStatus: '0'
                      docPublishTypeQuery:
                        - Systematic Review
                      qiniuUrlZh: ''
                      docKeywords: >-
                        meta-analysis, partial nephrectomy, renal cell
                        carcinoma, suture, sutureless.
                      diseaseTagsQuery:
                        - '267'
                      volume: ''
                      docAbstract: >-
                        Background: Partial nephrectomy (PN) is the recommended
                        treatment for T1 renal cell carcinoma (RCC). Compared
                        with suture PN, sutureless PN reduces the difficulty and
                        time of operation, but the safety and feasibility have
                        been controversial. This meta-analysis was conducted to
                        compare the function and perioperative outcomes of
                        suture and sutureless PN for T1 RCC. 

                        Methods: Systematic literature review was performed up
                        to April 2021 using multiple databases to identify
                        eligible comparative studies. According to the Preferred
                        Reporting Items for Systematic Reviews and Meta-analysis
                        (PRISMA) criteria, identification and selection of the
                        studies were conducted. Meta-analysis was performed for
                        studies comparing suture to sutureless PN for both T1a
                        and T1b RCC. In addition, subgroup analysis was
                        performed on operation time, warm ischemia time,
                        estimated blood loss, and postoperative complications.
                        Sensitivity analysis was used in analysis with high
                        heterogeneity (operation time and estimated blood
                        loss). 

                        Results: Eight retrospective studies were included with
                        a total of 1,156 patients; of the 1,156 patients, 499
                        received sutureless PN and 707 received suture PN. The
                        results showed that sutureless PN had shorter operative
                        time (I2 = 0%, P &lt; 0.001), warm ischemia time (I2 =
                        97.5%, P &lt; 0.001), and lower clamping rate (I2 =
                        85.8%, P = 0.003), but estimated blood loss (I2 = 76.6%,
                        P = 0.064) had no difference. In the comparison of
                        perioperative outcomes, there was no significant
                        difference in postoperative complications (I2 = 0%, P =
                        0.999), positive surgical margins (I2 = 0%, P = 0.356),
                        postoperative estimated glomerular filtration rat (eGFR)
                        (I2 = 0%, P = 0.656), and tumor recurrence (I2 = 0%, P =
                        0.531). 

                        Conclusions: In T1a RCC with low RENAL score, sutureless
                        PN is a feasible choice, whereas it should not be
                        overestimated in T1b RCC.
                      pageIdx: ''
                      sourcesCode: PMID34540681
                      status: '2'
                      docIf: '3.300'
                      docSimpleJournal: ''
                      highLightDocAuthor: >-
                        Wenjun Zhang, Bangwei Che, Shenghan Xu, Yi Mu, Jun He,
                        Kaifa Tang
                      journalId: '6126'
                      docPublishTime: '2021-09-02T00:00:00Z'
                      ztTags: ''
                      docSourceJournal: Frontiers in oncology
                      docAbstractZh: >-
                        背景:部分肾切除术(PN)是T1期肾细胞癌(RCC)的推荐治疗方法。与有缝线PN相比，无缝线PN降低了手术难度和时间，但安全性和可行性一直存在争议。本荟萃分析的目的是比较T1
                        RCC的缝合和不缝合PN的功能和围手术期结果。

                        方法:使用多个数据库进行截至2021年4月的系统文献综述，以确定符合条件的比较研究。根据系统评价和荟萃分析的首选报告项目(PRISMA)标准，进行研究的识别和选择。对T1a和T1b
                        RCC的缝合与不缝合PN进行meta分析。并对手术时间、热缺血时间、预估失血量、术后并发症进行亚组分析。对异质性较高的分析(手术时间和估计失血量)采用敏感性分析。

                        结果:纳入8项回顾性研究，共1156例患者;1156例患者中，499例采用无缝线PN,
                        707例采用缝线PN。结果显示，无缝线PN手术时间较短(I2 = 0%， P
                        &lt;0.001)、热缺血时间(I2 = 97.5%， P &lt;I2 = 85.8%， P =
                        0.003)，但估计失血量(I2 = 76.6%， P =
                        0.064)差异无统计学意义。围手术期结果比较，两组术后并发症(I2 = 0%， P =
                        0.999)、手术切缘阳性(I2 = 0%， P = 0.356)、术后肾小球滤过率(eGFR)估测(I2 =
                        0%， P = 0.656)、肿瘤复发率(I2 = 0%， P = 0.531)差异无统计学意义。

                        结论:在低肾评分的T1a RCC中，无缝线PN是一种可行的选择，而在T1b RCC中不应过高估计。
                      docFirstAuthor: Wenjun Zhang
                      videoUrl: ''
                      docMeshTerms: ''
                      pptEnUrl: ''
                      illness: ''
                      highLightDocKeywords: ''
                      citedBy: '0'
                      queryScore: 4
                      docInfo: ''
                      pmid: '34540681'
                      docTitleZh: ''
                      docAuthorNested:
                        - name: Wenjun Zhang
                        - name: Bangwei Che
                        - name: Shenghan Xu
                        - name: Yi Mu
                        - name: Jun He
                        - name: Kaifa Tang
                      meshTags: ''
                      docLastAuthor: Kaifa Tang
                      organization: ''
                      category: '0'
                      xkTags: ''
                      docPublishType: Systematic Review
                  total: 76
                  size: 10
                  current: 1
                  pages: 8
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 文献搜索2.0
      x-apifox-status: developing
      x-run-in-apifox: https://app.apifox.com/web/project/6739008/apis/api-336121378-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://devapi.infox-med.com/
    description: 测试环境
  - url: https://api.infox-med.com
    description: 正式环境
security: []

```