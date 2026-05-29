"""Web 控制器（预留，待未来实现）"""

# TODO: 实现 FastAPI Web 控制器
# 此模块预留用于未来的 Web UI 实现

# 示例结构：
#
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
#
# app = FastAPI(title="AI PR Reviewer")
#
# class AnalyzeRequest(BaseModel):
#     pr_url: str
#
# class AnalyzeResponse(BaseModel):
#     analysis_id: int
#     risk_level: str
#     report_markdown: str
#
# @app.post("/api/analyze", response_model=AnalyzeResponse)
# async def analyze_pr(request: AnalyzeRequest):
#     """分析 PR"""
#     pass
#
# @app.get("/api/history")
# async def get_history(limit: int = 20, offset: int = 0):
#     """获取分析历史"""
#     pass
#
# @app.get("/api/analysis/{analysis_id}")
# async def get_analysis(analysis_id: int):
#     """根据 ID 获取分析"""
#     pass
